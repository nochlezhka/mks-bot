# -*- coding: utf-8 -*-

import logging

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup
from functools import partial


def register_handlers(bot: TeleBot, config):
    bot.register_message_handler(
        partial(handler_start, config=config), commands=['start'], pass_bot=True
    )


def handler_start(message: Message, bot: TeleBot, config):
    if message.from_user.username not in config["allowed_users"]:
        try:
            msg = bot.send_message(
                message.from_user.id,
                config["texts"]["messages"]["permission_error"].format(name=message.from_user.first_name)
            )
        except Exception as ex:
            logging.error(ex)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('показать короткий статус', 'показать длинный статус', 'помощь')

        try:
            msg = bot.send_message(
                message.from_user.id,
                config["texts"]["messages"]["start"].format(name=message.from_user.first_name),
                reply_markup=markup
            )
        except Exception as ex:
            logging.error(ex)
