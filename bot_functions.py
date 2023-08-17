from datetime import datetime
from config import SYMBOLS
from binance import client
from binance.client import Client
import pandas as pd
from talib import MACD, RSI
import time
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
import numpy as np
from binance.client import Client
import json

def get_symbols(client: Client, leverage: int):
    # Binance'den tüm sembollerin listesini al
    exchange_info = client.futures_exchange_info()
    symbols = SYMBOLS  # config.py dosyasından sembollerin listesini al

    # Debug mesajı: Toplam sembol sayısı
    print(f"Toplam {len(exchange_info['symbols'])} sembol bulundu.")

    # Belirtilen kaldıraç oranına uygun sembollerin listesini oluştur
    for symbol_info in exchange_info['symbols']:
        if symbol_info['symbol'].endswith('USDT'):
            symbols.append(symbol_info['symbol'])
            # Debug mesajı: Sembol ve kaldıraç bilgisi
            print(f"Sembol: {symbol_info['symbol']} | Kaldıraç: {symbol_info.get('leverageFilter', {}).get('maxLeverage', 'Bilinmiyor')}")

    return symbols

def get_high_frequency_data(client: Client, symbols, interval, limit=1000):
    # Semboller için yüksek frekanslı verileri toplama
    data = {}
    for symbol in symbols:
        klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
        data[symbol] = [{
            'open_time': kline[0],
            'open': float(kline[1]),
            'high': float(kline[2]),
            'low': float(kline[3]),
            'close': float(kline[4]),
            'volume': float(kline[5])
        } for kline in klines]

    return data

def analyze_high_frequency_data(processed_data, macd_fast=12, macd_slow=26, macd_signal=9, rsi_period=14):
    macd_line, signal_line, _ = MACD(processed_data['close'], fastperiod=macd_fast, slowperiod=macd_slow, signalperiod=macd_signal)
    rsi_values = RSI(processed_data['close'], timeperiod=rsi_period)
    analysis_results = {
        'macd': macd_line,
        'signal': signal_line,
        'rsi': rsi_values
    }

    return analysis_results


def generate_trade_signals(analysis_results):
    # Gerekirse işlem sinyalleri oluştur
    trade_signals = {}
    for symbol, analysis in analysis_results.items():
        signals = []
        if analysis['macd'].iloc[-1] > analysis['signal'].iloc[-1] and analysis['rsi'].iloc[-1] < 30:
            signals.append({'action': 'BUY', 'quantity': 1})
        elif analysis['macd'].iloc[-1] < analysis['signal'].iloc[-1] and analysis['rsi'].iloc[-1] > 70:
            signals.append({'action': 'SELL', 'quantity': 1})
        trade_signals[symbol] = signals

    return trade_signals

def execute_trades(client: Client, trade_signals, quantity_multiplier=1):
    executed_orders = {}
    for symbol, signals in trade_signals.items():
        orders = []
        for signal in signals:
            side = signal['action']
            quantity = signal['quantity'] * quantity_multiplier
            order_type = 'MARKET'
            try:
                order = client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
                orders.append(order)
                # İşlemi kaydet
                log_trade(symbol, side, quantity, datetime.now())
            except Exception as e:
                print(f"İşlem hatası ({symbol}, {side}): {e}")

        executed_orders[symbol] = orders

    return executed_orders

def advanced_dynamic_risk_management(position, account_info, risk_factor=0.01, max_loss_percent=0.02):
    account_balance = account_info['balance']
    position_size = position['size']
    position_price = position['price']
    stop_loss_price = position_price - (position_price * max_loss_percent)

    risk_amount = account_balance * risk_factor
    risk_position_size = risk_amount / (position_price - stop_loss_price)

    if risk_position_size < position_size:
        # Pozisyon boyutunu azalt
        position['size'] = risk_position_size
    elif risk_position_size > position_size:
        # Pozisyon boyutunu artır
        position['size'] = risk_position_size

    # Yeni durdurma kaybı fiyatını ayarla
    position['stop_loss_price'] = stop_loss_price

    return position

def fetch_high_frequency_data(client, symbol, interval, limit=100):
    # Binance API'dan yüksek frekanslı veri al
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    ohlc_data = []
    for kline in klines:
        ohlc_data.append({
            'open': float(kline[1]),
            'high': float(kline[2]),
            'low': float(kline[3]),
            'close': float(kline[4]),
            'volume': float(kline[5])
        })
    return ohlc_data

