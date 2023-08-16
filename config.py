import os
from dotenv import load_dotenv

load_dotenv()

# Binance API Keys
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# SYMBOLS = ["SUSHIUSDT", "BTSUSDT", "INJUSDT", "BNTUSDT", "RDNTUSDT", "ZRXUSDT", "HIGHUSDT", "WAVESUSDT", "SPELLUSDT", "XTZUSDT", "DARUSDT", "JOEUSDT", "XMRUSDT", "PENDLEUSDT", "ALICEUSDT", "HOOKUSDT", "REEFUSDT", "BATUSDT", "DOGEUSDT", "TRXUSDT", "STORJUSDT", "SNXUSDT", "XLMUSDT", "IOTXUSDT", "DASHUSDT", "UMAUSDT", "KAVAUSDT", "OXTUSDT", "RUNEUSDT", "APEUSDT", "BLUEBIRDUSDT", "BNXUSDT", "OPUSDT", "KEYUSDT", "DGBUSDT", "SKLUSDT", "FOOTBALLUSDT", "TOMOUSDT", "MTLUSDT", "ETHBTC", "KSMUSDT", "BNBBUSD", "TRBUSDT", "MANAUSDT", "FLOWUSDT", "CHRUSDT", "GALUSDT", "USDCUSDT", "OGNUSDT", "RNDRUSDT", "SCUSDT", "KNCUSDT", "BLURUSDT", "ENJUSDT", "ATOMUSDT", "SOLBUSD", "NMRUSDT", "ENSUSDT", "ATAUSDT", "AGIXUSDT", "IOSTUSDT", "HBARUSDT", "ZECUSDT", "IDEXUSDT", "GALAUSDT", "EDUUSDT", "GTCUSDT", "ALGOUSDT", "LRCUSDT", "STGUSDT", "STXUSDT", "ARPAUSDT", "CELOUSDT", "QNTUSDT", "1INCHUSDT", "TUSDT", "LINAUSDT", "ARUSDT", "FILUSDT", "DODOXUSDT", "SOLUSDT", "COMBOUSDT", "GMTUSDT", "MDTUSDT", "XVSUSDT", "GMXUSDT", "BANDUSDT", "LDOUSDT", "XRPBUSD", "CRVUSDT", "BELUSDT", "ONEUSDT", "APTUSDT", "ANKRUSDT", "MAVUSDT", "RAYUSDT", "API3USDT", "ASTRUSDT", "HOTUSDT", "QTUMUSDT", "IOTAUSDT", "BTCBUSD", "LITUSDT", "YFIUSDT", "ETHUSDT", "ALPHAUSDT", "WOOUSDT", "SFPUSDT", "RLCUSDT", "BTCSTUSDT", "1000XECUSDT", "FXSUSDT", "CFXUSDT", "AUDIOUSDT", "IDUSDT", "HFTUSDT", "NEOUSDT", "UNFIUSDT", "SANDUSDT", "CTKUSDT", "MINAUSDT", "CELRUSDT", "AGLDUSDT", "RSRUSDT", "RENUSDT", "JASMYUSDT", "PHBUSDT", "YGGUSDT", "EGLDUSDT", "LUNA2USDT", "ONTUSDT", "VETUSDT", "IMXUSDT", "LQTYUSDT", "COTIUSDT", "CVXUSDT", "ARBUSDT", "BAKEUSDT", "GRTUSDT", "FLMUSDT", "MASKUSDT", "BALUSDT", "SUIUSDT", "DENTUSDT", "TRUUSDT", "CKBUSDT", "SSVUSDT", "C98USDT", "ZENUSDT", "NEARUSDT", "1000SHIBUSDT", "ANTUSDT", "ETHBUSD", "TLMUSDT", "AAVEUSDT", "ICPUSDT", "1000LUNCUSDT", "RADUSDT", "AVAXUSDT", "MAGICUSDT", "ROSEUSDT", "MATICUSDT",	"XVGUSDT", "MKRUSDT", "PEOPLEUSDT", "THETAUSDT", "UNIUSDT", "PERPUSDT", "RVNUSDT", "ARKMUSDT", "NKNUSDT", "KLAYUSDT", "DEFIUSDT", "COMPUSDT", "BTCDOMUSDT", "BTCUSDT", "OMGUSDT", "ICXUSDT", "1000PEPEUSDT", "FETUSDT", "LEVERUSDT", "1000FLOKIUSDT", "FTMUSDT", "DOGEBUSD", "SXPUSDT", "XEMUSDT", "WLDUSDT", "ZILUSDT", "AXSUSDT", "DYDXUSDT", "OCEANUSDT", "CHZUSDT", "DUSKUSDT", "CTSIUSDT", "ACHUSDT"]

# Bot ayarlarını almak için bir fonksiyon
def getBotSettings():
    with open('settings.json', 'r') as file:
        import json
        settings = json.load(file)
        return settings
# Gelişmiş Dinamik Risk Yönetimi için parametreler
def calculate_quantity(symbol, analysis_result):
    # İlgili sembol ve analiz sonucuna göre dinamik olarak işlem miktarını hesaplayın
    # Örnek olarak, belirli bir yüzde veya sabit miktar kullanabilirsiniz
    # Bu fonksiyonun içeriği, kullanılan strateji ve risk yönetimi politikasına bağlı olarak değişebilir
    risk_factor = 0.02
    balance = 1000 # Örnek bakiye
    quantity = balance * risk_factor # Örnek değer
    return quantity

# Alım satım sinyallerini belirlemek için bir fonksiyon
def determine_side(analysis_result):
    # Analiz sonucuna göre alım veya satım sinyali belirleyin
    # Örnek olarak, belirli göstergeler veya koşullar kullanabilirsiniz
    if analysis_result['MACD'] > analysis_result['Signal_Line'] and analysis_result['RSI'] < 70:
        side = "BUY"
    elif analysis_result['MACD'] < analysis_result['Signal_Line'] and analysis_result['RSI'] > 30:
        side = "SELL"
    else:
        side = "HOLD"
    return side