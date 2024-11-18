import pandas as pd
import numpy as np

# Function to calculate RSI (Relative Strength Index)
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)  # Calculate daily price changes
    gain = np.where(delta > 0, delta, 0)  # Positive gains (only when price increases)
    loss = np.where(delta < 0, -delta, 0)  # Negative losses (only when price decreases)
    
    # Convert gain and loss into 1D arrays
    gain = pd.Series(gain.flatten())  # Ensure it's 1D
    loss = pd.Series(loss.flatten())  # Ensure it's 1D
    
    avg_gain = gain.rolling(window=window, min_periods=1).mean()  # Rolling average gain
    avg_loss = loss.rolling(window=window, min_periods=1).mean()  # Rolling average loss

    rs = avg_gain / avg_loss  # Relative strength (RS)
    rsi = 100 - (100 / (1 + rs))  # RSI formula
    data['RSI'] = rsi
    return data

# Function to calculate Simple Moving Average (SMA)
def calculate_sma(data, window=50):
    data['SMA'] = data['Close'].rolling(window=window).mean()  # Rolling mean for SMA
    return data

# Function to apply technical indicators (RSI and SMA)
def apply_technical_indicators(data):
    data = calculate_rsi(data, window=14)  # Calculate 14-day RSI
    data = calculate_sma(data, window=50)  # Calculate 50-day SMA
    return data

# Function to generate buy/sell signals based on RSI
def generate_signals(data):
    # Buy when RSI < 30, sell when RSI > 70
    data['Signal'] = 0
    data.loc[data['RSI'] < 30, 'Signal'] = 1  # Buy signal
    data.loc[data['RSI'] > 70, 'Signal'] = -1  # Sell signal
    data['Position'] = data['Signal'].shift()  # Shift to represent next-day trading
    return data
