import requests
import os
import time
import json

auth = os.getenv("KMA_WEATHER_TOKEN")
base_url = "https://apihub.kma.go.kr/api"

def get_data(choice):
    # AWS매분자료 (1분마다 업데이트되는 종합 기상 자료)
    if choice == 1:
        url = f"{base_url}/typ01/cgi-bin/url/nph-aws2_min?disp=0&help=1&authKey={auth}"
        file_type = "csv"
        data_type = "AWS_overall"
    # AWS 운고 운량
    elif choice == 2:
        url = f"{base_url}/typ01/cgi-bin/url/nph-aws2_min_cloud?stn=0&disp=0&help=1&authKey={auth}"
        file_type = "csv"
        data_type = "AWS_cloud"
    else:
        print("\nInvalid choice\n")
        return

    timestamp = time.strftime("%m%d%H%M%S")
    save_path = os.path.join(os.getcwd(), "Weather_Data", f"{data_type}_{timestamp}.{file_type}")
    response = requests.get(url)
    response.encoding = 'euc-kr'
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    while True:
        option = int(input("Choose an option\n0)exit\n1)AWS매분자료\n2)AWS 운고운량\n>> "))
        if option == 0:
            break
        get_data(option)