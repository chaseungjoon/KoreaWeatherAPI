from KMA_API import get_data, get_all_data
from grid_data import load_grid

"""
1. get_data : 특정 정보 받아오기(KMA_API.py의 endpoints참조). out dir 지정 필요

    get_data(1, out_dir="weather_data")

2. get_all_data : 해당 시간의 모든 정보 받아오기. timestamp 디렉토리 자동으로 만든 후 저장

    get_all_data()

3. 기상청의 grid정보 dictionary로 저장

    grid = load_grid()

"""


if __name__ == "__main__":
    grid = load_grid()
    get_all_data()
    get_data(endpoint=1, out_dir="weather_data")