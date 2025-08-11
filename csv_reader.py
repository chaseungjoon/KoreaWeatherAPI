import csv
import os
from config import GRID_PATH, FIRE_DATA_DIR

def get_recent_fire():
    csv_files = [f for f in os.listdir(FIRE_DATA_DIR) if f.startswith("fire_data_") and f.endswith(".csv")]
    if not csv_files:
        return None

    latest_file = max(csv_files)
    return os.path.join(FIRE_DATA_DIR, latest_file)

def load_grid():
    result = []
    with open(GRID_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append({
                'ID': int(row['ID']),
                'LON': float(row['LON']),
                'LAT': float(row['LAT']),
                'NAME': row['NAME']
            })
    return result

def load_fire_grid():
    fire_file_path = get_recent_fire()
    if not fire_file_path:
        return []
    result = []
    with open(fire_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append({
                'DATE': row['acq_date'],
                'TIME': row['acq_time'],
                'LON': float(row['longitude']),
                'LAT': float(row['latitude']),
                'FRP': float(row['frp']),
                'CONFIDENCE': float(row['confidence'])
            })
    return result