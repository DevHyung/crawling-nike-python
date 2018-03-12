import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import xlsxwriter
import time
now = time.localtime()
s = "%04d%02d%02d_%02d%02d추출" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
def hook(blockNumber, blockSize, totalSize):
    percent = int(((blockNumber * blockSize) / totalSize) * 100)
    if (percent % 25) == 0:
        print("  [INFO] 사진 다운로드 " + str(percent) + "% 진행.")
basic_url = "http://nike.lotteimall.com/detailXml/gdsDetail.do?gdsCd="
with open('상품번호.txt','r') as f:
    code_list = []
    lines = f.readlines()
    for line in lines:
        code_list.append(line.strip())
#code_list = ['807471-103','903896-005','AA1256-002','AA2547-007','596728-038','878068-101']
wb = xlsxwriter.Workbook('./'+s+'.xlsx')
ws = wb.add_worksheet('sheet1')
ws.write(0, 0, "파일명이름")
ws.write(0, 1, "이름")
ws.write(0, 2, "모델명")
ws.write(0, 3, "색상")
ws.write(0, 4, "재질")
ws.write(0, 5, "사진들")
j = 1
for code in code_list:
    print("[INFO] 현재 상품번호 : " + str(code))
    # get html 소스
    url = basic_url + str(code)
    print(url)
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'html.parser')
    # 중간 단계
    prod_names = bs.select("#wrap > div.container > div.photo > div.top_area")[0]
    prod_info = bs.select("#tab1 > table")[0].find_all("td")
    prod_pics = bs.select("#wrap > div.container > div.photo > div.photo_area > ul")[0]
    # 데이터 추출
    eng_name = prod_names.find("h2").get_text().replace(code, "")
    kor_name = prod_names.find("h3").get_text()
    trs = bs.select("#tab1 > table")[0].find_all("tr")
    material = ''
    for tr in trs:
        if '소재' in tr.get_text().strip():
            material = tr.get_text().split('소재')[1].strip()
        if '색상' in tr.get_text().strip():
            color = tr.get_text().split('색상')[1].strip()

    print("[INFO] 영문 상품명 : " + eng_name)
    print("[INFO] 한글 상품명 : " + kor_name)
    print("[INFO] 소재 : " + material)
    print("[INFO] 색상 정보 : " + color)
    ws.write(j,0,kor_name)
    ws.write(j, 1, eng_name)
    ws.write(j, 2, code)
    ws.write(j, 3, color)
    ws.write(j, 4, material)
    # 사진 url 추출
    pic_urls = []
    img_tags = prod_pics.find_all("img")
    for img_tag in img_tags:
        pic_urls.append(img_tag.get("src"))
    # 사진 다운로드
    count = 1
    for pic_url in pic_urls:
        print("[INFO] " + str(count) + "번째 사진 다운로드 시작.")
        #dirname = "./pics/" + str(code)
        dirname = "./pics/"
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        fileurl = dirname + str(code) + "_" + str(count) + ".png"
        urllib.request.urlretrieve(pic_url, fileurl)
        ws.write(j, 4 + count, os.getcwd() + fileurl[1:].replace('/', '\\'))
        count += 1

    j+=1
    print("_"*30)
wb.close()