import requests as req
from bs4 import BeautifulSoup
import datetime
import pytz

#create Taipei timezone
tw = pytz.timezone('Asia/Taipei')

# 指定要抓取的網頁URL
def stock_parser(stock_code):
    url = "https://tw.stock.yahoo.com/quote/"+stock_code+".TW"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # 使用requests.get() 來得到網頁回傳內容
    r = req.get(url,headers=headers)
    # request.get()回傳的是一個物件
    # 若抓成功(即r.status_code==200), 則網頁原始碼會放在物件的text屬性, 我們把它存在一個變數 'web_content'
    web_content = r.text
    soup = BeautifulSoup(web_content, 'html.parser')
    stock_detail = soup.find_all('li', class_="price-detail-item")
    stock_title = soup.find_all('h1', class_="C($c-link-text)")[0].text + "(" + stock_code + ")"

    # 抓取原始資料
    # 這裡的索引是根據Yahoo股市網頁的HTML結構
    # 確保這些索引與想要抓取的資料相對應
    data_raw = []
    for x in stock_detail:
        data_raw.append(x.find_all('span')[1].text)

    # 重新排序資料
    # 原始 stock_overview 的順序為: 名稱, 成交, 開盤, 最高, 最低, 均價, 成交金額(億), 昨收, 漲跌幅, 漲跌, 總量, 昨量, 振幅
    # 新的順序為: 名稱, 最高, 最低, 開盤, 成交, 均價, 成交金額(億), 昨收, 漲跌幅, 漲跌, 總量, 昨量, 振幅
    # 為了方便對應，將原始資料依據其原始索引來標記：
    # [0] 成交價, [1] 開盤價, [2] 最高價, [3] 最低價, [4] 均價, [5] 成交金額(億), [6] 昨收, [7] 漲跌幅, [8] 漲跌, [9] 總量, [10] 昨量, [11] 振幅

    # 創建一個字典來儲存抓取到的資料，方便按名稱取用
    stock_data_map = {
        "成交": data_raw[0],
        "開盤": data_raw[1],
        "最高": data_raw[2],
        "最低": data_raw[3],
        "均價": data_raw[4],
        "成交金額(億)": data_raw[5],
        "昨收": data_raw[6],
        "漲跌幅": data_raw[7],
        "漲跌": data_raw[8],
        "總量": data_raw[9],
        "昨量": data_raw[10],
        "振幅": data_raw[11],
    }

    # 根據昨收和成交價判斷漲跌
    if float(stock_data_map["昨收"].replace(',', '')) > float(stock_data_map["成交"].replace(',', '')):
        stock_name = stock_title + " (跌)"
    elif float(stock_data_map["昨收"].replace(',', '')) < float(stock_data_map["成交"].replace(',', '')):
        stock_name = stock_title + " (漲)"
    else:
        stock_name = stock_title + " (平盤)"

    # 按照指定的順序排列資料
    # | 名稱 | 最高 | 最低 | 開盤 | 成交 | 均價 | 成交金額(億) | 昨收 | 漲跌幅 | 漲跌 | 總量 | 昨量 | 振幅 |
    ordered_data = [
        stock_name,
        stock_data_map["最高"],
        stock_data_map["最低"],
        stock_data_map["開盤"],
        stock_data_map["成交"],
        stock_data_map["均價"],
        stock_data_map["成交金額(億)"],
        stock_data_map["昨收"],
        stock_data_map["漲跌幅"],
        stock_data_map["漲跌"],
        stock_data_map["總量"],
        stock_data_map["昨量"],
        stock_data_map["振幅"]
    ]

    return ordered_data

stock_codes = ["%5ETWII", "5880", "00679B", "00713", "00733", "00907"]

stock_datas = []
for stock_code in stock_codes:
    stock_overview = stock_parser(stock_code)
    stock_datas.append(stock_overview)

# 打開 README.md 檔案並寫入資料
f = open("README.md", "w",encoding='UTF-8')

# 代入修改後的欄位順序
f.write('| 名稱 | 最高 | 最低 | 開盤 | 成交 | 均價 | 成交金額(億) | 昨收 | 漲跌幅 | 漲跌 | 總量 | 昨量 | 振幅 |\n')
f.write('| -------- | -------- | -------- | -------- |-------- | -------- | -------- |-------- |-------- |-------- | -------- | -------- |-------- |\n')

# 代入股票數據
for x in stock_datas:
    f.write('|')
    for y in x:
        f.write(y+'|')
    f.write('\n')

# 代入資料更新時間
f.write("###### 資料更新時間: "+str(datetime.datetime.now(tw).strftime("%Y-%m-%d %H:%M:%S")))
f.close()