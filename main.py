from KMA_data import get_data, endpoints
import time
import os

def download_all():
    timestamp = time.strftime("%m%d%H%M%S")
    out_dir = os.path.join(os.getcwd(), "weather_data", timestamp)

    for ep in endpoints:
        get_data(ep, out_dir)

if __name__ == "__main__":
    download_all()