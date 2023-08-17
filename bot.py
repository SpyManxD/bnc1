from binance.client import Client
from bot_functions import *

# Binance API anahtarları
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

# İşlem yapılacak semboller
symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']

# İşlem parametreleri
interval = "1m"  # 1 dakikalık zaman dilimi
window_length = 10  # LSTM pencere uzunluğu
epochs = 50  # LSTM eğitim dönemi

# Binance istemcisini oluşturma
client = Client(api_key, api_secret)

# İşlem döngüsü
while True:
    for symbol in symbols:
        # Veri toplama
        ohlc_data = fetch_high_frequency_data(client, symbol, interval)

        # Veri işleme
        scaled_data, scaler = process_high_frequency_data(ohlc_data)

        # LSTM tabanlı işlem stratejisi
        lstm_based_trading_strategy(client, symbol, interval, window_length, epochs)

        # Gerçek zamanlı izleme
        real_time_monitoring(client, executed_orders)

        # Adaptif öğrenme
        adaptive_learning(client, symbol, interval, window_length)

    time.sleep(60)  # Her sembol için 1 dakikalık bekleme süresi
