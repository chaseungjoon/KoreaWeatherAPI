import requests
import os
from PIL import Image
from io import BytesIO
from src.config import SAFEMAP_BASE_URL, SAFEMAP_API_KEY, SAFEMAP_DATA_DIR

def get_safemap_flood_data(divisions):
    if divisions >10 or divisions <1:
        print("Divisions must be between 1 and 10")
        return

    minx, miny, maxx, maxy = 124, 33, 132, 39
    cols, rows = divisions, divisions
    tile_size = 4096

    dx = (maxx - minx) / cols
    dy = (maxy - miny) / rows

    tiles = [[None for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            bbox = [minx + col * dx, miny + row * dy, minx + (col + 1) * dx, miny + (row + 1) * dy]
            params = {
                "apikey": SAFEMAP_API_KEY,
                "layers": "A2SM_FLUDMARKS",
                "styles": "A2SM_FludMarks",
                "format": "image/png",
                "transparent": "true",
                "service": "WMS",
                "version": "1.1.1",
                "request": "GetMap",
                "srs": "EPSG:4326",
                "bbox": ",".join(map(str, bbox)),
                "width": tile_size,
                "height": tile_size
            }

            tile_num = row * cols + col + 1
            try:
                response = requests.get(SAFEMAP_BASE_URL, params=params)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content)).convert("RGBA")
                    tiles[row][col] = img

                    tile_path = os.path.join(SAFEMAP_DATA_DIR, f"safemap_flood_map{tile_num}.png")
                    img.save(tile_path)
                    print(f"Saved tile {tile_num}")
                else:
                    print(f"Tile {tile_num} failed: {response.status_code}")
                    return
            except Exception as e:
                print(f"Exception for tile {tile_num}: {e}")
                return

    merged_width = tile_size * cols
    merged_height = tile_size * rows
    final_img = Image.new("RGBA", (merged_width, merged_height))

    for row in range(rows):
        for col in range(cols):
            img = tiles[row][col]
            if img is not None:
                paste_y = (rows - 1 - row) * tile_size  # north at top
                final_img.paste(img, (col * tile_size, paste_y))

    final_path = os.path.join(SAFEMAP_DATA_DIR, f"flood_map(124,33,132,39)({divisions*4096}X{divisions*4096}).png")
    final_img.save(final_path)
    print(f"Saved final combined image: {final_path}")

    for tile_num in range(1, rows * cols + 1):
        tile_path = os.path.join(SAFEMAP_DATA_DIR, f"safemap_flood_map{tile_num}.png")
        if os.path.exists(tile_path):
            os.remove(tile_path)
            print(f"Deleted tile {tile_num}")

if __name__ == "__main__":
    get_safemap_flood_data(divisions=2)