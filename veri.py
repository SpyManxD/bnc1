import bot_functions
import config
from binance.client import Client
import pandas as pd

# Binance istemcisini oluşturun
client = Client(config.API_KEY, config.API_SECRET)

# İlgili semboller
symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]

# Verileri toplama
data = {}
for symbol in symbols:
    data[symbol] = bot_functions.fetch_high_frequency_data(client, symbol, '1m') # Örnek zaman dilimi '1m'

# Verileri işleme
processed_data = {}
for symbol, ohlc_data in data.items():
    processed_data[symbol] = pd.DataFrame(ohlc_data) # Verileri DataFrame'e dönüştürme

# Analiz sonuçlarını alın
analysis_results = bot_functions.analyze_high_frequency_data(processed_data)

# Sonuçları yazdırın
for symbol, results in analysis_results.items():
    print(f"{symbol} için MACD: {results['macd']}")
    print(f"{symbol} için Sinyal: {results['signal']}")
    print(f"{symbol} için RSI: {results['rsi']}")
