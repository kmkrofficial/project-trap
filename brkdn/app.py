# app.py
from flask import Flask, render_template, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_ohlc/<symbol>/<exchange>')
def fetch_ohlc(symbol, exchange):
    # Define time zones for different exchanges
    exchange_timezones = {
        'NYSE': 'America/New_York',
        'NSE': 'Asia/Kolkata',
        'LSE': 'Europe/London'
    }
    
    # Get the appropriate time zone
    timezone = exchange_timezones.get(exchange, 'UTC')
    tz = pytz.timezone(timezone)
    
    # Get data for the last hour with 1-minute intervals
    end_date = datetime.now(tz)
    start_date = end_date - timedelta(hours=1)
    
    try:
        # Fetch data from yfinance
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date, interval='1m')
        
        # Check if data is available
        if df.empty:
            logging.warning(f"No data available for symbol {symbol} from {start_date} to {end_date}")
            
            # Fetch last 60 bars from the previous close
            previous_close_date = end_date - timedelta(days=1)
            df = ticker.history(start=previous_close_date, end=end_date, interval='1m')
            
            # Check if data is available after fetching from previous close
            if df.empty:
                return jsonify({
                    'status': 'error',
                    'message': 'No data available for the selected time range'
                })
            
            # Limit to last 60 bars
            df = df.tail(60)
        
        # Format data for ECharts
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
        logging.error(f"Error fetching data for symbol {symbol}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)