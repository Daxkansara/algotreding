import os
import matplotlib.pyplot as plt

def plot_signals(data, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label=f'{symbol} Closing Price', color='blue')
    buy_signals = data[data['Signal'] == 1]
    sell_signals = data[data['Signal'] == -1]
    plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', alpha=1)
    plt.title(f'{symbol} Buy and Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plot_filename = f'{symbol}_signals_plot.png'
    plot_path = os.path.join('static', 'plots', plot_filename)
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
    return plot_filename
