import os
import sys
import pandas as pd
from binance.client import Client
import config as cfg

# Redirects stdout to null to disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restores stdout to enable print
def enablePrint():
    sys.stdout = sys.__stdout__

# Prints a single line to stdout
def singlePrint(string):
    enablePrint()
    print(string)
    blockPrint()

def get_macd_rsi_signals(data):
    # Eğer data bir liste ise, bir DataFrame'e dönüştür
    if isinstance(data, list):
        # Sütun adlarını veri yapısına uygun olarak değiştirin
        data = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignored'])
        data[['open', 'high', 'low', 'close', 'volume']] = data[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)

    macd, signal_line = calculate_macd(data)
    rsi = calculate_rsi(data)
    signals = []
    for i in range(len(data)):
        if macd[i] > signal_line[i] and rsi[i] < 30:
            signals.append('BUY')
        elif macd[i] < signal_line[i] and rsi[i] > 70:
            signals.append('SELL')
        else:
            signals.append('HOLD')
    return signals

# p3Binance\bot_functions.py dosyası

def calculate_macd(data):
    # Eğer data bir liste ise, bir DataFrame'e dönüştür
    if isinstance(data, list):
        # Sütun adlarını veri yapısına uygun olarak değiştirin
        data = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignored'])
        data[['open', 'high', 'low', 'close', 'volume']] = data[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)

    short_window = 12
    long_window = 26

    short_ema = data['close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['close'].ewm(span=long_window, adjust=False).mean()

    macd = short_ema - long_ema
    signal_line = macd.ewm(span=9, adjust=False).mean()

    return macd, signal_line


def get_data(client, symbol):
    # Belirli bir sembol için tarihsel fiyat verilerini alın
    # Örnek olarak, son 100 mumun 1 dakikalık verilerini alabilirsiniz
    klines = client.futures_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1MINUTE, limit=100)

    # Verileri uygun bir biçime dönüştürün (örneğin, pandas DataFrame)
    data = {
        'timestamp': [int(k[0]) for k in klines],
        'open': [float(k[1]) for k in klines],
        'high': [float(k[2]) for k in klines],
        'low': [float(k[3]) for k in klines],
        'close': [float(k[4]) for k in klines],
        'volume': [float(k[5]) for k in klines]
    }

    return data

# Initializes the Binance client
def init_client():
    keys = cfg.getAPIKeys()
    client = Client(keys.api_key, keys.api_secret, {"verify": True, "timeout": 20})
    return client

# Function to get the liquidation price for a given market
def get_liquidation(client, symbol):
    # Example logic to retrieve liquidation price
    liquidation_price = client.futures_mark_price(symbol=symbol)['markPrice']
    return float(liquidation_price)

# Function to get the entry price of the position the bot entered
def get_entry(client, symbol):
    # Example logic to retrieve entry price
    entry_price = client.futures_position_information(symbol=symbol)[0]['entryPrice']
    return float(entry_price)

# Function to execute an order
def execute_order(client, symbol, order_type, side, position_side, quantity):
    # Example logic to execute the order
    order = client.futures_create_order(symbol=symbol, side=side, type=order_type, positionSide=position_side, quantity=quantity)
    return order

# Rounds a number to the given precision
def round_to_precision(number, precision):
    return round(number, precision)

# Converts candles to a DataFrame with open, high, low, close, and volume columns
def convert_candles(candles):
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignored'])
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)
    return df

