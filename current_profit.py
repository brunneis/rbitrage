#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import datetime

def get_trades_url(exchange, curr1, curr2):
    if exchange == "gdax":
        return f"https://api.gdax.com/products/{curr1}-{curr2}/trades"
    elif exchange == "kraken":
        return f"https://api.kraken.com/0/public/Trades?pair={curr1}{curr2}"

def get_profit(deposit_fee=0,
               withdraw_fee=0.15,
               tx_wallet_fee=0.000262,
               tx_exchange_fee=0.001,
               buy_fee_ratio=0.0026,
               sell_fee_ratio=0.003,
               buy_price=1,
               sell_price=1,
               quantity=9.14):
    quantity *= buy_price
    obtained_crypto = - tx_wallet_fee + (quantity / buy_price) * (1 - buy_fee_ratio) - tx_exchange_fee
    obtained_fiat = obtained_crypto * sell_price * (1 - sell_fee_ratio) - withdraw_fee
    return quantity, obtained_fiat - quantity
               
check = True

while(check):
    try:
        file = open("profit.csv", "a") 

        gdax_trades = requests.get(url=get_trades_url("gdax", "ltc", "eur")).json()
        gdax_price = float(gdax_trades[0]['price'])
        
        kraken_trades = requests.get(url=get_trades_url("kraken", "ltc", "eur")).json()['result']['XLTCZEUR']
        kraken_price = float(kraken_trades[-1][0])

        quantity, profit = get_profit(buy_price=kraken_price, sell_price=gdax_price)
        file.write("%.2f;%s;%f;%f;%f\n" % (round(profit, 2), datetime.datetime.now(), kraken_price, gdax_price, quantity))
        file.close()
    except:
        pass

    time.sleep(5)
