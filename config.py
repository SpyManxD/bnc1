import os
from dotenv import load_dotenv

# .env dosyasını yükleyin
load_dotenv()

# API anahtarları
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# İşlem yapılacak semboller
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']

# İşlem zaman dilimi
INTERVAL = "1m"

# LSTM pencere uzunluğu
WINDOW_LENGTH = 10

# LSTM eğitim dönemi
EPOCHS = 50

# Risk yönetimi parametreleri
MAX_RISK_PER_TRADE = 0.01  # Her işlemde risk edilecek maksimum sermaye yüzdesi
STOP_LOSS = 0.02  # Zararı durdurma yüzdesi
TAKE_PROFIT = 0.03  # Kar al yüzdesi

# Diğer genel ayarlar
REAL_TIME_MONITORING_INTERVAL = 60  # Gerçek zamanlı izleme aralığı (saniye)
