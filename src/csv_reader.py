import csv
import os
from config import GRID_PATH, FIRE_DATA_DIR, SATELLITE_DATA_DIR, KFS_DATA_DIR, korea_administrative_divisions


def get_recent_file(path):
    csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]
    if not csv_files:
        return None

    latest_file = max(csv_files)
    return os.path.join(path, latest_file)

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

def load_GK2A_fire_grid():
    satellite_fire_path = get_recent_file(os.path.join(SATELLITE_DATA_DIR, "csv"))
    if not satellite_fire_path:
        return []

    result = []
    with open(satellite_fire_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat = float(row['lat'])
            lon = float(row['lon'])
            FF = float(row['FF'])
            DQF_FF = row['DQF_FF']

            if not (33 <= lat <= 38 and 126 <= lon <= 130):
                continue
            if FF != 1.0:
                continue
            if DQF_FF not in ["7.0", "8.0", "9.0"]:
                continue

            result.append({
                'LAT': lat,
                'LON': lon,
                'FF': FF,
                'DQF_FF': DQF_FF
            })

        return result

def load_firms_fire_grid():
    fire_file_path = get_recent_file(FIRE_DATA_DIR)
    if not fire_file_path:
        return []
    result = []
    with open(fire_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:

            if row['instrument']=="MODIS":
                conf = float(row['confidence'])
            else:
                conf = row['confidence']

            result.append({
                'DATE': row['acq_date'],
                'TIME': row['acq_time'],
                'LON': float(row['longitude']),
                'LAT': float(row['latitude']),
                'FRP': float(row['frp']),
                'CONFIDENCE': conf,
                'INST': row['instrument']
            })
    return result

def load_kfs_fire_grid():
    fire_file_path = get_recent_file(KFS_DATA_DIR)
    if not fire_file_path:
        return []

    result = []
    with open(fire_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = {
                'ID': row['frfrInfoId'],
                'DATE': row['frfrFrngDtm'],
                'LAT': float(row['frfrLctnYcrd']),
                'LON': float(row['frfrLctnXcrd']),
                'ADDRESS': row['frfrSttmnAddr'],
                'PROGRESS': int(row['frfrPrgrsStcd']),
                'RESPONSE_LEVEL': int(row['frfrStepIssuCd']),
            }
            if 'frfrPotfrRt' in row and row['frfrPotfrRt'].isdigit():
                item['CONTAINMENT_RATE'] = int(row['frfrPotfrRt'])
            if 'frfrOccrrTpcd' in row:
                item['OCCURRENCE_STATUS'] = int(row['frfrOccrrStcd'])

            result.append(item)

    return result


def load_kfs_landslide_grid():
    landslide_file_path = get_recent_file(os.path.join(KFS_DATA_DIR, "landslide"))
    if not landslide_file_path:
        return []

    result = []
    with open(landslide_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['LNLD_FRCST_NM']:
                location = row['SGG_NM']
                item = {
                    'DATE': row['PREDC_ANLS_DT'],
                    'LOCATION': location,
                    'WARNING_LEVEL': row['LNLD_FRCST_NM']
                }

                if location in korea_administrative_divisions:
                    coord_data = korea_administrative_divisions[location]
                    item['LAT'] = coord_data['lat']
                    item['LON'] = coord_data['lon']
                else:
                    print(f"{location} not in reference db")
                    item['LAT'] = None
                    item['LON'] = None

                result.append(item)
            else:
                continue

    return result