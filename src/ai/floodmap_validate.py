import cv2
import numpy as np
import pandas as pd
import os
from typing import Tuple
from src.config import SAFEMAP_DATA_DIR


def parse_bounds_from_filename(filename: str) -> Tuple[float, float, float, float, int, int]:
    import re
    pattern = r"flood_map\((-?\d+\.?\d*),(-?\d+\.?\d*),(-?\d+\.?\d*),(-?\d+\.?\d*)\)\((\d+)X(\d+)\)"
    match = re.search(pattern, filename)
    if not match:
        raise ValueError(f"Cannot parse filename: {filename}")

    lon_min, lat_min, lon_max, lat_max, width, height = match.groups()
    return float(lon_min), float(lat_min), float(lon_max), float(lat_max), int(width), int(height)


def lonlat_to_pixel(lon: float, lat: float, lon_min: float, lat_min: float,
                    lon_max: float, lat_max: float, width: int, height: int) -> Tuple[int, int]:
    x = int((lon - lon_min) / (lon_max - lon_min) * width)
    y = int((lat_max - lat) / (lat_max - lat_min) * height)
    return x, y


def csv_to_png(csv_path: str, output_png_path: str) -> None:
    df = pd.read_csv(csv_path)
    filename = os.path.basename(csv_path)
    lon_min, lat_min, lon_max, lat_max, width, height = parse_bounds_from_filename(filename)

    img = np.zeros((height, width, 3), dtype=np.uint8)

    for _, row in df.iterrows():
        x = int(round(row['pixel_centroid_x']))
        y = int(round(row['pixel_centroid_y']))

        if 0 <= x < width and 0 <= y < height:
            img[y, x] = [255, 0, 0]

    cv2.imwrite(output_png_path, img)
    print(f"Generated PNG: {output_png_path}")


def calculate_difference(original_png: str, generated_png: str) -> Tuple[np.ndarray, float]:
    original = cv2.imread(original_png)
    generated = cv2.imread(generated_png)

    if original is None:
        raise FileNotFoundError(f"Cannot load original image: {original_png}")
    if generated is None:
        raise FileNotFoundError(f"Cannot load generated image: {generated_png}")

    if original.shape != generated.shape:
        print(f"Resizing generated image from {generated.shape} to {original.shape}")
        generated = cv2.resize(generated, (original.shape[1], original.shape[0]))

    original_flood_mask = np.any(original != [255, 255, 255], axis=2)
    generated_flood_mask = np.any(generated != [0, 0, 0], axis=2)

    orig_flood_count = np.sum(original_flood_mask)
    gen_flood_count = np.sum(generated_flood_mask)

    overlap = original_flood_mask & generated_flood_mask
    overlap_count = np.sum(overlap)

    missed = original_flood_mask & ~generated_flood_mask
    false_positive = generated_flood_mask & ~original_flood_mask

    missed_count = np.sum(missed)
    false_pos_count = np.sum(false_positive)

    diff_vis = np.zeros_like(original)
    diff_vis[overlap] = [0, 255, 0]
    diff_vis[missed] = [0, 0, 255]
    diff_vis[false_positive] = [255, 0, 0]

    total_flood_union = np.sum(original_flood_mask | generated_flood_mask)
    if total_flood_union == 0:
        loss_percentage = 0.0
    else:
        loss_percentage = ((missed_count + false_pos_count) / total_flood_union) * 100

    print(f"  Original flood pixels: {orig_flood_count}")
    print(f"  Generated flood pixels: {gen_flood_count}")
    print(f"  Correct detections: {overlap_count}")
    print(f"  Missed detections: {missed_count}")
    print(f"  False positives: {false_pos_count}")

    return diff_vis, loss_percentage


def validate_floodmap(csv_file: str, original_png: str):
    print(f"\n=== Validating: {os.path.basename(csv_file)} ===")

    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    generated_png = os.path.join(os.path.dirname(csv_file), f"{base_name}_generated.png")
    csv_to_png(csv_file, generated_png)

    diff_image, diff_percentage = calculate_difference(original_png, generated_png)

    diff_png = os.path.join(os.path.dirname(csv_file), f"{base_name}_diff.png")
    cv2.imwrite(diff_png, diff_image)

    print(f"Original PNG: {original_png}")
    print(f"Generated PNG: {generated_png}")
    print(f"Difference PNG: {diff_png}")
    print(f"Loss percentage: {diff_percentage:.2f}%")

    return diff_percentage


def main():
    csv_dir = os.path.join(SAFEMAP_DATA_DIR, "csv")
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

    total_loss = 0.0
    file_count = 0

    for csv_file in csv_files:
        csv_path = os.path.join(csv_dir, csv_file)

        base_name = os.path.splitext(csv_file)[0]
        original_png = os.path.join(SAFEMAP_DATA_DIR, f"{base_name}.png")

        if os.path.exists(original_png):
            loss_pct = validate_floodmap(csv_path, original_png)
            total_loss += loss_pct
            file_count += 1
        else:
            print(f"Warning: Original PNG not found for {csv_file}")

    if file_count > 0:
        avg_loss = total_loss / file_count
        print(f"\n=== Summary ===")
        print(f"Validated {file_count} flood maps")
        print(f"Average loss percentage: {avg_loss:.2f}%")
    else:
        print("No matching PNG files found for validation.")


if __name__ == "__main__":
    main()