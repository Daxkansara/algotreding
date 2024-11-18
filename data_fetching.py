import yfinance as yf

def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print(f"Error fetching stock data for {symbol}: {e}")
        return None

def get_live_prices(symbols):
    live_prices = {}
    try:
        # Attempt to fetch live prices in bulk
        live_data = yf.download(tickers=" ".join(symbols), period='1d')['Close']
        
        # Populate live_prices dictionary with data fetched in bulk
        live_prices.update({symbol: round(live_data[symbol].iloc[-1], 3) for symbol in live_data.columns})
        
        # Identify symbols that didn't return data
        missing_symbols = [symbol for symbol in symbols if symbol not in live_prices]
        
        # Fallback to individual fetch for missing symbols
        for symbol in missing_symbols:
            try:
                ticker = yf.Ticker(symbol)
                price = ticker.history(period='1d')['Close']
                if not price.empty:
                    live_prices[symbol] = round(price.iloc[-1], 3)
                else:
                    print(f"No data available for {symbol}")
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")

    except Exception as e:
        print(f"Error fetching live prices: {e}")
    
    return live_prices
