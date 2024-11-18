
@app.route("/run-backtest", methods=["GET"])
def run_backtest():
    stock = request.args.get("stock")
    strategy = request.args.get("strategy")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Validate inputs
    if not (stock and strategy and start_date and end_date):
        return jsonify({"error": "Missing required parameters"}), 400

    # Run your backtest logic here and return results
    results = simulate_backtest(stock, strategy, start_date, end_date)
    return jsonify({"summary": results})


def simulate_backtest(stock, strategy, start_date, end_date):
    # Placeholder for real historical price data
    # Here you might fetch historical prices for the stock
    # In this simulation, we’ll use random data for demonstration purposes

    # Simulate basic metrics
    total_return = round(random.uniform(5, 20), 2)  # Simulated return percentage
    max_drawdown = round(random.uniform(2, 10), 2)  # Simulated drawdown percentage

    # Generate random trade data as an example
    trade_summary = [
        {
            "entry_date": "2023-03-01",
            "exit_date": "2023-03-10",
            "profit": f"{round(random.uniform(1, 3), 2)}%"
        },
        {
            "entry_date": "2023-04-15",
            "exit_date": "2023-04-20",
            "profit": f"{round(random.uniform(1, 3), 2)}%"
        }
    ]

    # Simulate strategy-specific results
    if strategy == "ma":
        description = f"Moving Average backtest for {stock} from {start_date} to {end_date}"
    elif strategy == "rsi":
        description = f"RSI backtest for {stock} from {start_date} to {end_date}"
    else:
        description = f"Backtest for {stock} using {strategy} strategy from {start_date} to {end_date}"

    # Create result structure
    result = {
        "description": description,
        "total_return": f"{total_return}%",
        "max_drawdown": f"{max_drawdown}%",
        "trade_summary": trade_summary
    }

    return result
