import csv
import os

file_path = os.path.join(os.getcwd(), "map_data/grid.csv")

def load_grid():
    result = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append({
                'ID': int(row['ID']),
                'LON': float(row['LON']),
                'LAT': float(row['LAT']),
                'NAME': row['NAME']
            })
    return result