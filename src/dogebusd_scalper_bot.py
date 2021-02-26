import time
import settings
import numpy as np

from binance.client import Client
from binance.enums import *

client = Client(settings.API_KEY, settings.API_SECRET, tld='com')

SYMBOL_TICKER = 'DOGEBUSD'
QUANTITY_ORDERS = 200
KLINES_INTERVAL = '18 hour ago UTC'
DECIMAL_PLACE = 6


def get_klines():
    return client.get_historical_klines(SYMBOL_TICKER,
                                        Client.KLINE_INTERVAL_15MINUTE,
                                        KLINES_INTERVAL)


def trend():
    x = []
    y = []
    sum = 0
    resp = False

    klines = get_klines()

    if len(klines) != 72:
        return False

    for i in range(56, 72):
        for j in range(i - 50, i):
            sum = sum + float(klines[i][4])

        ma50_i = round(sum / 50, DECIMAL_PLACE)
        sum = 0
        x.append(i)
        y.append(float(ma50_i))

    model = np.polyfit(x, y, 1)

    if model[0] > 0:
        resp = True

    return resp


def media50():
    ma50_local = 0
    sum = 0
    klines = get_klines()

    print(len(klines))

    if len(klines) >= 60:
        for i in range(10, 60):
            sum = sum + float(klines[i][4])
        ma50_local = sum / 50

    return ma50_local


while True:
    orders = client.get_open_orders(symbol=SYMBOL_TICKER)

    if len(orders) != 0:
        print("THERE IS OPEN ORDERS")
        time.sleep(10)
        continue

    last_trader = client.get_recent_trades(symbol=SYMBOL_TICKER, limit=1)
    symbol_price = float(last_trader[0].get('price'))

    ma50 = media50()
    if ma50 == 0:
        continue

    if symbol_price:

        print("***** " + SYMBOL_TICKER + " *******")
        print("Actual MA50 " + str(round(ma50, DECIMAL_PLACE)))
        print("Actual Price " + str(round(symbol_price, DECIMAL_PLACE)))
        print("Price to Buy " + str(round(ma50 * 0.995, DECIMAL_PLACE)))

        if not trend():
            print("TENDENCIA BAJISTA")
            time.sleep(10)
            continue
        else:
            print("ALCISTA")

        if symbol_price < ma50 * 0.995:
            print("BUY")

            order = client.order_market_buy(
               symbol=SYMBOL_TICKER,
               quantity=QUANTITY_ORDERS
            )

            time.sleep(5)

            print("OCO")

            print(round(symbol_price * 1.02, DECIMAL_PLACE))
            print(round(symbol_price * 0.995, DECIMAL_PLACE))
            print(round(symbol_price * 0.994, DECIMAL_PLACE))

            orderOCO = client.order_oco_sell(
                symbol=SYMBOL_TICKER,
                quantity=QUANTITY_ORDERS,
                price=round(symbol_price * 1.02, DECIMAL_PLACE),
                stopPrice=round(symbol_price * 0.995, DECIMAL_PLACE),
                stopLimitPrice=round(symbol_price * 0.994, DECIMAL_PLACE),
                stopLimitTimeInForce='GTC'
            )
            time.sleep(30)
