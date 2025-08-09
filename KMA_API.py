import csv
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

def get_data(endpoint, out_dir):
    if endpoint not in endpoints:
        print("Wrong choice")
        return

    url = endpoints[endpoint]["url"]
    filename = endpoints[endpoint]["filename"]
    filetype = endpoints[endpoint]["filetype"]

    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        return

    timestamp = time.strftime("%m%d%H%M%S")
    os.makedirs(os.path.join(os.getcwd(),out_dir), exist_ok=True)

    temp_path = os.path.join(os.getcwd(),out_dir,f"{filename}.{filetype}")
    save_path = os.path.join(os.getcwd(), out_dir, f"{filename}_{timestamp}.{filetype}")

    if filetype == "csv":
        response.encoding = 'euc-kr'
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(response.text)

    convert_to_csv(temp_path, save_path)

def get_all_data():
    timestamp = time.strftime("%m%d%H%M%S")
    out_dir = os.path.join(os.getcwd(), "weather_data", timestamp)
    for ep in endpoints:
        get_data(ep, out_dir)

def convert_to_csv(infile_path, outfile_path):
    with open(infile_path, "r", encoding="utf-8") as f_in:
        lines = f_in.readlines()

    data_start = None
    for i, line in enumerate(lines):
        if line.strip() == "":
            continue
        if not line.lstrip().startswith("#"):
            data_start = i
            break
    if data_start is None:
        raise ValueError("No data line")

    header_line = None
    for line in lines:
        if line.startswith("#") and "YYMMDDHHMI" in line:
            header_line = line.strip()
            break
    if header_line is None:
        raise Exception("No header line")

    raw_headers = header_line.lstrip("#").strip().split()

    def clean_header(tok:str) -> str:
        while tok.endswith("."):
            tok = tok[:-1]
        return tok

    headers = [clean_header(h) for h in raw_headers]

    if headers and headers[0].upper().startswith("YYMMDD"):
        headers[0] = "TIME"

    data_rows = []
    for line in lines[data_start:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.strip().split()
        data_rows.append(parts)

    with open(outfile_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout)
        writer.writerow(headers)
        for row in data_rows:
            writer.writerow(row)

    os.remove(infile_path)

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
