# -*- coding: utf-8 -*-

import telebot
import sys
import time
import logging

from telebot import TeleBot
from tgbot.handlers import *
from utils import config as cfg_utils


def register_handlers(bot: TeleBot, config):
    for handler_group in [help, start, status, text]:
        handler_group.register_handlers(bot, config)


def run():
    sys.path.append('../resources/')
    config = cfg_utils.load("../resources/config.yml")

    telebot.logger.setLevel(logging.INFO)
    bot = telebot.TeleBot(config["telegram"]["token"], num_threads=5)

    while True:
        try:
            register_handlers(bot, config)

            bot.polling(non_stop=True, interval=0, timeout=10)
        except Exception as ex:
            logging.info("[telegram] Failed: %s" % ex)
            time.sleep(3)
