#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import datetime
import os.path
from threading import Thread


def get_trades_url(exchange, curr1, curr2):
    """
    Get the URL of an exchange for a given currency tuple
    """
    if exchange == 'gdax':
        return f'https://api.gdax.com/products/{curr1}-{curr2}/trades'
    elif exchange == 'kraken':
        return f'https://api.kraken.com/0/public/Trades?pair={curr1}{curr2}'


def get_profit(deposit_fee=0,
               withdraw_fee=0.15,
               tx_wallet_fee=0.0001,
               tx_exchange_fee=0.001,
               buy_fee_ratio=0.0026,
               sell_fee_ratio=0.003,
               buy_price=1,
               sell_price=1,
               quantity=1):
    """
    Get the net profit of an arbitrage operation
    """

    quantity *= buy_price

    obtained_crypto = - tx_wallet_fee + (quantity / buy_price) \
        * (1 - buy_fee_ratio) - tx_exchange_fee

    obtained_fiat = obtained_crypto * sell_price * (1 - sell_fee_ratio) \
        - withdraw_fee

    return quantity, obtained_fiat - quantity


def get_kraken_price(curr1, curr2):
    """
    Get the last trade price for the given currency tuple on Kraken
    """
    # Fix currency name for Kraken
    if curr1 == 'btc':
        curr1 = 'xbt'

    kraken_trades = requests.get(url=get_trades_url(
        'kraken',
        curr1,
        curr2)).json()['result'][f'X{curr1.upper()}Z{curr2.upper()}']
    return float(kraken_trades[-1][0])


def get_gdax_price(curr1, curr2):
    """
    Get the last trade price for the given currency tuple on GDAX
    """
    gdax_trades = requests.get(url=get_trades_url(
        'gdax',
        curr1,
        curr2)).json()
    return float(gdax_trades[0]['price'])


def _crawl(curr1, curr2, conf):
    """
    Start crawling data for the given currency tuple and conf
    """
    check = True
    while(check):
        try:
            suffix = datetime.datetime.today().strftime('%d%m%Y')
            rel_path = f'{curr1}{curr2}'
            filename = f'{rel_path}/{curr1}{curr2}_{suffix}.csv'

            # Create directory for the currency tuple if it does not exist
            if not os.path.exists(rel_path):
                os.mkdir(rel_path)

            # Add the CSV header if the file does not exist
            header = None
            if not os.path.isfile(filename):
                header = 'profit,datetime,kraken,gdax,quantity\n'

            file = open(filename, 'a')

            if header:
                file.write(header)

            kraken_price = get_kraken_price(curr1, curr2)
            gdax_price = get_gdax_price(curr1, curr2)

            conf['buy_price'] = kraken_price
            conf['sell_price'] = gdax_price

            quantity, profit = get_profit(**conf)

            file.write('%.2f,%s,%f,%f,%f\n' % (
                round(profit, 2),
                datetime.datetime.now(),
                kraken_price,
                gdax_price,
                quantity))

            file.close()
        except:
            pass

        time.sleep(5)


if __name__ == '__main__':

    ltc_conf = {
        'tx_wallet_fee': 0.0001,
        'tx_exchange_fee': 0.001,
    }

    eth_conf = {
        'tx_wallet_fee': 0.0000021,
        'tx_exchange_fee': 0.005,
    }

    btc_conf = {
        'tx_wallet_fee': 0.0001,
        'tx_exchange_fee': 0.001,
    }

    Thread(target=_crawl, args=('ltc', 'eur', ltc_conf)).start()
    time.sleep(1)

    Thread(target=_crawl, args=('eth', 'eur', eth_conf)).start()
    time.sleep(1)

    Thread(target=_crawl, args=('btc', 'eur', btc_conf)).start()

