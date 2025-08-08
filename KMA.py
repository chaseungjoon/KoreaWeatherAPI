import requests
import os
import time
import json


auth = os.getenv("KMA_WEATHER_TOKEN")

def getUrl(choice):
    # 1시간 주기
    if choice == "ASOS":
        return f"https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?stn=0&dataType=JSON&help=1&authKey={auth}"
    elif choice == "HSR_bin":
        return f"https://apihub.kma.go.kr/api/typ04/url/rdr_cmp_file.php?&data=bin&cmp=cpp&authKey={auth}"
    elif choice == "HSR_image":
        return f"https://apihub.kma.go.kr/api/typ04/url/rdr_cmp_file.php?&data=img&cmp=cmb&authKey={auth}"
    #5분 주기
    elif choice == "HSR_composite":
        return f"https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-rdr_cmp_inf?&cmp=HSR&qcd=MSK&disp=A&authKey={auth}"
    else:
        return None

def downloadFile(url):
    timestamp = time.strftime("%y%m%d%H%M%S")
    save_path = os.path.join(os.getcwd(), "Data", f"{timestamp}.csv")

    response = requests.get(url)
    response.encoding = 'euc-kr'
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    downloadFile(getUrl("HSR_composite"))

