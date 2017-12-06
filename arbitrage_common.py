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


def get_profit(deposit_fee=0,
               withdraw_fee=0.15,
               tx_wallet_fee=0.001,
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
