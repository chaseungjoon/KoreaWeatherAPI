import requests
from config import KFS_REALTIME_URL

def get_kfs_fire_data():
    response = requests.get(KFS_REALTIME_URL)
    data = response.json()

    return data


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