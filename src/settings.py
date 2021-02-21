import os

API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
TRADE_SYMBOL = os.environ.get('TRADE_SYMBOL')
TRADE_QUANTITY = float(os.environ.get('TRADE_QUANTITY', 0.1))
WS_URL = os.environ.get('WS_URL')
