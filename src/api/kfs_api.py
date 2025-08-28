import requests
from src.config import KFS_REALTIME_URL, KFS_DATA_DIR, KFS_LANDSLIDE_URL
import csv
import os
import json
from datetime import datetime, timedelta

def get_kfs_fire_data():
    try:
        response = requests.get(KFS_REALTIME_URL)
        data = response.json()
    except Exception as e:
        print(e)
        return

    data_list = data.get("fireShowInfoList")
    if not data_list:
        print("No KFS fire data found in the response.")
        return

    for fire_event in data_list:
        start_date_str = fire_event["frfrFrngDtm"]
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
        fire_event["frfrFrngDtm"] = start_date_obj.strftime("%Y%m%d%H%M%S")

    timestamp = datetime.now().strftime("%m%d%H%M")
    filepath = os.path.join(KFS_DATA_DIR, f"{timestamp}.csv")

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_list[0].keys())
            writer.writeheader()
            writer.writerows(data_list)
    except (IOError, IndexError) as e:
        print(e)


def get_kfs_landslide_data():
    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        response = requests.get(KFS_LANDSLIDE_URL + "&returnType=json&numOfRows=10000&inqDt=" + yesterday)
        data = response.json()
    except Exception as e:
        print(e)
        return

    totalCount = data.get("totalCount")
    numOfRows = data.get("numOfRows")
    body = data.get("body")
    if totalCount == 0:
        print("No KFS landslide data")
        return
    if totalCount > numOfRows:
        for page in range(2, (totalCount // numOfRows) + 2):
            try:
                response = requests.get(KFS_LANDSLIDE_URL + f"&returnType=json&numOfRows={numOfRows}&pageNo={page}&inqDt=" + yesterday)
                more_data = response.json()
                if more_data.get("body"):
                    body.extend(more_data.get("body", []))
            except Exception as e:
                print(e)
                continue

    for row in body:
        dt_str = row["PREDC_ANLS_DT"]
        dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        row["PREDC_ANLS_DT"] = dt_obj.strftime("%Y%m%d%H%M%S")

    filepath = os.path.join(KFS_DATA_DIR, "landslide", f"{yesterday[4:]}.csv")
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=body[0].keys())
            writer.writeheader()
            writer.writerows(body)
    except (IOError, IndexError) as e:
        print(e)

""" MONITORING API CALL """
def test_kfs_api():
    print("--------KFS FIRE DATA--------")
    response = requests.get(KFS_REALTIME_URL)
    data = response.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))

    print("\n\n--------KFS LANDSLIDE DATA--------")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    response2 = requests.get(KFS_LANDSLIDE_URL + "&returnType=json&numOfRows=10000&inqDt=" + yesterday)
    data2 = response2.json()
    print(json.dumps(data2, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    test_kfs_api()