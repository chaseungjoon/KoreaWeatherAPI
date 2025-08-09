import requests
import os
import argparse
import json

auth = os.getenv("KMA_WEATHER_TOKEN")

def get_data(url, output):
    save_path = os.path.join(os.getcwd(), output)
    response = requests.get(url)
    response.encoding = 'euc-kr'
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    url = "https://apihub.kma.go.kr/api/typ01/url/stn_inf.php?inf=AWS&stn=&help=1&authKey=ud6z-X7yRDKes_l-8qQyFg"
    output = "Map_Data/grid_AWS.csv"

    get_data(url, output)
