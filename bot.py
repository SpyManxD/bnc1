from binance.client import Client
from bot_functions import BinanceBot
from config import getAPIKeys, getBotSettings

# API anahtarlarını al
api_keys = getAPIKeys()

# Binance istemcisini oluştur
client = Client(api_keys.API_KEY, api_keys.API_SECRET)

# Bot ayarlarını al
bot_settings = getBotSettings()

# BinanceBot sınıfını oluştur
bot = BinanceBot(client, bot_settings)

# Sembollerin listesini al
symbols = bot_settings['symbols']

# Her sembol için analiz ve işlem yap
for symbol in symbols:
    # Sembol verilerini al
    symbol_data = bot.get_symbol_data(symbol)

    # MACD ve RSI göstergelerini hesapla
    macd, signal_line, rsi = bot.calculate_indicators(symbol_data)

    # Alım satım sinyallerini belirle
    buy_signal, sell_signal = bot.generate_signals(macd, signal_line, rsi)

    # Sinyallere göre işlem yap
    bot.execute_trades(symbol, buy_signal, sell_signal)

    # İzleme ve uyarıları ayarla
    bot.monitor_and_alert(symbol)

# BinanceBot sınıfının devamı

class BinanceBot:
    # Diğer metodlar...

    def get_symbol_data(self, symbol):
        # Sembol verilerini almak için kodlar
        # Örnek olarak, son 100 mum verisini alabilirsiniz
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)
        return klines

    def calculate_macd(self, symbol_data):
        # MACD hesaplama
        close_prices = [float(data[4]) for data in symbol_data]
        short_ema = self.calculate_ema(close_prices, self.settings['macd_short_window'])
        long_ema = self.calculate_ema(close_prices, self.settings['macd_long_window'])
        macd = [short - long for short, long in zip(short_ema, long_ema)]
        signal_line = self.calculate_ema(macd, self.settings['macd_signal_window'])
        return macd, signal_line
    def calculate_rsi(self, symbol_data):
        # RSI hesaplama
        close_prices = [float(data[4]) for data in symbol_data]
        gains = [close_prices[i] - close_prices[i - 1] if close_prices[i] > close_prices[i - 1] else 0 for i in range(1, len(close_prices))]
        losses = [close_prices[i - 1] - close_prices[i] if close_prices[i] < close_prices[i - 1] else 0 for i in range(1, len(close_prices))]
        avg_gain = sum(gains[-self.settings['rsi_window']:]) / self.settings['rsi_window']
        avg_loss = sum(losses[-self.settings['rsi_window']:]) / self.settings['rsi_window']
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_ema(self, data, window):
        # EMA hesaplama
        ema = [sum(data[:window]) / window]
        multiplier = 2 / (window + 1)
        for i in range(window, len(data)):
            ema.append((data[i] - ema[-1]) * multiplier + ema[-1])
        return ema

    def buy(self, symbol):
        # Alım işlemi
        order = self.client.futures_create_order(symbol=symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=1)
        print(f"Alım işlemi gerçekleştirildi: {order}")

    def sell(self, symbol):
        # Satım işlemi
        order = self.client.futures_create_order(symbol=symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=1)
        print(f"Satım işlemi gerçekleştirildi: {order}")

    def generate_signals(self, macd, signal_line, rsi):
        # Alım satım sinyallerini belirlemek için kodlar
        # Örnek olarak, MACD ve RSI'ya göre alım satım sinyalleri oluşturabilirsiniz
        buy_signal = macd > signal_line and rsi < 30
        sell_signal = macd < signal_line and rsi > 70
        return buy_signal, sell_signal

    def analyze_symbol(self, symbol):
        # Sembol analizi
        symbol_data = self.get_symbol_data(symbol)
        macd, signal_line = self.calculate_macd(symbol_data)
        rsi = self.calculate_rsi(symbol_data)

        # Alım satım sinyallerini belirlemek için kodlar
        buy_signal = macd[-1] > signal_line[-1] and rsi < 30
        sell_signal = macd[-1] < signal_line[-1] and rsi > 70

        # Sinyallere göre işlem yapmak için kodlar
        if buy_signal:
            self.buy(symbol)
        elif sell_signal:
            self.sell(symbol)

        # İzleme ve uyarıları ayarlamak için kodlar
        self.monitor_and_alert(symbol)

    def execute_trades(self, symbol, buy_signal, sell_signal):
        # Sinyallere göre işlem yapmak için kodlar
        # Örnek olarak, alım ve satım sinyallerine göre işlemleri yürütebilirsiniz
        if buy_signal:
            self.buy(symbol)
        elif sell_signal:
            self.sell(symbol)

    def monitor_and_alert(self, symbol):
        # İzleme ve uyarıları ayarlamak için kodlar
        current_price = self.get_current_price(symbol)
        if current_price > self.target_price[symbol]:
            alert_message = f"{symbol} hedef fiyatı aştı! Şu anki fiyat: {current_price}"
            self.send_email_alert(alert_message)
            self.log_info(alert_message)
            # İhtiyaca göre hedef fiyatı güncelleme veya diğer işlemler
    def send_email_alert(self, message):
        # Uyarı mesajını e-posta olarak gönderme
        email = EmailMessage()
        email.set_content(message)
        email["Subject"] = "Binance Bot Uyarısı"
        email["From"] = "your-email@example.com"
        email["To"] = "recipient@example.com"

        with smtplib.SMTP_SSL("smtp.example.com", 465) as smtp:
            smtp.login("your-email@example.com", "your-password")
            smtp.send_message(email)

        print(f"UYARI: {message} (E-posta gönderildi)")
    def log_info(self, info_message):
        # Bilgi mesajını bir log dosyasına yazma
        with open("bot_log.txt", "a") as log_file:
            log_file.write(f"{info_message}\n")
        print(f"BİLGİ: {info_message}")


    def run_bot(self):
        # Botun ana döngüsü
        while True:
            for symbol in self.settings['symbols']:
                self.analyze_symbol(symbol)
            time.sleep(60)  # 1 dakika bekletme

if __name__ == "__main__":
    # Bot ayarlarını al
    settings = config.getBotSettings()

    # BinanceBot sınıfının bir örneğini oluştur
    bot = BinanceBot(settings)

    # Botu başlat
    try:
        bot.run_bot()
    except KeyboardInterrupt:
        print("Bot durduruldu.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        # İhtiyaca göre ek hata işleme ve kayıt kodları

