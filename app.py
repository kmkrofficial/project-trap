from flask import Flask, render_template, request, jsonify
from scrape import get_fundamental_stock_data, get_ohlc_data, get_operating_cash_flow_data
from app_util import get_search_result
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import json

app = Flask(__name__)

@app.route("/stock")
def stock():
    if (not request.args.get("stock_symbol")) :
        return jsonify({
            "status" : "failure",
            "data": "Invalid API"
        })
    generic_info = {
        "Stock Name": request.args.get("stock_name"),
        "Stock Symbol": request.args.get("stock_symbol"),
        "Logo": request.args.get("logo"),
        "Sector": request.args.get("sector"),
    }
    stock_name = request.args.get("stock_symbol")
    ohlc_data = get_ohlc_data(stock_name)
    fundamental_data = get_fundamental_stock_data(stock_name)
    cash_flow_info = get_operating_cash_flow_data(stock_name)

    return render_template("stock.html", ohlc_data=ohlc_data, fundamental_data=fundamental_data, cash_flow_info=cash_flow_info, generic_info=generic_info)

@app.route("/", methods=["POST", "GET"])
def home():
    search_results = []
    if request.method == "POST":
        search_results = get_search_result(request.form["searchStock"])
    return render_template("index.html", search_results=search_results if len(search_results) > 0 else None)

@app.route('/fetch_ohlc/<symbol>/<exchange>')
def fetch_ohlc(symbol, exchange):
    # exchange_timezones = {
    #     'NYSE': 'America/New_York',
    #     'NSE': 'Asia/Kolkata',
    #     'LSE': 'Europe/London'
    # }
    exchange_timezones = {
        'NYSE': 'Asia/Kolkata',
        'NSE': 'Asia/Kolkata',
        'LSE': 'Asia/Kolkata'
    }
    timezone = exchange_timezones.get(exchange, 'UTC')
    tz = pytz.timezone(timezone)
    end_date = datetime.now(tz)
    start_date = end_date - timedelta(hours=1)
    
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date, interval='1m')
        if df.empty:
            print(f"No data available for symbol {symbol} from {start_date} to {end_date}")
            previous_close_date = end_date - timedelta(days=1)
            df = ticker.history(start=previous_close_date, end=end_date, interval='1m')
            
            if df.empty:
                return jsonify({
                    'status': 'error',
                    'message': 'No data available for the selected time range'
                })
            
            df = df.tail(60)
        
        data = []
        for index, row in df.iterrows():
            data.append([
                index.strftime('%Y-%m-%d %H:%M'),
                row['Open'],
                row['Close'],
                row['Low'],
                row['High'],
                row['Volume']
            ])
        
        return jsonify({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == "__main__": 
    app.run(port=8080)