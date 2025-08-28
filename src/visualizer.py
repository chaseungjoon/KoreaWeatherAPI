import os
import folium
from src.csv_reader import load_grid, load_firms_fire_grid, load_GK2A_fire_grid, load_kfs_fire_grid, \
    load_kfs_landslide_grid
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

def draw_firms_fire_grid():
    save_path = os.path.join(MAP_DATA_DIR, "fire_map_firms.html")

    grid = load_firms_fire_grid()
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
        if d.get("PROGRESS") <3:
            icon_color = "red"
        elif d.get("PROGRESS") ==3:
            icon_color = "green"
        else:
            icon_color = "blue"

        popup_text = (
            f"발생일시 : {d.get('DATE')}\n"
            f"주소 : {d.get('ADDRESS')}\n"
            f"상태 : {d.get('PROGRESS')}\n"
            f"단계 : {d.get('RESPONSE_LEVEL')}"
        )
        if "CONTAINMENT_RATE" in d:
            popup_text += f"\n진화율 : {d['CONTAINMENT_RATE']}"

        folium.Marker(
            location=[d.get("LAT"), d.get("LON")],
            popup=popup_text,
            icon=folium.Icon(color=icon_color, icon="info-sign")
        ).add_to(m)

    m.save(save_path)

def draw_kfs_landslide_grid():
    save_path = os.path.join(MAP_DATA_DIR, "landslide_map_kfs.html")
    grid = load_kfs_landslide_grid()
    if not grid:
        return
    center_lat = sum(d['LAT'] for d in grid) / len(grid)
    center_lon = sum(d['LON'] for d in grid) / len(grid)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)
    for d in grid:
        if d.get("WARNING_LEVEL") == "주의보":
            icon_color = "orange"
        elif d.get("WARNING_LEVEL") == "경보":
            icon_color = "red"
        else: icon_color = "green"
        popup_text = (
            f"발생일시 : {d.get('DATE')}\n"
            f"주소 : {d.get('LOCATION')}\n"
            f"단계 : {d.get('WARNING_LEVEL')}"
        )
        folium.Marker(
            location=[d.get("LAT"), d.get("LON")],
            popup=popup_text,
            icon=folium.Icon(color=icon_color, icon="info-sign")
        ).add_to(m)

    m.save(save_path)