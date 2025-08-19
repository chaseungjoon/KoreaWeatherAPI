import os

""" tokens """
KMA_WEATHER_TOKEN = os.getenv("KMA_WEATHER_TOKEN")
NASA_FIRMS_MAP_KEY = os.getenv("NASA_FIRMS_MAP_KEY")

""" directories """
DOWNLOAD_DEFAULT_DIR = "/Users/chaseungjun/Downloads"
ROOT_DIR = os.getcwd()
FIRE_DATA_DIR = os.path.join(ROOT_DIR, "firms_data")
MAP_DATA_DIR = os.path.join(ROOT_DIR, "map_data")
WEATHER_DATA_DIR = os.path.join(ROOT_DIR, "weather_data")
SATELLITE_DATA_DIR = os.path.join(ROOT_DIR, "GK2A_data")

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

""" nasa firms api """
NASA_FIRMS_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"+NASA_FIRMS_MAP_KEY+"/VIIRS_NOAA20_NRT/124.5,33.0,131.0,39.5"