# Calculates the Relative Strength Index (RSI) indicator
def calculate_rsi(data, window=14):
    delta = data['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Processes high-frequency data and returns processed data
def process_high_frequency_data(data):
    # Example logic to process high-frequency data
    # This can be customized based on specific requirements
    processed_data = data.resample('1T').ohlc()
    return processed_data

# Executes advanced trades based on the given signals
def execute_advanced_trades(client, symbol, signals, leverage, margin_type, trailing_percentage):
    # Example logic to execute advanced trades
    # This can be customized based on specific requirements
    for signal in signals:
        if signal == 'BUY':
            execute_order(client, symbol, 'MARKET', 'BUY', 'LONG', leverage)
        elif signal == 'SELL':
            execute_order(client, symbol, 'MARKET', 'SELL', 'SHORT', leverage)
        # Add logic for trailing stop-loss, margin type, etc.

# Monitors the market and sends alerts in real-time
def monitor_and_alert(client, symbol):
    # Example logic to monitor the market and send alerts
    # This can be customized based on specific requirements
    current_price = client.futures_ticker_price(symbol=symbol)['price']
    singlePrint(f"Current price for {symbol}: {current_price}")

# Implements dynamic risk management strategies
def dynamic_risk_management(client, symbols):
    # Example logic to implement dynamic risk management
    # This can be customized based on specific requirements
    for symbol in symbols:
        position = client.futures_position_information(symbol=symbol)[0]
        # Add logic to adjust position size, stop-loss, etc., based on risk parameters

# Implements advanced multi-symbol support
def advanced_multi_symbol_support(client, symbols):
    # Example logic to implement advanced multi-symbol support
    # This can be customized based on specific requirements
    for symbol in symbols:
        candles = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
        data = convert_candles(candles)
        signals = get_macd_rsi_signals(data)
        execute_advanced_trades(client, symbol, signals, leverage=20, margin_type='Cross', trailing_percentage=1)

# Implements advanced automatic trade execution
def advanced_automatic_trade_execution(client, symbol):
    # Infinite loop to continuously monitor and trade
    while True:
        # Get the latest candlestick data for the symbol
        candles = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
        data = convert_candles(candles) # Assuming you have a function to convert candles to the required data format

        # Get trading signals based on MACD and RSI
        signals = get_macd_rsi_signals(data)

        # Execute trades based on the signals
        execute_advanced_trades(client, symbol, signals, leverage=20, margin_type='Cross', trailing_percentage=1)


# Main function to run the bot
def run_bot():
    client = init_client()
    symbols = ["SUSHIUSDT", "BTSUSDT", "INJUSDT", "BNTUSDT", "RDNTUSDT", "ZRXUSDT", "HIGHUSDT", "WAVESUSDT", "SPELLUSDT", "XTZUSDT", "DARUSDT", "JOEUSDT", "XMRUSDT", "PENDLEUSDT", "ALICEUSDT", "HOOKUSDT", "REEFUSDT", "BATUSDT", "DOGEUSDT", "TRXUSDT", "STORJUSDT", "SNXUSDT", "XLMUSDT", "IOTXUSDT", "DASHUSDT", "UMAUSDT", "KAVAUSDT", "OXTUSDT", "RUNEUSDT", "APEUSDT", "BLUEBIRDUSDT", "BNXUSDT", "OPUSDT", "KEYUSDT", "DGBUSDT", "SKLUSDT", "FOOTBALLUSDT", "TOMOUSDT", "MTLUSDT", "ETHBTC", "KSMUSDT", "BNBBUSD", "TRBUSDT", "MANAUSDT", "FLOWUSDT", "CHRUSDT", "GALUSDT", "USDCUSDT", "OGNUSDT", "RNDRUSDT", "SCUSDT", "KNCUSDT", "BLURUSDT", "ENJUSDT", "ATOMUSDT", "SOLBUSD", "NMRUSDT", "ENSUSDT", "ATAUSDT", "AGIXUSDT", "IOSTUSDT", "HBARUSDT", "ZECUSDT", "IDEXUSDT", "GALAUSDT", "EDUUSDT", "GTCUSDT", "ALGOUSDT", "LRCUSDT", "STGUSDT", "STXUSDT", "ARPAUSDT", "CELOUSDT", "QNTUSDT", "1INCHUSDT", "TUSDT", "LINAUSDT", "ARUSDT", "FILUSDT", "DODOXUSDT", "SOLUSDT", "COMBOUSDT", "GMTUSDT", "MDTUSDT", "XVSUSDT", "GMXUSDT", "BANDUSDT", "LDOUSDT", "XRPBUSD", "CRVUSDT", "BELUSDT", "ONEUSDT", "APTUSDT", "ANKRUSDT", "MAVUSDT", "RAYUSDT", "API3USDT", "ASTRUSDT", "HOTUSDT", "QTUMUSDT", "IOTAUSDT", "BTCBUSD", "LITUSDT", "YFIUSDT", "ETHUSDT", "ALPHAUSDT", "WOOUSDT", "SFPUSDT", "RLCUSDT", "BTCSTUSDT", "1000XECUSDT", "FXSUSDT", "CFXUSDT", "AUDIOUSDT", "IDUSDT", "HFTUSDT", "NEOUSDT", "UNFIUSDT", "SANDUSDT", "CTKUSDT", "MINAUSDT", "CELRUSDT", "AGLDUSDT", "RSRUSDT", "RENUSDT", "JASMYUSDT", "PHBUSDT", "YGGUSDT", "EGLDUSDT", "LUNA2USDT", "ONTUSDT", "VETUSDT", "IMXUSDT", "LQTYUSDT", "COTIUSDT", "CVXUSDT", "ARBUSDT", "BAKEUSDT", "GRTUSDT", "FLMUSDT", "MASKUSDT", "BALUSDT", "SUIUSDT", "DENTUSDT", "TRUUSDT", "CKBUSDT", "SSVUSDT", "C98USDT", "ZENUSDT", "NEARUSDT", "1000SHIBUSDT", "ANTUSDT", "ETHBUSD", "TLMUSDT", "AAVEUSDT", "ICPUSDT", "1000LUNCUSDT", "RADUSDT", "AVAXUSDT", "MAGICUSDT", "ROSEUSDT", "MATICUSDT",	"XVGUSDT", "MKRUSDT", "PEOPLEUSDT", "THETAUSDT", "UNIUSDT", "PERPUSDT", "RVNUSDT", "ARKMUSDT", "NKNUSDT", "KLAYUSDT", "DEFIUSDT", "COMPUSDT", "BTCDOMUSDT", "BTCUSDT", "OMGUSDT", "ICXUSDT", "1000PEPEUSDT", "FETUSDT", "LEVERUSDT", "1000FLOKIUSDT", "FTMUSDT", "DOGEBUSD", "SXPUSDT", "XEMUSDT", "WLDUSDT", "ZILUSDT", "AXSUSDT", "DYDXUSDT", "OCEANUSDT", "CHZUSDT", "DUSKUSDT", "CTSIUSDT", "ACHUSDT"]
    advanced_multi_symbol_support(client, symbols)
    monitor_and_alert(client, 'BTCUSDT')
    dynamic_risk_management(client, symbols)

if __name__ == "__main__":
    run_bot()
