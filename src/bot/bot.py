# -*- coding: utf-8 -*-

import prettytable as pt
import telebot
import sys
import logging
import time

from utils import config as cfg_utils
from mks import check

from telebot.types import ReplyKeyboardRemove

sys.path.append('../resources/')
config = cfg_utils.load("../resources/config.yml")

bot = telebot.TeleBot(config["telegram"]["token"])
telebot.logger.setLevel(logging.INFO)

text_messages = {
    'start': u'{name}, привет! 🎉 Выбери необходимое действие в меню ✨',

    'help': '/help - показать данную подсказку',

    'wrong_msg': 'Похоже что-то пошло не так. Пожалуйста, воспользуйтесь подсказкой через /help или начните заного через /start'
}


@bot.message_handler(commands=['help'])
def handler_help(message):
    try:
        bot.send_message(
            message.from_user.id,
            text_messages['help'],
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as ex:
        logging.error(ex)


@bot.message_handler(commands=['start'])
def handler_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('выговориться', 'посмотреть историю', 'помощь')

    try:
        msg = bot.send_message(
            message.from_user.id,
            text_messages['start'].format(name=message.from_user.first_name),
            reply_markup=markup
        )
    except Exception as ex:
        logging.error(ex)


@bot.message_handler(commands=['status'])
def handler_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    try:
        table = check.check_status(config["clients"])
        msg = bot.send_message(
            message.from_user.id,
            f"```{table}```",
            parse_mode='MarkdownV2'
        )
    except Exception as ex:
        logging.error(ex)


def run():
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=10)
        except Exception as ex:
            logging.info("[telegram] Failed: %s" % ex)
            time.sleep(3)
