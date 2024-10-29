from bs4 import BeautifulSoup
import requests

def make_request(path):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    response = requests.get(f"https://finance.yahoo.com{path}", headers=headers)
    if response.status_code != 200:
        print("MakeRequest : Error has occurred")
        return None
    return BeautifulSoup(response.content, 'html5lib')

def get_ohlc_data(stock_name):
    parsed = make_request(f"/quote/{stock_name}/history/")
    if parsed == None:
        return {
            "status" : "failure",
            "data" : "Unable to retrieve"
        }
    table = parsed.find("table")
    theaders = table.find("thead")
    tbody = table.find("tbody")
    ohlc_data = {}
    for item in theaders.find_all("th"):
        ohlc_data[item.find(string=True).strip()] = []
    ohlc_data_keys = list(ohlc_data.keys())
    for item in tbody.find_all("tr"):
        i = 0
        for col in item.find_all("td"):
            ohlc_data[ohlc_data_keys[i]].append(col.find(string=True))
            i += 1
    return {
        "status" : "success",
        "data" : ohlc_data
    }

def get_fundamental_stock_data(stock_name):
    parsed = make_request(f"/quote/{stock_name}/key-statistics/")
    if parsed == None:
        return {
            "status" : "failure",
            "data" : "Unable to retrieve"
        }
    financial_info = {}
    financial_info_section = parsed.find("div", {"class" : "column yf-14j5zka"})
    
    for item in financial_info_section.find_all("table"):
        for row in item.find_all("tr"):
            key = row.find("td", {"class" : "label"}).find(string=True).strip()
            value = row.find("td", {"class" : "value"}, string=True).find(string=True).strip()
            financial_info[key] = value
    
    return financial_info

# print(get_fundamental_stock_data("DJT"))

# print(get_ohlc_data("DJT"))