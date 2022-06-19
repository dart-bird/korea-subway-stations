import requests
import pandas as pd
import json
headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'es-ES,es;q=0.9',
}

data = {
    "infId" : "OA-12764",
    "seqNo" : "",
    "seq" : "4",
    "infSeq" : "2"
}

response = requests.post('http://datafile.seoul.go.kr/bigfile/iot/inf/nio_download.do?&useCache=false', headers=headers, data=data, verify=False)
result = pd.read_excel(response.content)
keys = [key[0] for key in zip(result.keys())]
stations_info = [ {keys[0]:data[0], keys[1]:data[1], keys[2]:data[2]} for data in zip(result[keys[0]], result[keys[1]], result[keys[2]]) ]

with open("./seoul_stations.json", 'w') as file:
    json.dump(stations_info, file, ensure_ascii=False)