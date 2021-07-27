import os
import re
import json
import requests
import warnings
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore") 

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

url = "https://diemthi.vnanet.vn/"
char_regex = "[\n\t]"

response = requests.get(url, headers = headers, verify = False)
soupSite = BeautifulSoup(response.text, 'html.parser')
dataSelect = soupSite.find("select", id = "listCity")
allCityCode = dataSelect.find_all("option")

result = []

for code in allCityCode:
    data_code = code['value']
    data_name = re.sub(char_regex, "", code.getText().replace(data_code, ""))
    while (data_name[0] == " "):
        data_name = data_name[1:]
    result_tmp = dict()
    result_tmp['code'] = data_code
    result_tmp['name'] = data_name
    result.append(result_tmp)
    
with open("cityCode.json", 'w', encoding='utf-8') as f:
    f.write(json.dumps(result))