import os
import folium
from csv_reader import load_grid, load_nasa_fire_grid, load_GK2A_fire_grid, load_kfs_fire_grid
from config import MAP_DATA_DIR

def draw_grid():
    save_path = os.path.join(MAP_DATA_DIR, "map.html")

    grid = load_grid()
    if not grid:
        return
    center_lat = sum(d['LAT'] for d in grid) / len(grid)
    center_lon = sum(d['LON'] for d in grid) / len(grid)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    for d in grid:
        folium.Marker(
            location=[d['LAT'], d['LON']],
            popup=f"{d['NAME']} (ID: {d['ID']})",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    m.save(save_path)

def draw_GK2A_fire_grid():
    save_path = os.path.join(MAP_DATA_DIR, "fire_map_GK2A.html")

    grid = load_GK2A_fire_grid()
    if not grid:
        return
    center_lat = sum(d['LAT'] for d in grid) / len(grid)
    center_lon = sum(d['LON'] for d in grid) / len(grid)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    for d in grid:
        folium.Marker(
            location=[d['LAT'], d['LON']],
            popup=f"DQF_FF = {d['DQF_FF']}",
            icon = folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

    m.save(save_path)

def draw_nasa_fire_grid():
    save_path = os.path.join(MAP_DATA_DIR, "fire_map_firms.html")

    grid = load_nasa_fire_grid()
    if not grid:
        return
    center_lat = sum(d['LAT'] for d in grid) / len(grid)
    center_lon = sum(d['LON'] for d in grid) / len(grid)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    for d in grid:
        if d['INST']=="MODIS" and d['CONFIDENCE'] <=0:
            continue
        elif d['INST']=="VIIRS" and d['CONFIDENCE']=='l':
            continue

        folium.Marker(
            location=[d['LAT'], d['LON']],
            popup=f"{d['DATE']}-{d['TIME']}\nFRP: {d['FRP']} Conf: {d['CONFIDENCE']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

    m.save(save_path)

def draw_kfs_fire_grid():
    save_path = os.path.join(MAP_DATA_DIR, "fire_map_kfs.html")

    grid = load_kfs_fire_grid()
    if not grid:
        return
    center_lat = sum(d['LAT'] for d in grid) / len(grid)
    center_lon = sum(d['LON'] for d in grid) / len(grid)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    for d in grid:
        if d['DATE_END'] == "null":
            folium.Marker(
                location=[d['LAT'], d['LON']],
                popup=f"Start : {d['DATE_START']}, 진행상태 : {d['PROGRESS']}, 단계 : {d['RESPONSE_LEVEL']}, 진화율 : {d['CONTROL']}%",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)
        else:
            folium.Marker(
                location=[d['LAT'], d['LON']],
                popup=f"Start : {d['DATE_START']}, End : {d['DATE_END']}, 단계 : {d['RESPONSE_LEVEL']}",
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(m)

    m.save(save_path)