import re
import os
import sys
import glob
import csv
from src.config import SAFEMAP_DATA_DIR
from dataclasses import dataclass
from typing import Tuple, List
import cv2
import numpy as np

"""
55% Validation accuracy
"""

H_LO = 96
H_HI = 124
S_LO = 169
V_LO = 184

OPEN_KERNEL = 2
MIN_AREA_PIXELS = 4

@dataclass
class GeoBounds:
    lon_min: float
    lat_min: float
    lon_max: float
    lat_max: float

    def px_to_lonlat(self, x: float, y: float, W: int, H: int) -> Tuple[float, float]:
        lon = self.lon_min + ((x+0.5) / W) * (self.lon_max - self.lon_min)
        lat = self.lat_max - ((y+0.5) / H) * (self.lat_max - self.lat_min)
        return lon, lat

FNAME_RE = re.compile(
    r"flood_map\((?P<lon_min>-?\d+\.?\d*),(?P<lat_min>-?\d+\.?\d*),"
    r"(?P<lon_max>-?\d+\.?\d*),(?P<lat_max>-?\d+\.?\d*)\)\((?P<W>\d+)X(?P<H>\d+)\)",
    re.IGNORECASE
)

def parse_bounds_from_name(path:str) -> Tuple[GeoBounds, Tuple[int, int], str]:
    name = os.path.basename(path)
    m = FNAME_RE.search(name)
    if not m:
        raise ValueError(f"Filename does not match expected pattern: {name}")
    lon_min = float(m.group("lon_min"))
    lat_min = float(m.group("lat_min"))
    lon_max = float(m.group("lon_max"))
    lat_max = float(m.group("lat_max"))
    W = int(m.group("W"))
    H = int(m.group("H"))
    return GeoBounds(lon_min, lat_min, lon_max, lat_max), (W, H), os.path.splitext(name)[0]

def mask_flood_bgr(img_bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lo = np.array([H_LO, S_LO, V_LO], dtype=np.uint8)
    hi = np.array([H_HI, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lo, hi)

    if OPEN_KERNEL > 0:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (OPEN_KERNEL, OPEN_KERNEL))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k, iterations=1)
    return mask

def components(mask: np.ndarray) -> Tuple[int, np.ndarray, np.ndarray, np.ndarray]:
    return cv2.connectedComponentsWithStats(mask, connectivity=8, ltype=cv2.CV_32S)

def process_image(path: str, out_csv: str) -> int:
    gb, (W_decl, H_decl), map_name = parse_bounds_from_name(path)
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"Failed to read image: {path}")

    H, W = img.shape[:2]
    if (W, H) != (W_decl, H_decl):
        sys.stderr.write(
            f"[warn] Declared size ({W_decl}x{H_decl}) != actual ({W}x{H}) for {path}\n"
        )

    mask = mask_flood_bgr(img)
    num_labels, labels, stats, centroids = components(mask)

    total_area = float(W * H)
    rows: List[List] = []
    next_id = 0

    for label in range(1, num_labels):
        x, y, w, h, area = stats[label]
        if area < MIN_AREA_PIXELS:
            continue
        cx, cy = centroids[label]

        lon, lat = gb.px_to_lonlat(cx, cy, W, H)

        lon_min, lat_max = gb.px_to_lonlat(x, y, W, H)
        lon_max, lat_min = gb.px_to_lonlat(x + w - 1, y + h - 1, W, H)

        size_ratio = area / total_area

        rows.append([
            next_id,
            round(lat, 8), round(lon, 8),
            size_ratio,
            int(area),
            float(cx), float(cy),
            round(lat_min, 8), round(lon_min, 8),
            round(lat_max, 8), round(lon_max, 8),
            map_name
        ])
        next_id += 1

    header = [
        "id",
        "lat", "lon",
        "size",
        "pixel_area",
        "pixel_centroid_x", "pixel_centroid_y",
        "bbox_min_lat", "bbox_min_lon",
        "bbox_max_lat", "bbox_max_lon",
        "map_name",
    ]

    write_header = not os.path.exists(out_csv)
    with open(out_csv, "a", newline="", encoding="utf-8") as f:
        wri = csv.writer(f)
        if write_header:
            wri.writerow(header)
        wri.writerows(rows)

    return len(rows)

def main():
    out_csv_path = os.path.join(SAFEMAP_DATA_DIR, "csv")
    files = sorted(glob.glob(os.path.join(SAFEMAP_DATA_DIR, "*.png")))

    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]
        csv_file = os.path.join(out_csv_path, f"{base}.csv")
        n = process_image(f, csv_file)
        print(f"{f} -> {n} rows")

if __name__ == "__main__":
    main()