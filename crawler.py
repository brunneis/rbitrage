#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import os.path
from threading import Thread
from crawler_helper import *
from arbitrage_common import *

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

