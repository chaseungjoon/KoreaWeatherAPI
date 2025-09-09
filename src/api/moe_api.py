from datetime import datetime, timedelta
import os
import requests
import csv
from src.config import MOE_FLOOD_URL, MOE_DATA_DIR

def get_flood_data():
    rounded_time = datetime.now().replace(second=0, microsecond=0)
    rounded_time = rounded_time.replace(minute=(rounded_time.minute // 10) * 10)
    while True:
        url = MOE_FLOOD_URL + rounded_time.strftime("%Y%m%d%H%M")
        try:
            response = requests.post(url)
            data = response.json()
        except Exception as e:
            print(e)
            return

        if data[0]['wl'] != '-':
            break
        else:
            rounded_time -= timedelta(minutes=10)

    csv_path = os.path.join(MOE_DATA_DIR, f"{rounded_time.strftime('%Y%m%d%H%M')}.csv")
    if data:
        fieldnames = list(data[0].keys())
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow(entry)
    else:
        print("No data")

""" MONITORING API CALL """
def test_flood_api():
    rounded_time = datetime.now().replace(second=0, microsecond=0)
    rounded_time = rounded_time.replace(minute=(rounded_time.minute // 10) * 10)
    rounded_time -= timedelta(minutes=20)
    url = MOE_FLOOD_URL + rounded_time.strftime("%Y%m%d%H%M")
    response = requests.get(url)
    data = response.json()
    print(data[0])

if __name__ == "__main__":
    test_flood_api()