import pandas as pd

def simulate_trades(data, initial_capital=10000):
    # DataFrame to store trades and portfolio value
    trades = pd.DataFrame(index=data.index)
    trades['Close'] = data['Close']
    trades['Position'] = data['Position'].fillna(0)

    # Daily returns based on price changes and position (1 for buy, -1 for sell)
    trades['Returns'] = trades['Close'].pct_change() * trades['Position']

    # Calculate portfolio value over time
    trades['Portfolio Value'] = (1 + trades['Returns']).cumprod() * initial_capital
    return trades
