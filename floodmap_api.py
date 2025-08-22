import requests
import os
from config import SAFEMAP_API_KEY, SAFEMAP_FLOOD_LAYER_URL, FLOOD_DATA_DIR


def get_flood_layer_map():
    base_url = SAFEMAP_FLOOD_LAYER_URL
    params = {
        "service": "WMS",
        "version": "1.1.1",
        "request": "GetMap",
        "apikey": SAFEMAP_API_KEY,
        "layers": "A2SM_FLUDMARKS",
        "styles": "A2SM_FludMarks",
        "format": "image/png",
        "transparent": "true",
        "exceptions": "text/xml",
        "srs": "EPSG:4326",
        "bbox": "126.8,37.4,127.2,37.6",
        "width": 800,
        "height": 600
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(response.status_code)
            return
    except Exception as e:
        print(e)
        return

    with open(os.path.join(FLOOD_DATA_DIR, "flood_map.png"), "wb") as f:
        f.write(response.content)

if __name__ == "__main__":
    get_flood_layer_map()