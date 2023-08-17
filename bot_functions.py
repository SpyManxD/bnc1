from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from binance.client import Client
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
import time




def fetch_high_frequency_data(client, symbol, interval):
    # Binance API'sinden yüksek frekanslı veri alın
    ohlc_data = client.futures_klines(symbol=symbol, interval=interval)
    return ohlc_data

def process_high_frequency_data(ohlc_data):
    # Veri ön işleme
    close_prices = [x[4] for x in ohlc_data]
    # Veriyi ölçeklendirme
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(np.array(close_prices).reshape(-1, 1))
    return scaled_data, scaler

def create_data_generator(scaled_data, window_length, batch_size):
    # Veri üreteci oluşturma
    # LSTM modeli için zaman serisi verisi oluşturma
    X, y = [], []
    for i in range(window_length, len(scaled_data) - 1):
        X.append(scaled_data[i - window_length:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    data_generator = TimeseriesGenerator(X, y, length=window_length, batch_size=batch_size)
    return data_generator



def generate_trade_signals(analysis_results):
    # İşlem sinyalleri oluşturma
    # Örnek olarak, belirli bir MACD ve RSI kombinasyonuna dayalı sinyaller oluşturabilirsiniz
    trade_signals = {}
    for symbol, result in analysis_results.items():
        if result['MACD'] > 0 and result['RSI'] < 70:
            trade_signals[symbol] = 'BUY'
        elif result['MACD'] < 0 and result['RSI'] > 30:
            trade_signals[symbol] = 'SELL'
    return trade_signals

def execute_trades(client, trade_signals):
    # İşlem sinyallerini kullanarak işlemleri yürütün
    executed_orders = []
    for symbol, signal in trade_signals.items():
        if signal == 'BUY':
            # Alış emri oluştur
            order = client.futures_create_order(symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=1)
        elif signal == 'SELL':
            # Satış emri oluştur
            order = client.futures_create_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=1)
        executed_orders.append(order)
    return executed_orders

def calculate_dynamic_risk_parameters(account_info, symbol_info):
    # Dinamik risk parametrelerini hesapla
    # Örnek olarak, sermayenin belirli bir yüzdesini riske atabilirsiniz
    risk_percentage = 0.01
    capital = float(account_info['balance'])
    risk_amount = capital * risk_percentage
    symbol_price = float(symbol_info['lastPrice'])
    position_size = risk_amount / symbol_price

    # Durdurma kaybı ve kar al seviyeleri belirle
    stop_loss_level = symbol_price * 0.99  # %1 kayıp
    take_profit_level = symbol_price * 1.01  # %1 kar

    return position_size, stop_loss_level, take_profit_level

def execute_trades_with_risk_management(client, trade_signals, account_info):
    # Dinamik risk yönetimi ile işlemleri yürütün
    executed_orders = []
    for symbol, signal in trade_signals.items():
        symbol_info = client.futures_ticker(symbol=symbol)
        position_size, stop_loss_level, take_profit_level = calculate_dynamic_risk_parameters(account_info, symbol_info)
        if signal == 'BUY':
            order = client.futures_create_order(
                symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET,
                quantity=position_size, stopPrice=stop_loss_level, takeProfitPrice=take_profit_level
            )
        elif signal == 'SELL':
            order = client.futures_create_order(
                symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET,
                quantity=position_size, stopPrice=stop_loss_level, takeProfitPrice=take_profit_level
            )
        executed_orders.append(order)
    return executed_orders

def monitor_trades(client, executed_orders):
    # İşlemleri izleme
    for order in executed_orders:
        order_status = client.futures_get_order(symbol=order['symbol'], orderId=order['orderId'])
        print(f"Symbol: {order_status['symbol']}, Status: {order_status['status']}, Executed Quantity: {order_status['executedQty']}, Price: {order_status['price']}")

def alert_conditions(order_status):
    # Uyarı koşulları
    if order_status['status'] == 'FILLED':
        print(f"Order for {order_status['symbol']} has been filled at {order_status['price']}")
    elif order_status['status'] == 'PARTIALLY_FILLED':
        print(f"Order for {order_status['symbol']} has been partially filled at {order_status['price']}")
    elif order_status['status'] == 'CANCELED':
        print(f"Order for {order_status['symbol']} has been canceled")

def real_time_monitoring(client, executed_orders):
    # Gerçek zamanlı izleme ve uyarılar
    while True:
        monitor_trades(client, executed_orders)
        for order in executed_orders:
            order_status = client.futures_get_order(symbol=order['symbol'], orderId=order['orderId'])
            alert_conditions(order_status)
        time.sleep(60)  # Her 1 dakikada bir güncelle

def create_lstm_model(window_length):
    # LSTM modeli oluşturma
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(window_length, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def train_lstm_model(model, data_generator, epochs=10):
    # LSTM modelini eğitme
    model.fit(data_generator, epochs=epochs)
    return model

def predict_with_lstm_model(model, input_data):
    # LSTM modeli ile tahmin yapma
    prediction = model.predict(input_data)
    return prediction

def lstm_based_trading_strategy(client, symbol, interval, window_length, epochs):
    # LSTM tabanlı işlem stratejisi
    ohlc_data = fetch_high_frequency_data(client, symbol, interval)
    scaled_data, scaler = process_high_frequency_data(ohlc_data)
    data_generator = create_data_generator(scaled_data, window_length, batch_size=32)
    model = create_lstm_model(window_length)
    trained_model = train_lstm_model(model, data_generator, epochs)
    input_data = scaled_data[-10:]
    prediction = predict_with_lstm_model(trained_model, input_data)
    # Tahminlere dayalı işlem kararları alınabilir

def hyperparameter_tuning(model, param_grid, data_generator):
    # Hiperparametre ayarlama
    grid = GridSearchCV(estimator=KerasRegressor(build_fn=model, verbose=0), param_grid=param_grid, n_jobs=-1, cv=3)
    grid_result = grid.fit(data_generator)
    return grid_result.best_params_

def adaptive_learning(client, symbol, interval, window_length):
    # Adaptif öğrenme
    ohlc_data = fetch_high_frequency_data(client, symbol, interval)
    scaled_data, scaler = process_high_frequency_data(ohlc_data)
    data_generator = create_data_generator(scaled_data, window_length, batch_size=32)
    model = create_lstm_model(window_length)
    param_grid = {'batch_size': [10, 20, 30, 40], 'epochs': [10, 50, 100]}
    best_params = hyperparameter_tuning(model, param_grid, data_generator)
    trained_model = train_lstm_model(model, data_generator, epochs=best_params['epochs'])
    input_data = scaled_data[-10:]
    prediction = predict_with_lstm_model(trained_model, input_data)    # Tahminlere dayalı işlem kararları alınabilir

