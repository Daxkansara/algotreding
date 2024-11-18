from flask import Flask, render_template, request, url_for, jsonify
import yfinance as yf
from data_fetching import get_stock_data
from strategy import apply_technical_indicators, generate_signals
from plot_results import plot_signals
import os
import json

app = Flask(__name__)

# Cache directory and stock list path
CACHE_DIR = "cache"
STOCK_LIST_PATH = os.path.join(CACHE_DIR, "all_stock_symbols.json")
PLOTS_DIR = 'static/plots'

# Ensure necessary directories exist
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# Load or fetch all stock symbols
def load_all_stock_symbols():
    if os.path.exists(STOCK_LIST_PATH):
        with open(STOCK_LIST_PATH, "r") as f:
            symbols = json.load(f)
    else:
        # Placeholder: Fetch symbols from a reliable source or API
        symbols = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "BABA", "V",
    "JPM", "JNJ", "WMT", "PG", "DIS", "MA", "HD", "PYPL", "INTC", "CSCO",
    "CMCSA", "PFE", "KO", "PEP", "NKE", "MRK", "XOM", "VZ", "ABBV", "T"
]
  # Example list
        with open(STOCK_LIST_PATH, "w") as f:
            json.dump(symbols, f)
    return symbols

STOCKS = load_all_stock_symbols()
# Fetch live prices
def get_live_prices(symbols):
    live_prices = {}
    try:
        live_data = yf.download(tickers=" ".join(symbols), period='1d')['Close']
        live_prices = {symbol: round(live_data[symbol].iloc[-1], 3) for symbol in symbols if symbol in live_data.columns}
    except Exception as e:
        print(f"Error fetching live prices: {e}")
    return live_prices

@app.route("/", methods=["GET"])
def index():
    live_prices = get_live_prices(STOCKS[:5])  # Display a few stock prices on the homepage
    return render_template("index.html", live_prices=live_prices)

@app.route("/fetch-prices", methods=["GET"])
def fetch_prices():
    # Fetch live prices dynamically for frontend updates
    live_prices = get_live_prices(STOCKS[:5])
    return jsonify(live_prices)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").upper()
    filtered_stocks = [symbol for symbol in STOCKS if query in symbol]
    return render_template("search.html", stocks=filtered_stocks)

@app.route("/stock/<symbol>", methods=["GET"])
def stock_detail(symbol):
    stock_data = get_stock_data(symbol, '2022-01-01', '2023-01-01')
    stock_data = apply_technical_indicators(stock_data)
    stock_data = generate_signals(stock_data)
    plot_filename = plot_signals(stock_data, symbol)
    plot_url = url_for('static', filename=f'plots/{plot_filename}')
    current_price = stock_data['Close'].iloc[-1]
    prediction_price = round(float(current_price * 1.05), 2)
    return render_template("stock_detail.html", symbol=symbol, stock_data=stock_data, 
                           plot_url=plot_url, prediction_price=prediction_price)
  
@app.route("/fetch-symbols", methods=["GET"])
def fetch_symbols():
    return jsonify({"symbols": STOCKS})

@app.route('/run-backtest', methods=['GET'])
def run_backtest():
    stock = request.args.get('stock')
    strategy = request.args.get('strategy')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Simulate a backtest result for demonstration purposes
    result = {
        "summary": f"Backtest for {stock} using {strategy} strategy from {start_date} to {end_date} completed successfully."
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
