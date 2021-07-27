import os
import re
import json
import time
import requests
import warnings
from bs4 import BeautifulSoup

url = "http://diemthi.hcm.edu.vn/Home/Show"

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

step_sleep = 2000

time_sleep = 100

def convertText(data):
    text = data.renderContents()
    return text.strip().decode("utf-8")
    
def convertScore(fullScore):
    check = None
    if fullScore.find("KHTN") != -1:
        check = True
    else:
        check = False
    data = list(filter(None, fullScore.split(" ")))
    for i in range(len(data) - 1):
        if not data[i].replace(".", "").isnumeric() and not data[i + 1].replace(".", "").isnumeric():
            data[i] += " " + data[i + 1]
            data[i + 1] = ''
        data[i] = data[i].replace(":", "")
    return check, list(filter(None, data))
    
def getScore(fullScore):
    #D1 = Toan, D2 = Ngu van, D3 = Vat li, D4 = Hoa hoc, D5 = Sinh hoc, D6 = KHTN, D7 = Lich su, D8 = Dia li, D9 = GDCD, D10 = KHXH, D11 = Ngoai ngu
    result = {
        'D1': "-",
        'D2': "-",   
        'D3': "-",
        'D4': "-",
        'D5': "-",
        'D6': "-",   
        'D7': "-",
        'D8': "-",
        'D9': "-",
        'D10': "-",
        'D11': "-"
    }
    checkKHTN, dataScore = convertScore(fullScore)
    result['D1'] = dataScore[1]
    result['D2'] = dataScore[3]
    if checkKHTN:
        result['D3'] = dataScore[5]
        result['D4'] = dataScore[7]
        result['D5'] = dataScore[9]
        result['D6'] = dataScore[11]
    else:
        result['D7'] = dataScore[5]
        result['D8'] = dataScore[7]
        result['D9'] = dataScore[9]
        result['D10'] = dataScore[11]
    result['D11'] = dataScore[13]
    return result


def getData(SoBaoDanh):
    param = {'SoBaoDanh': SoBaoDanh}
    response = requests.get(url, headers = headers, params = param, verify = False)
    soupSite = BeautifulSoup(response.text, 'html.parser')
    dataSelect = soupSite.find_all("tr")[1]
    dataAll = dataSelect.find_all("td")
    fullName = convertText(dataAll[0])
    CCID = convertText(dataAll[1])
    fullScore = getScore(convertText(dataAll[2]))
    
    # jsonData =  {
        # "SoBaoDanh": SoBaoDanh,
        # "fullName": fullName,
        # "CCID": CCID,
        # "fullScore": fullScore)
    # }
   
    csvData = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}"
    return csvData.format(SoBaoDanh, fullName, CCID, fullScore['D1'], fullScore['D2'], 
                            fullScore['D3'], fullScore['D4'], fullScore['D5'], fullScore['D6'], 
                            fullScore['D7'], fullScore['D8'], fullScore['D9'], fullScore['D10'], 
                            fullScore['D11'])



if __name__ == '__main__':
    formatID = "02{}"
    noti = "SoBaoDanh: {} -> {}"

    for i in range(1, 99999):  
        if i % step_sleep == 0:
            time.sleep(time_sleep)
        id = formatID.format(str(i).zfill(6))
        try:
            with open("dataHCM.csv", "a", encoding="utf-8") as f:
                f.write(getData(id) + "\n")     
            print(noti.format(id, "Success"))
        except:
            print(noti.format(id, "Fail"))
            continue
    f.close()