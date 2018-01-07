# WealthWatchBot for Telegram
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

import yaml
import sys
import time
import logging
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from crawler_helper import *
from arbitrage_common import *


class WealthWatchbot(object):
    def __init__(self):
        self.users = {}

        self.interval = {}
        self.interval['ltc'] = 5
        self.interval['xrp'] = 5

        self.ltc_conf = {
            'tx_wallet_fee': 0.001,
            'tx_exchange_fee': 0.001,
        }

        self.xrp_conf = {
            'tx_wallet_fee': 0.00002,
            'tx_exchange_fee': 0.00002,
        }

        logging.basicConfig(filename='bot.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger()

        with open('./bot_conf.yaml', 'r') as stream:
            try:
                conf = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                logging.error(e, exc_info=True)
                sys.exit(1)

        # Token
        try:
            self.__dict__['token'] = conf['token']
        except KeyError:
            logging.error(e, exc_info=True)
            sys.exit(1)

        # Start message
        try:
            self.__dict__['start_message'] = conf['start_message']
        except KeyError:
            self.__dict__['start_message'] = ''

    def watch_ltc_eur(self):
        kraken_price = get_kraken_price("ltc", "eur")
        gdax_price = get_gdax_price("ltc", "eur")
        self.ltc_conf['buy_price'] = kraken_price
        self.ltc_conf['sell_price'] = gdax_price
        diff = gdax_price - kraken_price
        _, profit = get_profit(**self.ltc_conf)
        fee = diff - profit

        # if profit > 4:
        #     if profit > 7:
        #         self.interval['ltc'] = 5
        #     elif profit > 4:
        #         self.interval['ltc'] = 30
        #     else:
        #         self.interval['ltc'] = 60

        text = u"LTC/EUR 📈\n" \
        + "Profit: %.2f€\n" % profit \
        + "Diff: %.2f€\n" % diff \
        + "Fee: %.2f€\n\n" % fee \
        + "Kraken: %.2f€\n" % kraken_price \
        + "GDAX: %.2f€" % gdax_price
        print(text)

        for chat_id in self.users.values():
            self.bot.send_message(chat_id=chat_id,
                                  text=text)

    def watch_xrp_eur(self):
        gatehub_price = get_gatehub_price("xrp", "eur")
        kraken_price = get_kraken_price("xrp", "eur")
        self.xrp_conf['buy_price'] = gatehub_price
        self.xrp_conf['sell_price'] = kraken_price
        diff = gatehub_price - kraken_price
        _, profit = get_profit(**self.xrp_conf)
        fee = diff - profit

        # if profit > .05:
        #     if profit > .1:
        #         self.interval['xrp'] = 5
        #     elif profit > .7:
        #         self.interval['xrp'] = 30
        #     else:
        #         self.interval['xrp'] = 60

        text = u"XRP/EUR 📈\n" \
        + "Profit: %.2f€\n" % profit \
        + "Diff: %.2f€\n" % diff \
        + "Fee: %.2f€\n\n" % fee \
        + "GateHub: %.2f€\n" % gatehub_price \
        + "Kraken: %.2f€" % kraken_price
        print(text)

        for chat_id in self.users.values():
            self.bot.send_message(chat_id=chat_id,
                                  text=text)

    def alert_manager_ltc(self):
        while(True):
            try:
                self.watch_ltc_eur()
            except Exception as e:
                print(e)
            time.sleep(self.interval['ltc'])

    def alert_manager_xrp(self):
        while(True):
            try:
                self.watch_xrp_eur()
            except Exception as e:
                print(e)
            time.sleep(self.interval['xrp'])

    def start_handler(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text=self.__dict__['start_message'])

    def password_handler(self, bot, update):
        password = update.message.text[3:]
        if password == "magallanes":
            username = update.message.from_user.username
            chat_id = update.message.chat_id
            self.users[username] = chat_id
            self.bot = bot
            bot.send_message(chat_id=chat_id,
                             text="Let's buy some lambos...")

    def run(self):
        updater = Updater(token=self.__dict__['token'])
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', self.start_handler)
        password_handler = CommandHandler('p', self.password_handler)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(password_handler)

        updater.start_polling()

        Thread(target=self.alert_manager_ltc).start()
        Thread(target=self.alert_manager_xrp).start()


if __name__ == "__main__":
    app = WealthWatchbot()
    app.run()
