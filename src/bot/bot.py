# -*- coding: utf-8 -*-

import sys
import logging
import time
import telebot

from utils import config as cfg_utils
from mks import check


sys.path.append('../resources/')
config = cfg_utils.load("../resources/config.yml")

bot = telebot.TeleBot(config["telegram"]["token"])
telebot.logger.setLevel(logging.INFO)

text_messages = {
    'start': '{name}, привет! 🎉 Выбери необходимое действие в меню ✨',

    'help': '/start - начальный экран \n/status - показать статус \n/help - показать подсказку',
    'permission_error': 'Сорри, мы не знаем, кто ты. Напиши @kvendingoldo чтобы исправить доступ к боту.',

    'wrong_msg': 'Похоже что-то пошло не так. Пожалуйста, воспользуйся подсказкой через /help или начните заного через /start'
}


@bot.message_handler(commands=['start'])
def handler_start(message):
    if message.from_user.username not in config["allowed_users"]:
        try:
            msg = bot.send_message(
                message.from_user.id,
                text_messages['permission_error'].format(name=message.from_user.first_name)
            )
        except Exception as ex:
            logging.error(ex)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('показать статус', 'помощь')

        try:
            msg = bot.send_message(
                message.from_user.id,
                text_messages['start'].format(name=message.from_user.first_name),
                reply_markup=markup
            )
        except Exception as ex:
            logging.error(ex)


@bot.message_handler(commands=['status'])
def handler_status(message):
    if message.from_user.username not in config["allowed_users"]:
        try:
            msg = bot.send_message(
                message.from_user.id,
                text_messages['permission_error'].format(name=message.from_user.first_name)
            )
        except Exception as ex:
            logging.error(ex)
    else:
        try:
            table = check.check_status(config["clients"])
            msg = bot.send_message(
                message.from_user.id,
                f"```{table}```",
                parse_mode='MarkdownV2'
            )
        except Exception as ex:
            logging.error(ex)


@bot.message_handler(commands=['help'])
def handler_help(message):
    if message.from_user.username not in config["allowed_users"]:
        try:
            msg = bot.send_message(
                message.from_user.id,
                text_messages['permission_error'].format(name=message.from_user.first_name)
            )
        except Exception as ex:
            logging.error(ex)
    else:
        try:
            bot.send_message(
                message.from_user.id,
                text_messages['help'],
                reply_markup=telebot.types.ReplyKeyboardRemove()
            )
        except Exception as ex:
            logging.error(ex)


@bot.message_handler(content_types=['text'])
def handler_text(message):
    if message.from_user.username not in config["allowed_users"]:
        try:
            msg = bot.send_message(
                message.from_user.id,
                text_messages['permission_error'].format(name=message.from_user.first_name)
            )
        except Exception as ex:
            logging.error(ex)
    else:
        if message.text == 'показать статус':
            try:
                table = check.check_status(config["clients"])
                msg = bot.send_message(
                    message.from_user.id,
                    f"```{table}```",
                    parse_mode='MarkdownV2'
                )
            except Exception as ex:
                logging.error(ex)

        elif message.text == 'помощь':
            try:
                bot.send_message(
                    message.from_user.id,
                    text_messages['help'],
                    reply_markup=telebot.types.ReplyKeyboardRemove()
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
