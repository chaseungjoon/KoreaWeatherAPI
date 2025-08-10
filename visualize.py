import os
import folium
from grid_data import load_grid

save_path = os.path.join(os.getcwd(), 'map_data/map.html')

grid = load_grid()
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