def process_single_symbol_data(data):
    # Veriyi işleme kodları
    processed_data = pd.DataFrame({
        'open': [item['open'] for item in data],
        'high': [item['high'] for item in data],
        'low': [item['low'] for item in data],
        'close': [item['close'] for item in data],
        'volume': [item['volume'] for item in data]
    })
    return processed_data

def predict_profit_loss(processed_data, trade_signal):
    # Kar ve zarar tahmininde bulun
    close_prices = processed_data['close']
    current_price = close_prices[-1]
    predicted_price = current_price  # Yapay zeka modeli ile tahmin edilebilir
    if trade_signal['action'] == 'BUY':
        predicted_profit = predicted_price - current_price
    else:
        predicted_profit = current_price - predicted_price
    return predicted_profit

def execute_advanced_trade(client, symbol, trade_signal, processed_data):
    # İşlem yürütme stratejisi
    quantity = trade_signal['quantity']
    side = trade_signal['action']
    predicted_profit = predict_profit_loss(processed_data, trade_signal)
    if predicted_profit > 0:  # Kar bekleniyorsa işlemi yürüt
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        return order
    else:
        print(f"İşlem yürütülmedi, beklenen kar: {predicted_profit}")
        return None

def calculate_dynamic_risk(position, account_info, risk_factor=0.01, max_loss_percent=0.02):
    account_balance = account_info['balance']
    position_size = position['size']
    position_price = position['price']
    stop_loss_price = position_price - (position_price * max_loss_percent)

    risk_amount = account_balance * risk_factor
    risk_position_size = risk_amount / (position_price - stop_loss_price)

    if risk_position_size < position_size:
        # Pozisyon boyutunu azalt
        position['size'] = risk_position_size
    elif risk_position_size > position_size:
        # Pozisyon boyutunu artır
        position['size'] = risk_position_size

    # Yeni durdurma kaybı fiyatını ayarla
    position['stop_loss_price'] = stop_loss_price

    return position

def real_time_monitoring(client, symbols, executed_orders, interval_seconds=5):
    while True:
        for symbol in symbols:
            ticker = client.futures_ticker_symbol(symbol=symbol)  # İlgili sembol için gelecek işlemleri bilgilerini al
            print(f"{symbol}: Fiyat: {ticker['lastPrice']} | Hacim: {ticker['volume']} | Alış: {ticker['bidPrice']} | Satış: {ticker['askPrice']}")

        for order in executed_orders:
            if order['status'] != 'FILLED':
                print(f"Uyarı: {order['symbol']} işlemi dolmadı!")
        time.sleep(interval_seconds)
def prepare_data(data, window_length, batch_size):
    # 'close' değerlerini bir diziye dönüştürme
    close_values = data.values.reshape(-1, 1)

    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(close_values)

    generator = TimeseriesGenerator(data_scaled, data_scaled, length=window_length, batch_size=batch_size)

    return generator, scaler


def create_model(window_length):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(window_length, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(model, data_generator, epochs=1):
    history = model.fit(data_generator, epochs=epochs, verbose=0) # verbose=0, eğitim sırasında her adımdaki çıktıyı gizler
    loss = history.history['loss'][0]
    return loss
        # İsterseniz burada başka istatistikler veya bilgiler de ekleyebilirsiniz.

def predict_future(model, data, symbol, window_length, scaler, future_steps=5):
    if symbol not in data:
        raise KeyError(f"Symbol {symbol} not found in data.")

    symbol_data = data[symbol]
    close_data = [item['close'] for item in symbol_data][-window_length:]
    future_predictions = []
    input_data = np.array(close_data).reshape(1, window_length, 1)
    print(symbol_data)

    for i in range(future_steps):
        prediction = model.predict(input_data)
        future_predictions.append(scaler.inverse_transform(prediction)[0][0])
        input_data = np.append(input_data[0][1:], prediction)
        input_data = input_data.reshape((1, window_length, 1))

    return future_predictions

def log_trade(symbol, action, quantity, timestamp):
    trade = {
        'symbol': symbol,
        'action': action,
        'quantity': quantity,
        'timestamp': str(timestamp)
    }
    with open('trade_history.json', 'a') as file:
        file.write(json.dumps(trade) + '\n')

def log_prediction(symbol, prediction, timestamp):
    prediction_log = {
        'symbol': symbol,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'prediction': [float(p) for p in prediction]  # float32 türünden float türüne dönüştürme
    }

    with open('predictions.log', 'a') as file:
        file.write(json.dumps(prediction_log) + '\n')

