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

    'state_1': 'Оцени свое состояние по 10ти балльной шкале',
    'state_2': 'Время высказаться! Ты можешь сделать это голосовым сообщением, текстом или видео-кружочком. Данные я не сохраняю 🙅‍ (у меня на это банально нет ресурсов 🙂)',
    'state_3': 'Очень здорово, что высказался! Полегчало? Пожалуйста, оцени свое состояние еще раз',
    'state_4': 'Круто, спасибо за практику, {name}! Не забывай ее делать регулярно, ведь я для этого и существую',

    'show_history': 'Ваша история: \n',

    'help': 'Я - бот, который дает тебе возможность высказаться. Просто нажми /start и скажи все, что у тебя держалось внутри. 💥 До и после того как ты выскажешься (это может быть текст, голосовое или видео-кружочек) я спрошу тебя про твои ощущения по десятибалльной шкале. Не волнуйся, я не собираю данные 🙅‍, у меня банально нет денег, чтобы их хранить :) \n\nУ меня есть следующие команды: \n/start - начать высказываться \n/help - показать данную подсказку',

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
