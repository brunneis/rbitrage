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


def get_trades_url(exchange, curr1, curr2):
    """
    Get the URL of an exchange for a given currency tuple
    """
    if exchange == 'gdax':
        return f'https://api.gdax.com/products/{curr1}-{curr2}/trades'
    elif exchange == 'kraken':
        return f'https://api.kraken.com/0/public/Trades?pair={curr1}{curr2}'


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
