# -*- coding: utf-8 -*-

import time
import telebot

import logging


def run(config):
    logging.info("Hello from MKS alerts system")

    bot = telebot.TeleBot(config["telegram"]["token"])
    telebot.logger.setLevel(logging.INFO)

    while True:
        header, items = check.get_long_status(config["clients"], config["default_version_endpoint"])

        for item in items:
            client_name, mks_version, mks_status, mks_ssl_status, client_type, client_url = item

            if mks_status != "ok":
                bot.send_message(
                    usr1.id, 'FAIL!'
                )
            else:
                if mks_ssl_status != "ok":
                    bot.send_message(
                        usr1.id, 'FAIL!'
                    )

                if mks_version == "?":
                    bot.send_message(
                        usr1.id, 'FAIL!'
                    )

        time.sleep(config["alerts"]["check_period"])
