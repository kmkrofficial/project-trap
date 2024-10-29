from flask import Flask, render_template, request, jsonify
from scrape import get_fundamental_stock_data, get_ohlc_data, get_operating_cash_flow_data
from app_util import get_search_result

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

if __name__ == "__main__": 
    app.run(port=8080)