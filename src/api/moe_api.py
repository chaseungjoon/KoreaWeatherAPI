from datetime import datetime, timedelta
import os
import requests
import csv
from src.config import MOE_FLOOD_URL, MOE_DATA_DIR

def get_flood_data():
    """
    - 현재 시간을 가장 가까운 10분 단위로 반올림
    - wl 필드가 하나라도 비어있으면 10분 전 데이터로 재요청
    """
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

if __name__ == "__main__":
    get_flood_data()