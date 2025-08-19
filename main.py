from kma_api import get_weather_data, get_all_weather_data, get_GK2A_fire_data
from nasa_api import get_firms_data
from csv_reader import load_grid, load_nasa_fire_grid, load_GK2A_fire_grid
from visualizer import draw_nasa_fire_grid, draw_GK2A_fire_grid

"""
1. 최신 날씨정보 받아오기 (특정 Endpoint 정보)

    * 1분 단위 업데이트
    * 5~7분 딜레이
    * 첫 번째 parameter : Endpoint 지정 (config.py의 KMA_ENDPOINTS참조)
    * 두 번째 parameter : output dir 

        get_weather_data(1, out_dir=WEATHER_DATA_DIR)

2. 최신 날씨정보 받아오기 (모든 정보)
    
    * 1분 단위 업데이트
    * 5~7분 딜레이
    * weather_data 폴더에 timestamp 폴더 생성 후, 그 안에 Endpoint 종류별로 .csv로 저장

        get_all_weather_data()

3. 최신 화재 데이터 받아오기
    
    * 12시간 단위 업데이트
    * Optional parameter : 지난 n일간의 화재 데이터 (default=3)
    * firms_data 폴더에 .csv로 저장

        get_firms_data()    # 지난 3일간의 화재 데이터
        get_firms_data(5)   # 지난 5일간의 화재 데이터
        
    * 2분 단위 업데이트
    * 10시간 딜레이
    
        get_GK2A_fire_data()   # 천리안2호 위성 화재 데이터 .csv로 저장
    
4. 기상관측소 위치 정보, 화재 발생 위치 정보 로드하기

    * format : [ {data_0}, {data_1}, ..., {data_n} ] (dicts inside an array)

        grid = load_grid()
        nasa_fire_grid = load_nasa_fire_grid()
        GK2A_fire_grid = load_GK2A_fire_grid()
    
4. csv파일을 읽어 grid 지도, fire 지도 그리기

    * map_data 폴더에 .html로 저장 

        draw_grid()
        draw_nasa_fire_grid()
        draw_GK2A_fire_grid()

"""

def fetch_recent():
    get_all_weather_data()

    get_firms_data()
    draw_nasa_fire_grid()

    get_GK2A_fire_data()
    draw_GK2A_fire_grid()

if __name__ == "__main__":

    """ Fetch most recent data"""
    fetch_recent()



    """ Load weather grid"""
    grid = load_grid()

    """ Load nasa fire position grid"""
    nasa_fire_grid = load_nasa_fire_grid()

    """ Load GK2A fire position grid"""
    GK2A_fire_grid = load_GK2A_fire_grid()

