import logging
from datetime import datetime
import math
import numpy as np
import talib
from talib import MACD, RSI
from binance.client import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def analyze_symbols(client, symbol):
    # Veriyi al
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE)
    close = [ float(entry[ 4 ]) for entry in klines ]
    close_array = np.asarray(close)

    # MACD hesaplama
    macd, signal, _ = talib.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)

    # RSI hesaplama
    rsi = talib.RSI(close_array, timeperiod=14)

    return {'macd': macd[ -1 ], 'signal': signal[ -1 ], 'rsi': rsi[ -1 ]}

def determine_side(analysis_result):
    if analysis_result[ 'macd' ] > analysis_result[ 'signal' ] and analysis_result[ 'rsi' ] < 30:
        return 'BUY'
    elif analysis_result[ 'macd' ] < analysis_result[ 'signal' ] and analysis_result[ 'rsi' ] > 70:
        return 'SELL'
    else:
        return None

def execute_trade(client, symbol, quantity, side):
    order_type = 'MARKET'
    try:
        if side == 'BUY':
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity
            )
        elif side == 'SELL':
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity
            )
        return order
    except Exception as e:
        print(f"İşlem hatası: {e}")
        return None

def process_tick_data(tick_data):
    # Veriyi işleme kodları
    processed_data = {
        'open': tick_data[ 'open' ],
        'high': tick_data[ 'high' ],
        'low': tick_data[ 'low' ],
        'close': tick_data[ 'close' ],
        'volume': tick_data[ 'volume' ]
    }
    return processed_data

def analyze_high_frequency_data(processed_data):
    # İlgili analizler ve stratejiler
    macd, signal, hist = MACD(processed_data[ 'close' ])
    rsi = RSI(processed_data[ 'close' ])
    analysis_result = {
        'macd': macd,
        'signal': signal,
        'hist': hist,
        'rsi': rsi
    }
    return analysis_result

def generate_trade_signals(processed_data):
    # Gerekirse işlem sinyalleri oluştur
    analysis_result = analyze_high_frequency_data(processed_data)
    trade_signals = [ ]
    if analysis_result[ 'macd' ] > analysis_result[ 'signal' ] and analysis_result[ 'rsi' ] < 30:
        trade_signals.append({'action': 'BUY', 'quantity': 1})
    elif analysis_result[ 'macd' ] < analysis_result[ 'signal' ] and analysis_result[ 'rsi' ] > 70:
        trade_signals.append({'action': 'SELL', 'quantity': 1})
    return trade_signals

def calculate_RSI(data, window_length):
    # RSI Hesaplaması için kullanılır.
    # Delta değerini hesapla
    delta = data['close'].diff(1)

    # Kazanç ve kaybı ayırmak için pozitif ve negatif deltaları hesapla
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))

    # Ortalama kazanç ve kaybı hesapla
    avg_gain = gain.rolling(window=window_length, min_periods=1).mean()
    avg_loss = loss.rolling(window=window_length, min_periods=1).mean()

    # RSI değerini hesapla
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def calculate_MACD(data, short_window_length, long_window_length, signal_length):
    # MACD Hesaplaması için kullanılır.
    # Kısa ve uzun hareketli ortalamaları hesapla
    short_ema = data['close'].ewm(span=short_window_length, adjust=False).mean()
    long_ema = data['close'].ewm(span=long_window_length, adjust=False).mean()

    # MACD değerini hesapla
    macd = short_ema - long_ema

    # MACD sinyalini hesapla
    signal = macd.ewm(span=signal_length, adjust=False).mean()

    return macd, signal

def check_advanced_MACD_RSI_combination(data, window_length_rsi, short_window_length_macd, long_window_length_macd, signal_length_macd):
    # Gelişmiş MACD ve RSI kombinasyonu için kullanılır.
    # RSI ve MACD değerlerini hesapla
    rsi = calculate_RSI(data, window_length_rsi)
    macd, signal = calculate_MACD(data, short_window_length_macd, long_window_length_macd, signal_length_macd)

    # MACD ve sinyal çizgisinin kesişimini kontrol et
    crossover = (macd > signal) & (macd.shift(1) <= signal.shift(1))

    # MACD ve sinyal çizgisinin ters kesişimini kontrol et
    crossover_down = (macd < signal) & (macd.shift(1) >= signal.shift(1))

    # MACD ve RSI stratejisinin birleşimini uygula
    buy_signal = crossover & (rsi < 30)
    sell_signal = crossover_down & (rsi > 70)

    return buy_signal, sell_signal

def real_time_monitoring_alert(client: Client, symbol: str, email_address: str, threshold_price: float):
    # Gerçek zamanlı fiyat alın
    price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    print(f"{symbol} şu anki fiyatı: {price}")

    # Fiyat belirtilen eşiğin altındaysa bir uyarı e-postası gönderin
    if price <= threshold_price:
        message = MIMEMultipart()
        message["Subject"] = f"{symbol} fiyatı düştü!"
        message["From"] = 'your_email@example.com'  # Gönderici e-posta adresi
        message["To"] = email_address

        body = f"{symbol} fiyatı {price} oldu. İlgili işlemleri kontrol etmek isteyebilirsiniz."
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP('smtp.example.com', 587)  # Kullandığınız SMTP sunucusunun adresi
        server.starttls()
        server.login('your_email@example.com', 'your_password')  # Gönderici e-posta girişi
        server.sendmail('your_email@example.com', email_address, message.as_string())
        server.quit()

        print(f"{symbol} fiyatı {threshold_price} altına düştü! E-posta gönderildi.")

def advanced_dynamic_risk_management(position, account_info):
    risk_factor = 0.01
    max_loss_percent = 0.02

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
