from KMA_API import get_data, get_all_data
from NASA_FIRMS_API import get_firms_data
from csv_reader import load_grid, load_fire_grid
from visualizer import map_grid, fire_grid

"""
1. get_data : 특정 정보 받아오기(KMA_API.py의 endpoints참조). out dir 지정 필요

    get_data(1, out_dir="weather_data")

2. get_all_data : 해당 시간의 모든 정보 받아오기. timestamp 디렉토리 자동으로 만든 후 저장

    get_all_data()
    
3. NASA FIRMS API 로 화재 데이터 받아오기

    get_firms_data()
    
4. grid 지도, fire 지도 그리기 (map_data에 .html로 저장)

    map_grid()
    fire_grid()

"""


if __name__ == "__main__":
    grid = load_grid()
    fire_map = load_fire_grid()

    get_all_data()
    get_data(endpoint=1, out_dir="weather_data")

    get_firms_data()

    map_grid()
    fire_grid()