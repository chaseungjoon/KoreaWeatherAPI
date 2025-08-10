import io
import os
import pandas as pd
import time
import requests

MAP_KEY = os.getenv("NASA_FIRMS_MAP_KEY")
kor_url = 'https://firms.modaps.eosdis.nasa.gov/api/country/csv/' + MAP_KEY + '/MODIS_NRT/KOR/3'

def get_firms_data():
    try:
        response = requests.get(kor_url)
        csv_data = io.StringIO(response.text)
        df_kor = pd.read_csv(csv_data)
        timestamp = time.strftime("%m%d%H%M%S")
        save_path = "fire_data/fire_data_" + timestamp + ".csv"

        if not df_kor.empty:
            time_str = df_kor['acq_time'].astype(str).str.zfill(4)
            datetime_str = df_kor['acq_date'] + ' ' + time_str
            utc_time = pd.to_datetime(datetime_str, format='%Y-%m-%d %H%M').dt.tz_localize('UTC')
            kst_time = utc_time.dt.tz_convert('Asia/Seoul')

            df_kor['acq_date'] = kst_time.dt.strftime('%Y-%m-%d')
            df_kor['acq_time'] = kst_time.dt.strftime('%H%M')

            df_kor.to_csv(save_path, index=False)
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    get_firms_data()