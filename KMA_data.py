import requests
import os
import time

auth = os.getenv("KMA_WEATHER_TOKEN")
data_dir = "weather_data"
aws_base_url = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min"
endpoints = {
        1: {"url": aws_base_url + f"?authKey={auth}", "filename": "AWS", "filetype": "csv", "desc" : "AWS 매분자료"},
        2: {"url": aws_base_url + f"_cloud?authKey={auth}", "filename": "AWS_cloud", "filetype":"csv", "desc": "AWS 운고운량"},
        3: {"url": aws_base_url + f"_lst?authKey={auth}", "filename": "AWS_temp", "filetype":"csv", "desc": "AWS 초상온도"},
        4: {"url": aws_base_url + f"_vis?authKey={auth}", "filename": "AWS_vis", "filetype":"csv", "desc": "AWS 가시거리"},
}

def get_data(choice):
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
    save_path = os.path.join(os.getcwd(), data_dir, f"{filename}_{timestamp}.{filetype}")

    if filetype == "csv":
        response.encoding = 'euc-kr'
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(response.text)


if __name__ == "__main__":
    while True:
        print("Choose an option"
              "\n0. exit")
        for key, val in endpoints.items():
            print(f"{key}. {val['desc']}")
        option = int(input(">> "))
        if option == 0:
            break
        get_data(option)