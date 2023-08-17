import os
from dotenv import load_dotenv

# .env dosyasını yükleyin
load_dotenv()

# API anahtarları
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

SYMBOLS = ["BTCUSDT", "ETHUSDT", "ADAUSDT"]

# Kaldıraç oranı
LEVERAGE = int(os.getenv('LEVERAGE', 10))

# İşlem zaman dilimleri
TIME_FRAMES = os.getenv('TIME_FRAMES', '1m,3m,5m').split(',')

# İlgili sembol filtresi
SYMBOL_FILTER = os.getenv('SYMBOL_FILTER', 'USDT')

# Risk yönetimi parametreleri
MAX_RISK = float(os.getenv('MAX_RISK', 0.02))
STOP_LOSS = float(os.getenv('STOP_LOSS', 0.01))