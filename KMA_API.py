import requests
import os
import time
import argparse

auth = os.getenv("KMA_WEATHER_TOKEN")
data_dir = "weather_data"
aws_base_url = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min"
endpoints = {
        1: {"url": aws_base_url + f"?authKey={auth}", "filename": "AWS", "filetype": "csv", "desc" : "AWS 매분자료"},
        2: {"url": aws_base_url + f"_cloud?authKey={auth}", "filename": "AWS_cloud", "filetype":"csv", "desc": "AWS 운고운량"},
        3: {"url": aws_base_url + f"_lst?authKey={auth}", "filename": "AWS_temp", "filetype":"csv", "desc": "AWS 초상온도"},
        4: {"url": aws_base_url + f"_vis?authKey={auth}", "filename": "AWS_vis", "filetype":"csv", "desc": "AWS 가시거리"},
}

def get_data(choice, out_dir):
    if choice not in endpoints:
        print("Wrong choice")
        return

    url = endpoints[choice]["url"]
    filename = endpoints[choice]["filename"]
    filetype = endpoints[choice]["filetype"]

    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        return

    timestamp = time.strftime("%m%d%H%M%S")
    os.makedirs(os.path.join(os.getcwd(),out_dir), exist_ok=True)
    save_path = os.path.join(os.getcwd(), out_dir, f"{filename}_{timestamp}.{filetype}")

    if filetype == "csv":
        response.encoding = 'euc-kr'
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(response.text)


def get_all_data():
    timestamp = time.strftime("%m%d%H%M%S")
    out_dir = os.path.join(os.getcwd(), "weather_data", timestamp)
    for ep in endpoints:
        get_data(ep, out_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--choice', '-c', type=int, choices=endpoints.keys())
    parser.add_argument('--list', '-l', action='store_true')
    parser.add_argument('--out', '-o', type=str, default=data_dir)
    args = parser.parse_args()

    if args.list:
        print("Available endpoints:")
        for key, val in endpoints.items():
            print(f"{key}. {val['desc']}")
    elif args.choice:
        get_data(args.choice, args.out)
