import csv
import requests
import time
import argparse
import pandas as pd
import numpy as np
import netCDF4 as nc
from pyproj import Proj
from datetime import datetime, timedelta
from config import *

np.seterr(invalid="ignore", divide="ignore")


def get_weather_data(endpoint, out_dir):
    if endpoint not in KMA_ENDPOINTS:
        print("Wrong choice")
        return

    url = KMA_ENDPOINTS[endpoint]["url"]
    filename = KMA_ENDPOINTS[endpoint]["filename"]
    filetype = KMA_ENDPOINTS[endpoint]["filetype"]

    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        return

    timestamp = time.strftime("%m%d%H%M%S")
    os.makedirs(out_dir, exist_ok=True)

    temp_path = os.path.join(out_dir,f"{filename}.{filetype}")
    save_path = os.path.join(out_dir, f"{filename}_{timestamp}.{filetype}")

    if filetype == "csv":
        response.encoding = 'euc-kr'
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(response.text)

    convert_to_csv(temp_path, save_path)

def get_all_weather_data():
    timestamp = time.strftime("%m%d%H%M%S")
    out_dir = os.path.join(WEATHER_DATA_DIR, timestamp)
    for endpoint in KMA_ENDPOINTS:
        get_weather_data(endpoint, out_dir)


def nc_to_csv(nc_file: str):
    ds = nc.Dataset(nc_file, 'r')
    
    FF = ds.variables["FF"][:]
    DQF_FF = ds.variables["DQF_FF"][:]
    
    proj_var = ds.variables["gk2a_imager_projection"]
    
    lat_1 = proj_var.getncattr("standard_parallel1")  # 30.0
    lat_2 = proj_var.getncattr("standard_parallel2")  # 60.0
    lat_0 = proj_var.getncattr("origin_latitude")     # 38.0
    lon_0 = proj_var.getncattr("central_meridian")    # 126.0
    false_easting = proj_var.getncattr("false_easting")   # 0.0
    false_northing = proj_var.getncattr("false_northing") # 0.0
    
    pixel_size = proj_var.getncattr("pixel_size")     # 2000.0 m
    upper_left_easting = proj_var.getncattr("upper_left_easting")   # -899000.0
    upper_left_northing = proj_var.getncattr("upper_left_northing") # 899000.0
    
    ny, nx = FF.shape
    
    x_coords = upper_left_easting + np.arange(nx) * pixel_size
    y_coords = upper_left_northing - np.arange(ny) * pixel_size
    xx, yy = np.meshgrid(x_coords, y_coords)
    
    lcc_proj = Proj(proj='lcc',
                    lat_1=lat_1, lat_2=lat_2, 
                    lat_0=lat_0, lon_0=lon_0,
                    x_0=false_easting, y_0=false_northing,
                    datum='WGS84')
    
    lon, lat = lcc_proj(xx, yy, inverse=True)
    
    valid_mask = (np.isfinite(lat) & np.isfinite(lon) &
                 (lat >= 28) & (lat <= 43) & 
                 (lon >= 120) & (lon <= 135))
    
    ff = FF[valid_mask].flatten()
    dqf = DQF_FF[valid_mask].flatten()
    lat = lat[valid_mask].flatten()
    lon = lon[valid_mask].flatten()
    
    ds.close()
    
    csv_dir = os.path.join(SATELLITE_DATA_DIR, "csv")
    os.makedirs(csv_dir, exist_ok=True)
    base_name = os.path.basename(nc_file).replace(".nc", ".csv")
    csv_file = os.path.join(csv_dir, base_name)

    df = pd.DataFrame({
        "lat": lat,
        "lon": lon,
        "FF": ff,
        "DQF_FF": dqf
    })
    df.to_csv(csv_file, index=False)

def get_GK2A_fire_data():
    """ 데이터 딜레이 약 10시간, 짝수분만 가능"""
    cur_timestamp = time.strftime("%Y%m%d%H%M")
    dt = datetime.strptime(cur_timestamp, "%Y%m%d%H%M")
    dt_temp = dt - timedelta(hours=11)

    if dt_temp.minute % 2 != 0:
        dt_temp -= timedelta(minutes=1)
    timestamp = dt_temp.strftime("%Y%m%d%H%M")

    url = KMA_SATELLITE_BASE_URL+timestamp+f"&authKey={KMA_WEATHER_TOKEN}"
    try:
        response = requests.get(url)
        save_path = os.path.join(SATELLITE_DATA_DIR, "nc", f"{timestamp}.nc")

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        if response.status_code != 200:
            print("API 요청 실패 : ", response.status_code)
            return
    except Exception as e:
        print(e)
        return

    nc_to_csv(save_path)

def convert_to_csv(infile_path, outfile_path):
    with open(infile_path, "r", encoding="utf-8") as f_in:
        lines = f_in.readlines()

    data_start = None
    for i, line in enumerate(lines):
        if line.strip() == "":
            continue
        if not line.lstrip().startswith("#"):
            data_start = i
            break
    if data_start is None:
        raise ValueError("No data line")

    header_line = None
    for line in lines:
        if line.startswith("#") and "YYMMDDHHMI" in line:
            header_line = line.strip()
            break
    if header_line is None:
        raise Exception("No header line")

    raw_headers = header_line.lstrip("#").strip().split()

    def clean_header(tok:str) -> str:
        while tok.endswith("."):
            tok = tok[:-1]
        return tok

    headers = [clean_header(h) for h in raw_headers]

    if headers and headers[0].upper().startswith("YYMMDD"):
        headers[0] = "TIME"

    data_rows = []
    for line in lines[data_start:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.strip().split()
        data_rows.append(parts)

    with open(outfile_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout)
        writer.writerow(headers)
        for row in data_rows:
            writer.writerow(row)

    os.remove(infile_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--choice', '-c', type=int, choices=KMA_ENDPOINTS.keys())
    parser.add_argument('--list', '-l', action='store_true')
    parser.add_argument('--out', '-o', default=WEATHER_DATA_DIR)
    args = parser.parse_args()

    if args.list:
        print("Available endpoints:")
        for key, val in KMA_ENDPOINTS.items():
            print(f"{key}. {val['desc']}")
    elif args.choice:
        get_weather_data(args.choice, args.out)
