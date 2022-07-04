from numpy import NaN
import requests
import pandas as pd
import json
import subprocess
import re
from bs4 import BeautifulSoup

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'es-ES,es;q=0.9',
}

response = requests.get('https://data.seoul.go.kr/dataList/OA-12764/F/1/datasetView.do')
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

