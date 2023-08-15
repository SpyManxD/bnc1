import bot_functions as bf
import config as cfg
import time
import traceback  # For detailed error handling

# Connect to the Binance API and produce a client
client = bf.init_client()

# Load settings from settings.json
settings = cfg.getBotSettings()
symbols = settings.symbols
leverage = int(settings.leverage)
margin_type = settings.margin_type
confirmation_periods = settings.trading_periods.split(",")
trailing_percentage = float(settings.trailing_percentage)

# Main trading loop
try:
    for symbol in symbols:
        for period in confirmation_periods:
            # Retrieve market data
            data = bf.get_data(client, symbol, period)

            # Advanced Strategy Selection: MACD and RSI Combination
            signals = bf.get_macd_rsi_signals(data)

            # High-Frequency Data Processing
            processed_data = bf.process_high_frequency_data(data)

            # Advanced Automatic Trade Execution
            bf.execute_advanced_trades(client, symbol, signals)

            # Advanced Real-time Monitoring and Alerts
            bf.monitor_and_alert(client, symbol)

            time.sleep(1)  # Sleep to avoid hitting the rate limits

    # Advanced Dynamic Risk Management
    bf.dynamic_risk_management(client, symbols)

except Exception as e:
    print("An error occurred while executing the bot:")
    print(str(e))
    print("Stack Trace:")
    traceback.print_exc()  # Printing the detailed stack trace of the error
