import requests
import settings
import pprint
import time

from binance.client import Client
from binance.enums import *

BUY_ORDER = 'buy'
SELL_ORDER = 'sell'

COINGECKO_BASE_URL = 'https://api.coingecko.com/api/v3'
COINGECKO_SIMPLE_PRICE_ENDPOINT = '/simple/price'
COINGECKO_ASSET = 'binancecoin'
COINGECKO_QUOTE_ASSET = 'binance-usd'

ASSET = 'BNB'
QUOTE_ASSET = 'BUSD'
BUY_ALLOCATION = 0.5
SELL_ALLOCATION = 0.15
SELL_SPREAD = 0.001
BUY_SPREAD = 0.002
TICK_INTERVAL = 2000  # In seconds

client = Client(settings.API_KEY, settings.API_SECRET, tld='com')


def order_limit(buy_or_sell, data):
    try:
        print("sending order")
        if buy_or_sell == BUY_ORDER:
            print("limit buy")
            pprint.pprint(data)
            order = client.order_limit_buy(**data)
            print(order)
        elif buy_or_sell == SELL_ORDER:
            print("limit sell")
            pprint.pprint(data)
            order = client.order_limit_sell(**data)
            print(order)
        else:
            print("Invalid action")
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def get_binance_asset_balance(asset):
    return client.get_asset_balance(asset)


def get_binance_symbol_info():
    return client.get_symbol_info(f'{ASSET}{QUOTE_ASSET}')


def close_open_orders():
    symbol = f'{ASSET}{QUOTE_ASSET}'
    orders = client.get_open_orders(symbol=symbol)

    for order in orders:
        client.cancel_order(
            symbol=symbol,
            orderId=order.get('orderId'))


def get_current_market_price():
    results = None

    url = f'{COINGECKO_BASE_URL}{COINGECKO_SIMPLE_PRICE_ENDPOINT}'
    asset_params = {
        'ids': f'{COINGECKO_ASSET},{COINGECKO_QUOTE_ASSET}',
        'vs_currencies': 'usd'
    }
    req = requests.get(url, params=asset_params)
    if req.status_code == 200:
        results = req.json()

    if results:
        asset = results.get(COINGECKO_ASSET).get('usd')
        base_asset = results.get(COINGECKO_QUOTE_ASSET).get('usd')
        print(f"{COINGECKO_ASSET} current price", asset)
        print(f"{COINGECKO_QUOTE_ASSET} current price", base_asset)
        return asset / base_asset
    else:
        return None


def go_trade():
    close_open_orders()
    symbol_info = get_binance_symbol_info()
    market_price = get_current_market_price()

    if market_price:
        asset_balance = get_binance_asset_balance(ASSET)
        quote_asset_balance = get_binance_asset_balance(QUOTE_ASSET)

        if asset_balance and quote_asset_balance:
            free_asset = float(asset_balance.get('free'))
            free_quote_asset = float(quote_asset_balance.get('free'))

            sell_price = market_price * (1 + SELL_SPREAD)
            buy_price = market_price * (1 - BUY_SPREAD)

            sell_volume = free_asset * SELL_ALLOCATION
            buy_volume = free_quote_asset * BUY_ALLOCATION / market_price

            print("sell price", sell_price)
            print("buy price", buy_price)

            print("sell volume", sell_volume)
            print("buy volume", buy_volume)

            percent_price = symbol_info.get('filters')[2]
            min_qty = percent_price.get('minQty')
            max_qty = percent_price.get('maxQty')

            print("Min Qty", min_qty)
            print("Max Qty", max_qty)

            sell_data = {
                'symbol': f'{ASSET}{QUOTE_ASSET}',
                'quantity': "{:0.0{}f}".format(sell_volume, 2),
                'price': "{:0.0{}f}".format(sell_price, 2),
            }

            order_limit(SELL_ORDER, sell_data)

            if buy_volume < float(min_qty) * 10:
                buy_volume = 0.1

            buy_data = {
                'symbol': f'{ASSET}{QUOTE_ASSET}',
                'quantity': "{:0.0{}f}".format(buy_volume, 2),
                'price': "{:0.0{}f}".format(buy_price, 2),
            }

            order_limit(BUY_ORDER, buy_data)


def run():
    #time.sleep(settings.DELAY)
    print("do it")
    go_trade()
    #run()


if __name__ == '__main__':
    run()
