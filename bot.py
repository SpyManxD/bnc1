import bot_functions as bf
import config as cfg
import time
import traceback

# Connect to the Binance API and produce a client
client = bf.init_client()

# Load settings from settings.json
settings = cfg.getBotSettings()
symbols = settings['symbols']
leverage = int(settings['leverage'])
margin_type = settings['margin_type']
trailing_percentage = float(settings['trailing_percentage'])

# Main trading loop
try:
    for symbol in symbols:
        # Retrieve market data
        data = bf.get_data(client, symbol)

        # Check if data is valid
        if data is None:
            print(f"Failed to retrieve data for {symbol}")
            continue

        # Advanced Strategy Selection: MACD and RSI Combination
        signals = bf.get_macd_rsi_signals(data)

        # Check if signals are valid
        if signals is None:
            print(f"Failed to generate signals for {symbol}")
            continue

        # High-Frequency Data Processing
        processed_data = bf.process_high_frequency_data(data)

        # Advanced Automatic Trade Execution
        bf.execute_advanced_trades(client, symbol, signals, leverage, margin_type, trailing_percentage)

        time.sleep(1)  # Sleep to avoid hitting the rate limits

    # Advanced Dynamic Risk Management
    bf.dynamic_risk_management(client, symbols)

except Exception as e:
    print("An error occurred while executing the bot:")
    print(str(e))
    print("Stack Trace:")
    traceback.print_exc()
