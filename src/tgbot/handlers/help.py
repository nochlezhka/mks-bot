# -*- coding: utf-8 -*-

import logging

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from functools import partial


def register_handlers(bot: TeleBot, config):
    bot.register_message_handler(
        partial(handler_help, config=config), commands=['help'], pass_bot=True
    )


def handler_help(message: Message, bot: TeleBot, config):
    if message.from_user.username not in config["allowed_users"]:
        try:
            msg = bot.send_message(
                message.from_user.id,
                config["texts"]["messages"]["permission_error"].format(name=message.from_user.first_name)
            )
        except Exception as ex:
            logging.error(ex)
    else:
        try:
            bot.send_message(
                message.from_user.id,
                config["texts"]["messages"]["help"],
                reply_markup=ReplyKeyboardRemove()
            )
        except Exception as ex:
            logging.error(ex)
