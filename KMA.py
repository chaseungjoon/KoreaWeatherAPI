import requests
import os
import time

auth = os.getenv("KMA_WEATHER_TOKEN")
aws_base_url = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min"
endpoints = {
        1: {"url": aws_base_url + f"?authKey={auth}", "filename": "AWS", "filetype": ".csv"},
        2: {"url": aws_base_url + f"_cloud?&authKey={auth}", "filename": "AWS_cloud", "filetype":".csv"},
}

def get_data(choice):
    if choice not in endpoints:
        print("Wrong choice")
        return

    url = endpoints[choice]["url"]
    filename = endpoints[choice]["filename"]
    filetype = endpoints[choice]["filetype"]

    timestamp = time.strftime("%m%d%H%M%S")
    save_path = os.path.join(os.getcwd(), "Weather_Data", f"{filename}_{timestamp}.{filetype}")
    response = requests.get(url)
    response.encoding = 'euc-kr'
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    while True:
        option = int(input("Choose an option"
                           "\n0)exit"
                           "\n1)AWS매분자료"
                           "\n2)AWS 운고운량"
                           "\n>> "))
        if option == 0:
            break
        get_data(option)