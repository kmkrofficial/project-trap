from bs4 import BeautifulSoup
import requests

def get_ohlc_data(stock_name):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    response = requests.get(f"https://finance.yahoo.com/quote/{stock_name}/history/", headers=headers)
    if response.status_code != 200:
        print("Error has occurred")
        return {
            "status" : "failure",
            "data" : "Unable to retrieve"
        }
    parsed = BeautifulSoup(response.content, 'html5lib')
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

print(get_ohlc_data("DJT"))