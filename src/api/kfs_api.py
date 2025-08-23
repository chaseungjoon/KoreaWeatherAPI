import requests
from src.config import KFS_REALTIME_URL, KFS_DATA_DIR
import csv
import os
from datetime import datetime

""" 실제 응답

{
  "fireShowInfoList": [
    {
      "frfrLctnXcrd": "127.67243000000057",
      "frfrPrgrsStcd": "02",
      "frfrOccrrTpcd": "05",
      "frfrStepIssuCd": "00",
      "frfrPotfrRt": 70,
      "frfrSttmnDt": "20250822",
      "frfrSttmnHms": "144122",
      "frfrInfoId": "398504",
      "frfrOccrrStcd": "31",
      "frfrLctnYcrd": "37.08104000024055",
      "frfrSttmnLctnXcrd": "127.67243000000029",
      "frfrSttmnLctnYcrd": "37.08104000012027",
      "frfrSttmnAddr": "충청북도 음성군 감곡면 영산리",
      "frfrPrgrsStcdNm": "진화중",
      "frfrSttmnAddrDe": "충청북도 음성군 감곡면 영산리 산55-3임",
      "frfrFrngDtm": "2025-08-22 14:41:22",
      "frfrStepIssuNm": "초기 대응",
      "lgdngCd": "4377037026"
    }
  ]
}
"""

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



""" MONITORING API CALL """
def test_kfs_api():
    response = requests.get(KFS_REALTIME_URL)
    data = response.json()
    print(data)

if __name__ == "__main__":
    test_kfs_api()