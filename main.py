from KMA_API import get_data, get_all_data
from grid_data import load_grid

"""
get_data(1, "weather_data")

get_all_data()

grid = load_grid()
"""


if __name__ == "__main__":

    grid = load_grid()
    get_all_data()