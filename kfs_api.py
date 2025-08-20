import requests
from config import KFS_REALTIME_URL, KFS_DATA_DIR
import csv
import os
from datetime import datetime

""" 예상 응답

{
  "fireShowInfoList": [
      {
        "frfrInfoId": "20250819001",            // 산불 고유 ID
        "frfrLctnXcrd": "127.0456",             // 경도 (lon)
        "frfrLctnYcrd": "37.5123",              // 위도 (lat)
        "frfrSttmnAddr": "경기도 수원시 팔달구",     // 발생지 주소
        "frfrFrngDtm": "2025-08-19 14:32:00",   // 발생 일시
        "potfrCmpleDtm": null,                  // 진화 완료 일시, 없으면 null
        "frfrPrgrsStcd": "02",                  // 진행 상태 코드
        "frfrPrgrsStcdNm": "진화중",              // 진행 상태명
        "frfrStepIssuCd": "02",                 // 대응 단계 코드 (00~03, 99)
        "frfrStepIssuNm": "산불2단계",            // 대응 단계명
        "frfrPotfrRt": 45                       // 진화율 (%)
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

    """ DUMMY DATA! DELETE AFTER VALIDATION OF API"""
    print(data)
    data = {
        "fireShowInfoList": [
          {
            "frfrInfoId": "20250819001",
            "frfrLctnXcrd": "127.0456",
            "frfrLctnYcrd": "37.5123",
            "frfrSttmnAddr": "경기도 수원시 팔달구",
            "frfrFrngDtm": "2025-08-19 14:32:00",
            "potfrCmpleDtm": "null",
            "frfrPrgrsStcd": "02",
            "frfrPrgrsStcdNm": "진화중",
            "frfrStepIssuCd": "02",
            "frfrStepIssuNm": "산불2단계",
            "frfrPotfrRt": 45
          },
            {
                "frfrInfoId": "20250819002",
                "frfrLctnXcrd": "128.0456",
                "frfrLctnYcrd": "37.5123",
                "frfrSttmnAddr": "경기도 성남시",
                "frfrFrngDtm": "2025-08-19 16:39:04",
                "potfrCmpleDtm": "null",
                "frfrPrgrsStcd": "02",
                "frfrPrgrsStcdNm": "진화중",
                "frfrStepIssuCd": "02",
                "frfrStepIssuNm": "산불2단계",
                "frfrPotfrRt": 66
            },
            {
                "frfrInfoId": "20250819002",
                "frfrLctnXcrd": "127.0956",
                "frfrLctnYcrd": "37.4723",
                "frfrSttmnAddr": "경기도 성남시",
                "frfrFrngDtm": "2025-08-19 16:39:04",
                "potfrCmpleDtm": "2025-08-19 16:50:57",
                "frfrPrgrsStcd": "99",
                "frfrPrgrsStcdNm": "진화완료",
                "frfrStepIssuCd": "01",
                "frfrStepIssuNm": "산불1단계",
                "frfrPotfrRt": 100
            }
        ]
    }

    data_list = data.get("fireShowInfoList")

    if not data_list:
        print("No KFS fire data found in the response.")
        return

    for fire_event in data_list:
        start_date_str = fire_event["frfrFrngDtm"]
        end_date_str = fire_event["potfrCmpleDtm"]

        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
        fire_event["frfrFrngDtm"] = start_date_obj.strftime("%Y%m%d%H%M%S")

        if end_date_str.lower() != "null":
            end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
            fire_event["potfrCmpleDtm"] = end_date_obj.strftime("%Y%m%d%H%M%S")

    timestamp = datetime.now().strftime("%m%d%H%M")
    filepath = os.path.join(KFS_DATA_DIR, f"{timestamp}.csv")

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_list[0].keys())
            writer.writeheader()
            writer.writerows(data_list)
    except (IOError, IndexError) as e:
        print(e)
