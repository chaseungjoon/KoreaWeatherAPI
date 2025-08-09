import requests
import os
import time
import json

auth = os.getenv("KMA_WEATHER_TOKEN")
base_url = "https://apihub.kma.go.kr/api"

def get_data(choice):
    # ASOS (1시간마다 업데이트 되는 종합 날씨 데이터)
    if choice == 1:
        url = f"{base_url}/typ01/url/kma_sfctm2.php?stn=0&dataType=JSON&help=1&authKey={auth}"
        file_type = "json"
        data_type = "ASOS"
    # 대기 정보 binary
    elif choice == 2:
        url = f"{base_url}/typ04/url/rdr_cmp_file.php?&data=bin&cmp=cpp&authKey={auth}"
        file_type = "bin"
        data_type = "HSR_bin"
    # 대기 정보 image (인코딩 필요)
    elif choice == 3:
        url = f"{base_url}/typ04/url/rdr_cmp_file.php?&data=img&cmp=cmb&authKey={auth}"
        file_type = "cmb"
        data_type = "HSR_img"
    # 향후 1시간 일기예보 (5분마다 업데이트)
    elif choice == 4:
        url = f"{base_url}/typ01/cgi-bin/url/nph-rdr_cmp_inf?&cmp=HSR&qcd=MSK&disp=A&authKey={auth}"
        file_type = "txt"
        data_type = "HSR_comp"
    else:
        print("\nInvalid choice\n")
        return

    timestamp = time.strftime("%y%m%d%H%M%S")
    save_path = os.path.join(os.getcwd(), "Data", f"{data_type}_{timestamp}.{file_type}")
    response = requests.get(url)
    response.encoding = 'euc-kr'
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    while True:
        option = int(input("Choose an option\n0)exit\n1)ASOS\n2)HSR_bin\n3)HSR_image\n4)HSR_composite\n>> "))
        if option == 0:
            break
        get_data(option)