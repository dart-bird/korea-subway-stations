from numpy import NaN
import requests
import pandas as pd
import json
import subprocess
import re
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'data.seoul.go.kr',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

response = requests.get('https://data.seoul.go.kr/dataList/OA-12764/F/1/datasetView.do', headers=headers)
html = BeautifulSoup(response.content, 'html.parser')
seq = re.findall(r'\d+', html.select("#fileTr_1 > td:nth-child(6) > a")[0]['href'])[0]

data = {
    "infId" : "OA-12764",
    "seqNo" : "",
    "seq" : str(seq),
    "infSeq" : "2"
}

response = requests.post('http://datafile.seoul.go.kr/bigfile/iot/inf/nio_download.do?&useCache=false', headers=headers, data=data, verify=False)
result = pd.read_excel(response.content, engine='openpyxl').dropna()
keys = [key[0] for key in zip(result.keys())]
stations_info = {"stationList":[   
                    {keys[0]:int(data[0]), keys[1]:int(data[1]), keys[2]:str(data[2])}
                    for data in zip(result[keys[0]], result[keys[1]], result[keys[2]])
                ]}

with open("./seoul_stations.json", 'r') as f1:
    data = json.load(f1)

if data!=stations_info:
    with open("./seoul_stations.json", 'w') as f2:
        json.dump(stations_info, f2, ensure_ascii=False)
    subprocess.call(['python', 'commit_push.py'])
else:
    print('Nothing to update.')