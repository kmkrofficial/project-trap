from flask import Flask, render_template
from scrape import get_fundamental_stock_data, get_ohlc_data

app = Flask(__name__)

@app.route("/")
def home():
    ohlc_data = get_ohlc_data("ICICIBANK.NS")
    fundamental_data = get_fundamental_stock_data("ICICIBANK.NS")
    print(ohlc_data)
    print(fundamental_data)
    return render_template("index.html", ohlc_data=ohlc_data, fundamental_data=fundamental_data)

if __name__ == "__main__": 
    app.run(port=8080)