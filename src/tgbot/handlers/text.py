# -*- coding: utf-8 -*-

import logging
import telebot

from telebot import TeleBot
from telebot.types import Message
from functools import partial
from mks import check
from utils import table_to_img as tti


def register_handlers(bot: TeleBot, config):
    bot.register_message_handler(
        partial(handler_text, config=config), content_types=['text'], pass_bot=True
    )


def handler_text(message: Message, bot: TeleBot, config):
    if message.from_user.username not in config["allowed_users"]:
        try:
            msg = bot.send_message(
                message.from_user.id,
                config["texts"]["messages"]["permission_error"].format(name=message.from_user.first_name)
            )
        except Exception as ex:
            logging.error(ex)
    else:
        latest_mks_version = check.get_latest_version(
            config["github"]["token"]
        )

        if message.text == 'показать короткий статус':
            try:
                bot.send_message(
                    message.from_user.id,
                    config["texts"]["messages"]["processing"],
                    reply_markup=telebot.types.ReplyKeyboardRemove()
                )
                header, data = check.get_short_status(config["clients"], config["default_version_endpoint"])
                bot.send_photo(
                    message.from_user.id,
                    photo=tti.convert(header, data, latest_mks_version, config["colors"])
                )
            except Exception as ex:
                logging.error(ex)

        if message.text == 'показать длинный статус':
            latest_mks_version = check.get_latest_version(
                config["github"]["token"]
            )

            try:
                bot.send_message(
                    message.from_user.id,
                    config["texts"]["messages"]["processing"],
                    reply_markup=telebot.types.ReplyKeyboardRemove()
                )

                header, data = check.get_long_status(config["clients"], config["default_version_endpoint"])
                bot.send_photo(
                    message.from_user.id,
                    photo=tti.convert(header, data, latest_mks_version, config["colors"])
                )
            except Exception as ex:
                logging.error(ex)

        elif message.text == 'помощь':
            try:
                bot.send_message(
                    message.from_user.id,
                    config["texts"]["messages"]["help"],
                    reply_markup=telebot.types.ReplyKeyboardRemove()
                )
            except Exception as ex:
                logging.error(ex)

        else:
            try:
                bot.send_message(
                    message.from_user.id,
                    config['texts']['messages']["unknown"],
                    reply_markup=telebot.types.ReplyKeyboardRemove()
                )
            except Exception as ex:
                logging.error(ex)
