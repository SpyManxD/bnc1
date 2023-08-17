from datetime import datetime
from tqdm import tqdm
import pandas as pd
from binance.client import Client
from bot_functions import prepare_data, generate_trade_signals
import bot_functions
import config
import time

def main():
    global trade_signals, ohlc_data, SYMBOLS
    trade_signals = {}  # trade_signals'ı boş bir sözlük olarak tanımlayın
    window_length = 60  # Örnek bir değer
    batch_size = 32  # Örnek bir değer
    client = Client(config.API_KEY, config.API_SECRET)  # Binance client'ını oluştur
    print("Semboller alınıyor...")  # Debug mesajı
    symbols = config.SYMBOLS
    print("Semboller alınıyor...")
    print(f"{len(symbols)} sembol bulundu.")

    processed_data = {}  # Boş bir sözlük

    for symbol in symbols:
        ohlc_data = bot_functions.fetch_high_frequency_data(client, symbol, '1m')
        processed_data[symbol] = bot_functions.process_single_symbol_data(ohlc_data)  # Verileri işle
        print(f"{symbol} işleniyor...")  # Debug mesajı
        # Verinin neye benzediğini kontrol etmek için yazdırın
        print(ohlc_data)
        # Verileri DataFrame'e dönüştürme
        processed_data_df = pd.DataFrame(ohlc_data)
        # Veri üreteci ve ölçekleyici oluşturma
        data_generator, scaler = bot_functions.prepare_data(processed_data_df['close'], window_length, batch_size)
        # Analiz sonuçlarını alın
        analysis_results = bot_functions.analyze_high_frequency_data(processed_data_df)
        # Model oluşturma
        model = bot_functions.create_model(window_length)
        # Modeli eğitme
        for epoch in range(100):
            if epoch % 10 == 0:  # Her 10 dönemde bir yazdır
                print(f"Epoch {epoch}/100")
            loss = bot_functions.train_model(model, data_generator, epochs=1)  # Her seferinde bir dönem eğit
            if epoch % 10 == 0:  # Her 10 dönemde bir yazdır
                print(f"Loss: {loss:.4f}")

            prediction = bot_functions.predict_future(model, processed_data, symbol, window_length, scaler, future_steps=5)
            # Tahminleri kaydet
            bot_functions.log_prediction(symbol, prediction, datetime.now())

            trade_signals = bot_functions.generate_trade_signals(analysis_results)
            # İşlem sinyallerini kullanarak işlemleri yürütün
            executed_orders = bot_functions.execute_trades(client, trade_signals)
            print(f"Yürütülen işlemler: {executed_orders}")
            trade_signals = bot_functions.analyze_high_frequency_data(analysis_results, trade_signals)
            bot_functions.real_time_monitoring(executed_orders)
            # Bekleme süresi (isteğe bağlı)
        time.sleep(1)

if __name__ == "__main__":
    main()
