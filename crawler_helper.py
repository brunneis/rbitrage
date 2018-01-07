# Crypto Arbitrage Tools
# Copyright (C) 2017 Rodrigo Martínez <dev@brunneis.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from time import gmtime, strftime
import datetime

def get_trades_url(exchange, curr1, curr2):
    """
    Get the URL of an exchange for a given currency tuple
    """
    if exchange == 'gdax':
        return f'https://api.gdax.com/products/{curr1}-{curr2}/trades'
    elif exchange == 'kraken':
        return f'https://api.kraken.com/0/public/Trades?pair={curr1}{curr2}'
    elif exchange == 'gatehub':
        # TODO XRP/EUR ONLY
        if curr1 == 'xrp' and curr2 == 'eur':
            base_url = 'https://api.gatehub.net/rippledata/v2/exchanges/XRP/EUR%2Brhub8VRN55s94qWKDv6jmDy1pUykJzF3wq?descending=true&interval=15minute&start='
            return base_url + strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                gmtime((datetime.datetime.now() \
                - datetime.timedelta(hours=12) \
                - datetime.datetime.utcfromtimestamp(0)).total_seconds()))

def get_gatehub_price(curr1, curr2):
    """
    Get the last trade price for the given currency tuple on GateHub
    """
    gatehub_trades = requests.get(url=get_trades_url(
        'gatehub',
        curr1,
        curr2)).json()
    return float(gatehub_trades['exchanges'][0]['close'])

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
