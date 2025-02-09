# -*- coding: utf-8 -*-

import datetime
import logging
import telebot

from threading import Thread

from bot.bot import run as b_run
from daemons.alerts import run as a_run

from utils import config as cfg_utils

if __name__ == '__main__':
    config = cfg_utils.load("../resources/config.yml")

    log_dir = config["log"]["dir"]
    if log_dir:
        log_name = '%s/%s.log' % (config["log"]["dir"], datetime.datetime.now().strftime('%d_%m_%Y_%H_%M'))
        logging.basicConfig(filename=log_name, level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    telebot.logger.setLevel(logging.INFO)

    mks_alerts = Thread(target=a_run, args=(config,))
    mks_alerts.start()

    telegram_bot_proccess = Thread(target=b_run, args=())
    telegram_bot_proccess.start()
    telegram_bot_proccess.join()
