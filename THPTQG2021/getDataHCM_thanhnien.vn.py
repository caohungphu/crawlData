import os
import re
import json
import time
import requests
import warnings
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore") 

url = "https://thanhnien.vn/ajax/diemthi.aspx?kythi=THPT&nam=2021&city=DDT&text={}&top=no"

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

file_output = "dataHCM_2.csv"

def getData(SoBaoDanh):
    response = requests.get(url.format(SoBaoDanh), headers = headers, verify = False)
    soupSite = BeautifulSoup(response.text, 'html.parser')
    dataSelect = soupSite.find("tr")
    data = dataSelect.find_all("td")
    # return {
        # 'sobaodanh': SoBaoDanh,
        # 'hoten': data[2].getText(),
        # 'ngaysinh': data[4].getText(),
        # 'gioitinh': data[5].getText(),
        
        # 'diemToan': data[6].getText(),
        # 'diemNguVan': data[7].getText(),
        # 'diemNgoaiNgu': data[16].getText(),
        
        # 'diemVatLy': data[8].getText(),
        # 'diemHoaHoc': data[9].getText(),
        # 'diemSinhHoc': data[10].getText(),
        # 'diemKHTN': data[11].getText(),
        
        # 'diemLichSu': data[12].getText(),
        # 'diemDiaLy': data[13].getText(),
        # 'diemGDCD': data[14].getText(),
        # 'diemKHXH': data[15].getText(),
        
        
    # }
    
    csvData = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}"
    return csvData.format(SoBaoDanh, data[2].getText(), data[4].getText(), data[5].getText(),
                            data[6].getText(), data[7].getText(), data[16].getText(),  
                            data[8].getText(), data[9].getText(), data[10].getText(), data[11].getText(), 
                            data[12].getText(), data[13].getText(), data[14].getText(), data[15].getText())


if __name__ == '__main__':
    formatID = "02{}"
    noti = "SoBaoDanh: {} -> {}"
    
    for i in range(1, 99999):  
        id = formatID.format(str(i).zfill(6))
        try:
            with open(file_output, "a", encoding="utf-8") as f:
                f.write(getData(id) + "\n")     
            print(noti.format(id, "Success"))
        except:
            print(noti.format(id, "Fail"))
            continue
    f.close()