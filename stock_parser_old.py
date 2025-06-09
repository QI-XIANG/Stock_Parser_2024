import requests as req
from bs4 import BeautifulSoup
import datetime 
import pytz

#create Taipei timezone
tw = pytz.timezone('Asia/Taipei')

# 指定要抓取的網頁URL
import requests as req
from bs4 import BeautifulSoup

# 指定要抓取的網頁URL
def stock_parser(stock_code):
    url = "https://tw.stock.yahoo.com/quote/"+stock_code+".TW"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # 使用requests.get() 來得到網頁回傳內容
    r = req.get(url,headers=headers)
    stock_overview = []
    # request.get()回傳的是一個物件 
    # 若抓成功(即r.status_code==200), 則網頁原始碼會放在物件的text屬性, 我們把它存在一個變數 'web_content'
    web_content = r.text
    soup = BeautifulSoup(web_content, 'html.parser')
    stock_detail = soup.find_all('li', class_="price-detail-item")
    stock_title = soup.find_all('h1', class_="C($c-link-text)")[0].text + "(" + stock_code + ")"
    stock_overview.append(stock_title)
    for x in stock_detail:
        stock_overview.append(x.find_all('span')[1].text)
    
    if(stock_overview[7]>stock_overview[1]):
        stock_overview[0] = soup.find_all('h1', class_="C($c-link-text)")[0].text + "(" + stock_code + ")" + " (跌)"
    elif(stock_overview[7]<stock_overview[1]):
        stock_overview[0] = soup.find_all('h1', class_="C($c-link-text)")[0].text + "(" + stock_code + ")" + " (漲)"
    else:
        stock_overview[0] = soup.find_all('h1', class_="C($c-link-text)")[0].text + "(" + stock_code + ")" + " (平盤)"

    #print(stock_overview)
    
    return stock_overview

column_names = ["名稱", "成交", "開盤", "最高", "最低", "均價", "成交金額(億)", "昨收", "漲跌幅", "漲跌", "總量", "昨量", "振幅"]
stock_codes = ["%5ETWII", "5880", "00679B", "00713", "00733", "00907"]

stock_datas = []
for stock_code in stock_codes:
    stock_overview = stock_parser(stock_code)
    stock_datas.append(stock_overview)

f = open("README.md", "w",encoding='UTF-8')
f.write('| 名稱 | 成交 | 開盤 | 最高 | 最低 | 均價 | 成交金額(億) | 昨收 | 漲跌幅 | 漲跌 | 總量 | 昨量 | 振幅 |\n')
f.write('| -------- | -------- | -------- | -------- |-------- | -------- | -------- |-------- |-------- |-------- | -------- | -------- |-------- |\n')
for x in stock_datas:
    f.write('|')
    for y in x:
        f.write(y+'|')
    f.write('\n')
f.write("###### 資料更新時間: "+str(datetime.datetime.now(tw).strftime("%Y-%m-%d %H:%M:%S")))
f.close()