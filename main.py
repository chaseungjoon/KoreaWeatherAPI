from kma_api import get_weather_data, get_all_weather_data
from nasa_api import get_firms_data
from csv_reader import load_grid, load_fire_grid
from visualizer import draw_grid, draw_fire_grid
from config import *

"""
1. get_data : 특정 정보 받아오기(KMA_API.py의 endpoints참조). out dir 지정 필요

        get_weather_data(1, out_dir=WEATHER_DATA_DIR)

2. get_all_data : 해당 시간의 모든 정보 받아오기

    * weather_data 폴더에 timestamp 폴더 생성 후, 그 안에 .csv로 저장

        get_all_weather_data()
    
3. NASA FIRMS API 로 화재 데이터 받아오기

    * fire_data 폴더에 .csv로 저장

        get_firms_data()
    
4. 기상관측소 정보 (grid.csv), 화재 발생 정보 (fire_data_.csv) 

    * format : [ {data_0}, {data_1}, ..., {data_n} ]

        grid = load_grid()
        fire_grid = load_fire_grid()
    
4. csv파일을 읽어 grid 지도, fire 지도 그리기

    * map_data 폴더에 .html로 저장 

        draw_grid()
        draw_fire_grid()

"""

def fetch_recent():

    get_all_weather_data()
    get_firms_data()
    draw_fire_grid()

if __name__ == "__main__":

    fetch_recent()