import os

""" tokens """
KMA_WEATHER_TOKEN = os.getenv("KMA_WEATHER_TOKEN")
NASA_FIRMS_MAP_KEY = os.getenv("NASA_FIRMS_MAP_KEY")
SAFEMAP_API_KEY = os.getenv("SAFEMAP_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
KFS_LANDSLIDE_KEY = os.getenv("KFS_LANDSLIDE_KEY")

""" directories """
DOWNLOAD_DEFAULT_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRE_DATA_DIR = os.path.join(PROJECT_ROOT_DIR, "firms_data")
MAP_DATA_DIR = os.path.join(PROJECT_ROOT_DIR, "map_data")
WEATHER_DATA_DIR = os.path.join(PROJECT_ROOT_DIR, "kma_data")
SATELLITE_DATA_DIR = os.path.join(PROJECT_ROOT_DIR, "GK2A_data")
KFS_DATA_DIR = os.path.join(PROJECT_ROOT_DIR, "kfs_data")
SAFEMAP_DATA_DIR = os.path.join(PROJECT_ROOT_DIR, "safemap_data")

""" files """
GRID_PATH = os.path.join(MAP_DATA_DIR, "grid.csv")

""" kma api """
KMA_AWS_BASE_URL = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min"
KMA_ENDPOINTS = {
        1: {"url": KMA_AWS_BASE_URL + f"?authKey={KMA_WEATHER_TOKEN}", "filename": "AWS", "filetype": "csv", "desc" : "AWS 매분자료"},
        2: {"url": KMA_AWS_BASE_URL + f"_cloud?authKey={KMA_WEATHER_TOKEN}", "filename": "AWS_cloud", "filetype":"csv", "desc": "AWS 운고운량"},
        3: {"url": KMA_AWS_BASE_URL + f"_lst?authKey={KMA_WEATHER_TOKEN}", "filename": "AWS_temp", "filetype":"csv", "desc": "AWS 초상온도"},
        4: {"url": KMA_AWS_BASE_URL + f"_vis?authKey={KMA_WEATHER_TOKEN}", "filename": "AWS_vis", "filetype":"csv", "desc": "AWS 가시거리"},
}
KMA_SATELLITE_BASE_URL = "https://apihub.kma.go.kr/api/typ05/api/GK2A/LE2/FF/KO/data?date="

"""kfs api"""
KFS_REALTIME_URL = "https://fd.forest.go.kr/ffas/pubConn/selectPublicFireShowList.do"
KFS_LANDSLIDE_URL = f"https://www.safetydata.go.kr/V2/api/DSSP-IF-00735?serviceKey={KFS_LANDSLIDE_KEY}"

""" safemap api"""
SAFEMAP_BASE_URL = "http://www.safemap.go.kr/openApiService/wms/getLayerData.do"

""" nasa firms api """
NASA_FIRMS_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"+NASA_FIRMS_MAP_KEY+"/VIIRS_NOAA20_NRT/124.5,33.0,131.0,39.5"

""" Korea administrative address to lat/lon reference"""
korea_administrative_divisions = {
    # 서울특별시 (25개 자치구)
    "서울특별시 종로구": {"lat": None, "lon": None},
    "서울특별시 중구": {"lat": None, "lon": None},
    "서울특별시 용산구": {"lat": None, "lon": None},
    "서울특별시 성동구": {"lat": None, "lon": None},
    "서울특별시 광진구": {"lat": None, "lon": None},
    "서울특별시 동대문구": {"lat": None, "lon": None},
    "서울특별시 중랑구": {"lat": None, "lon": None},
    "서울특별시 성북구": {"lat": None, "lon": None},
    "서울특별시 강북구": {"lat": None, "lon": None},
    "서울특별시 도봉구": {"lat": None, "lon": None},
    "서울특별시 노원구": {"lat": None, "lon": None},
    "서울특별시 은평구": {"lat": None, "lon": None},
    "서울특별시 서대문구": {"lat": None, "lon": None},
    "서울특별시 마포구": {"lat": None, "lon": None},
    "서울특별시 양천구": {"lat": None, "lon": None},
    "서울특별시 강서구": {"lat": None, "lon": None},
    "서울특별시 구로구": {"lat": None, "lon": None},
    "서울특별시 금천구": {"lat": None, "lon": None},
    "서울특별시 영등포구": {"lat": None, "lon": None},
    "서울특별시 동작구": {"lat": None, "lon": None},
    "서울특별시 관악구": {"lat": None, "lon": None},
    "서울특별시 서초구": {"lat": None, "lon": None},
    "서울특별시 강남구": {"lat": None, "lon": None},
    "서울특별시 송파구": {"lat": None, "lon": None},
    "서울특별시 강동구": {"lat": None, "lon": None},

    # 부산광역시 (15개 자치구 + 1개 군)
    "부산광역시 중구": {"lat": None, "lon": None},
    "부산광역시 서구": {"lat": None, "lon": None},
    "부산광역시 동구": {"lat": None, "lon": None},
    "부산광역시 영도구": {"lat": None, "lon": None},
    "부산광역시 부산진구": {"lat": None, "lon": None},
    "부산광역시 동래구": {"lat": None, "lon": None},
    "부산광역시 남구": {"lat": None, "lon": None},
    "부산광역시 북구": {"lat": None, "lon": None},
    "부산광역시 강서구": {"lat": None, "lon": None},
    "부산광역시 해운대구": {"lat": None, "lon": None},
    "부산광역시 사하구": {"lat": None, "lon": None},
    "부산광역시 금정구": {"lat": None, "lon": None},
    "부산광역시 연제구": {"lat": None, "lon": None},
    "부산광역시 수영구": {"lat": None, "lon": None},
    "부산광역시 사상구": {"lat": None, "lon": None},
    "부산광역시 기장군": {"lat": None, "lon": None},

    # 대구광역시 (7개 자치구 + 2개 군)
    "대구광역시 중구": {"lat": None, "lon": None},
    "대구광역시 동구": {"lat": None, "lon": None},
    "대구광역시 서구": {"lat": None, "lon": None},
    "대구광역시 남구": {"lat": None, "lon": None},
    "대구광역시 북구": {"lat": None, "lon": None},
    "대구광역시 수성구": {"lat": None, "lon": None},
    "대구광역시 달서구": {"lat": None, "lon": None},
    "대구광역시 달성군": {"lat": None, "lon": None},
    "대구광역시 군위군": {"lat": None, "lon": None},

    # 인천광역시 (8개 자치구 + 2개 군)
    "인천광역시 중구": {"lat": None, "lon": None},
    "인천광역시 동구": {"lat": None, "lon": None},
    "인천광역시 미추홀구": {"lat": None, "lon": None},
    "인천광역시 연수구": {"lat": None, "lon": None},
    "인천광역시 남동구": {"lat": None, "lon": None},
    "인천광역시 부평구": {"lat": None, "lon": None},
    "인천광역시 계양구": {"lat": None, "lon": None},
    "인천광역시 서구": {"lat": None, "lon": None},
    "인천광역시 강화군": {"lat": None, "lon": None},
    "인천광역시 옹진군": {"lat": None, "lon": None},

    # 광주광역시 (5개 자치구)
    "광주광역시 동구": {"lat": None, "lon": None},
    "광주광역시 서구": {"lat": None, "lon": None},
    "광주광역시 남구": {"lat": None, "lon": None},
    "광주광역시 북구": {"lat": None, "lon": None},
    "광주광역시 광산구": {"lat": None, "lon": None},

    # 대전광역시 (5개 자치구)
    "대전광역시 중구": {"lat": None, "lon": None},
    "대전광역시 동구": {"lat": None, "lon": None},
    "대전광역시 서구": {"lat": None, "lon": None},
    "대전광역시 유성구": {"lat": None, "lon": None},
    "대전광역시 대덕구": {"lat": None, "lon": None},

    # 울산광역시 (4개 자치구 + 1개 군)
    "울산광역시 중구": {"lat": None, "lon": None},
    "울산광역시 남구": {"lat": None, "lon": None},
    "울산광역시 동구": {"lat": None, "lon": None},
    "울산광역시 북구": {"lat": None, "lon": None},
    "울산광역시 울주군": {"lat": None, "lon": None},

    # 세종특별자치시
    "세종특별자치시": {"lat": None, "lon": None},

    # 경기도 (28개 시 + 3개 군)
    "경기도 수원시": {"lat": None, "lon": None},
    "경기도 수원시 장안구": {"lat": None, "lon": None},
    "경기도 수원시 권선구": {"lat": None, "lon": None},
    "경기도 수원시 팔달구": {"lat": None, "lon": None},
    "경기도 수원시 영통구": {"lat": None, "lon": None},
    "경기도 성남시": {"lat": None, "lon": None},
    "경기도 성남시 수정구": {"lat": None, "lon": None},
    "경기도 성남시 중원구": {"lat": None, "lon": None},
    "경기도 성남시 분당구": {"lat": None, "lon": None},
    "경기도 의정부시": {"lat": None, "lon": None},
    "경기도 안양시": {"lat": None, "lon": None},
    "경기도 안양시 만안구": {"lat": None, "lon": None},
    "경기도 안양시 동안구": {"lat": None, "lon": None},
    "경기도 부천시": {"lat": None, "lon": None},
    "경기도 부천시 원미구": {"lat": None, "lon": None},
    "경기도 부천시 소사구": {"lat": None, "lon": None},
    "경기도 부천시 오정구": {"lat": None, "lon": None},
    "경기도 광명시": {"lat": None, "lon": None},
    "경기도 동두천시": {"lat": None, "lon": None},
    "경기도 평택시": {"lat": None, "lon": None},
    "경기도 안산시": {"lat": None, "lon": None},
    "경기도 안산시 상록구": {"lat": None, "lon": None},
    "경기도 안산시 단원구": {"lat": None, "lon": None},
    "경기도 고양시": {"lat": None, "lon": None},
    "경기도 고양시 덕양구": {"lat": None, "lon": None},
    "경기도 고양시 일산동구": {"lat": None, "lon": None},
    "경기도 고양시 일산서구": {"lat": None, "lon": None},
    "경기도 과천시": {"lat": None, "lon": None},
    "경기도 구리시": {"lat": None, "lon": None},
    "경기도 남양주시": {"lat": None, "lon": None},
    "경기도 오산시": {"lat": None, "lon": None},
    "경기도 시흥시": {"lat": None, "lon": None},
    "경기도 군포시": {"lat": None, "lon": None},
    "경기도 의왕시": {"lat": None, "lon": None},
    "경기도 하남시": {"lat": None, "lon": None},
    "경기도 용인시": {"lat": None, "lon": None},
    "경기도 용인시 처인구": {"lat": None, "lon": None},
    "경기도 용인시 기흥구": {"lat": None, "lon": None},
    "경기도 용인시 수지구": {"lat": None, "lon": None},
    "경기도 파주시": {"lat": None, "lon": None},
    "경기도 이천시": {"lat": None, "lon": None},
    "경기도 안성시": {"lat": None, "lon": None},
    "경기도 김포시": {"lat": None, "lon": None},
    "경기도 화성시": {"lat": None, "lon": None},
    "경기도 광주시": {"lat": None, "lon": None},
    "경기도 양주시": {"lat": None, "lon": None},
    "경기도 포천시": {"lat": None, "lon": None},
    "경기도 여주시": {"lat": None, "lon": None},
    "경기도 연천군": {"lat": None, "lon": None},
    "경기도 가평군": {"lat": None, "lon": None},
    "경기도 양평군": {"lat": None, "lon": None},

    # 충청북도 (3개 시 + 8개 군)
    "충청북도 청주시": {"lat": None, "lon": None},
    "충청북도 청주시 상당구": {"lat": None, "lon": None},
    "충청북도 청주시 흥덕구": {"lat": None, "lon": None},
    "충청북도 청주시 서원구": {"lat": None, "lon": None},
    "충청북도 청주시 청원구": {"lat": None, "lon": None},
    "충청북도 충주시": {"lat": None, "lon": None},
    "충청북도 제천시": {"lat": None, "lon": None},
    "충청북도 보은군": {"lat": None, "lon": None},
    "충청북도 옥천군": {"lat": None, "lon": None},
    "충청북도 영동군": {"lat": None, "lon": None},
    "충청북도 증평군": {"lat": None, "lon": None},
    "충청북도 진천군": {"lat": None, "lon": None},
    "충청북도 괴산군": {"lat": None, "lon": None},
    "충청북도 음성군": {"lat": None, "lon": None},
    "충청북도 단양군": {"lat": None, "lon": None},

    # 충청남도 (8개 시 + 7개 군)
    "충청남도 천안시": {"lat": None, "lon": None},
    "충청남도 천안시 동남구": {"lat": None, "lon": None},
    "충청남도 천안시 서북구": {"lat": None, "lon": None},
    "충청남도 공주시": {"lat": None, "lon": None},
    "충청남도 보령시": {"lat": None, "lon": None},
    "충청남도 아산시": {"lat": None, "lon": None},
    "충청남도 서산시": {"lat": None, "lon": None},
    "충청남도 논산시": {"lat": None, "lon": None},
    "충청남도 계룡시": {"lat": None, "lon": None},
    "충청남도 당진시": {"lat": None, "lon": None},
    "충청남도 금산군": {"lat": None, "lon": None},
    "충청남도 부여군": {"lat": None, "lon": None},
    "충청남도 서천군": {"lat": None, "lon": None},
    "충청남도 청양군": {"lat": None, "lon": None},
    "충청남도 홍성군": {"lat": None, "lon": None},
    "충청남도 예산군": {"lat": None, "lon": None},
    "충청남도 태안군": {"lat": None, "lon": None},

    # 전라남도 (5개 시 + 17개 군)
    "전라남도 목포시": {"lat": None, "lon": None},
    "전라남도 여수시": {"lat": None, "lon": None},
    "전라남도 순천시": {"lat": None, "lon": None},
    "전라남도 나주시": {"lat": None, "lon": None},
    "전라남도 광양시": {"lat": None, "lon": None},
    "전라남도 담양군": {"lat": None, "lon": None},
    "전라남도 곡성군": {"lat": None, "lon": None},
    "전라남도 구례군": {"lat": None, "lon": None},
    "전라남도 고흥군": {"lat": None, "lon": None},
    "전라남도 보성군": {"lat": None, "lon": None},
    "전라남도 화순군": {"lat": None, "lon": None},
    "전라남도 장흥군": {"lat": None, "lon": None},
    "전라남도 강진군": {"lat": None, "lon": None},
    "전라남도 해남군": {"lat": None, "lon": None},
    "전라남도 영암군": {"lat": None, "lon": None},
    "전라남도 무안군": {"lat": None, "lon": None},
    "전라남도 함평군": {"lat": None, "lon": None},
    "전라남도 영광군": {"lat": None, "lon": None},
    "전라남도 장성군": {"lat": None, "lon": None},
    "전라남도 완도군": {"lat": None, "lon": None},
    "전라남도 진도군": {"lat": None, "lon": None},
    "전라남도 신안군": {"lat": None, "lon": None},

    # 경상북도 (10개 시 + 12개 군)
    "경상북도 포항시": {"lat": None, "lon": None},
    "경상북도 포항시 남구": {"lat": None, "lon": None},
    "경상북도 포항시 북구": {"lat": None, "lon": None},
    "경상북도 경주시": {"lat": None, "lon": None},
    "경상북도 김천시": {"lat": None, "lon": None},
    "경상북도 안동시": {"lat": None, "lon": None},
    "경상북도 구미시": {"lat": None, "lon": None},
    "경상북도 영주시": {"lat": None, "lon": None},
    "경상북도 영천시": {"lat": None, "lon": None},
    "경상북도 상주시": {"lat": None, "lon": None},
    "경상북도 문경시": {"lat": None, "lon": None},
    "경상북도 경산시": {"lat": None, "lon": None},
    "경상북도 의성군": {"lat": None, "lon": None},
    "경상북도 청송군": {"lat": None, "lon": None},
    "경상북도 영양군": {"lat": None, "lon": None},
    "경상북도 영덕군": {"lat": None, "lon": None},
    "경상북도 청도군": {"lat": None, "lon": None},
    "경상북도 고령군": {"lat": None, "lon": None},
    "경상북도 성주군": {"lat": None, "lon": None},
    "경상북도 칠곡군": {"lat": None, "lon": None},
    "경상북도 예천군": {"lat": None, "lon": None},
    "경상북도 봉화군": {"lat": None, "lon": None},
    "경상북도 울진군": {"lat": None, "lon": None},
    "경상북도 울릉군": {"lat": None, "lon": None},

    # 경상남도 (8개 시 + 10개 군)
    "경상남도 창원시": {"lat": None, "lon": None},
    "경상남도 창원시 마산회원구": {"lat": None, "lon": None},
    "경상남도 창원시 마산합포구": {"lat": None, "lon": None},
    "경상남도 창원시 성산구": {"lat": None, "lon": None},
    "경상남도 창원시 의창구": {"lat": None, "lon": None},
    "경상남도 창원시 진해구": {"lat": None, "lon": None},
    "경상남도 진주시": {"lat": None, "lon": None},
    "경상남도 통영시": {"lat": None, "lon": None},
    "경상남도 사천시": {"lat": None, "lon": None},
    "경상남도 김해시": {"lat": None, "lon": None},
    "경상남도 밀양시": {"lat": None, "lon": None},
    "경상남도 거제시": {"lat": None, "lon": None},
    "경상남도 양산시": {"lat": None, "lon": None},
    "경상남도 의령군": {"lat": None, "lon": None},
    "경상남도 함안군": {"lat": None, "lon": None},
    "경상남도 창녕군": {"lat": None, "lon": None},
    "경상남도 고성군": {"lat": None, "lon": None},
    "경상남도 남해군": {"lat": None, "lon": None},
    "경상남도 하동군": {"lat": None, "lon": None},
    "경상남도 산청군": {"lat": None, "lon": None},
    "경상남도 함양군": {"lat": None, "lon": None},
    "경상남도 거창군": {"lat": None, "lon": None},
    "경상남도 합천군": {"lat": None, "lon": None},

    # 강원특별자치도 (7개 시 + 11개 군)
    "강원특별자치도 춘천시": {"lat": None, "lon": None},
    "강원특별자치도 원주시": {"lat": None, "lon": None},
    "강원특별자치도 강릉시": {"lat": None, "lon": None},
    "강원특별자치도 동해시": {"lat": None, "lon": None},
    "강원특별자치도 태백시": {"lat": None, "lon": None},
    "강원특별자치도 속초시": {"lat": None, "lon": None},
    "강원특별자치도 삼척시": {"lat": None, "lon": None},
    "강원특별자치도 홍천군": {"lat": None, "lon": None},
    "강원특별자치도 횡성군": {"lat": None, "lon": None},
    "강원특별자치도 영월군": {"lat": None, "lon": None},
    "강원특별자치도 평창군": {"lat": None, "lon": None},
    "강원특별자치도 정선군": {"lat": None, "lon": None},
    "강원특별자치도 철원군": {"lat": None, "lon": None},
    "강원특별자치도 화천군": {"lat": None, "lon": None},
    "강원특별자치도 양구군": {"lat": None, "lon": None},
    "강원특별자치도 인제군": {"lat": None, "lon": None},
    "강원특별자치도 고성군": {"lat": None, "lon": None},
    "강원특별자치도 양양군": {"lat": None, "lon": None},

    # 전북특별자치도 (6개 시 + 8개 군)
    "전북특별자치도 전주시": {"lat": None, "lon": None},
    "전북특별자치도 전주시 완산구": {"lat": None, "lon": None},
    "전북특별자치도 전주시 덕진구": {"lat": None, "lon": None},
    "전북특별자치도 군산시": {"lat": None, "lon": None},
    "전북특별자치도 익산시": {"lat": None, "lon": None},
    "전북특별자치도 정읍시": {"lat": None, "lon": None},
    "전북특별자치도 남원시": {"lat": None, "lon": None},
    "전북특별자치도 김제시": {"lat": None, "lon": None},
    "전북특별자치도 진안군": {"lat": None, "lon": None},
    "전북특별자치도 완주군": {"lat": None, "lon": None},
    "전북특별자치도 무주군": {"lat": None, "lon": None},
    "전북특별자치도 장수군": {"lat": None, "lon": None},
    "전북특별자치도 임실군": {"lat": None, "lon": None},
    "전북특별자치도 순창군": {"lat": None, "lon": None},
    "전북특별자치도 고창군": {"lat": None, "lon": None},
    "전북특별자치도 부안군": {"lat": None, "lon": None},

    # 제주특별자치도 (2개 행정시)
    "제주특별자치도 제주시": {"lat": None, "lon": None},
    "제주특별자치도 서귀포시": {"lat": None, "lon": None}
}