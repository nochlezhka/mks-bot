# -*- coding: utf-8 -*-

import time
import telebot

import logging

from mks import check

text_messages = {
    'failed': u'[FAILED] {name} check for {client_name}',
    'resolved': u'[RESOLVED] {type} check for {client_name}'
}

alerts_inmem_db = {}


def send_alert(config, client):
    bot = telebot.TeleBot(config["telegram"]["token"])

    for alert_name in alerts_inmem_db[client]:
        if alerts_inmem_db[client][alert_name]["failed"] > 3:
            for receiver in config["alerts"]["receivers"]:
                bot.send_message(
                    receiver, text_messages['failed'].format(
                        name=alert_name,
                        client_name=client
                    )
                )
        if alerts_inmem_db[client][alert_name]["resolved"] > 3:
            for receiver in config["alerts"]["receivers"]:
                bot.send_message(
                    receiver, text_messages['resolved'].format(
                        name=alert_name,
                        client_name=client
                    )
                )
            alerts_inmem_db[client][alert_name]["resolved"] = 0
            alerts_inmem_db[client][alert_name]["failed"] = 0


def update_inmem_db(type, state):
    if state != "ok":
        alerts_inmem_db[type]['status']['failed'] += 1
    else:
        if alerts_inmem_db[type]['status']['failed'] != 0:
            alerts_inmem_db[type]['status']['resolved'] += 1
        else:
            alerts_inmem_db[type]['status']['resolved'] = 0


def run(config):
    logging.info("Hello from MKS alerts system")
    alert_types = ["healthy", "ssl_status"]

    while True:
        header, items = check.get_long_status(config["clients"], config["default_version_endpoint"])

        for item in items:
            client_info = {
                "name": item[0],
                "healthy": item[2],
                "ssl_status": item[3]
            }

            if client_info["name"] not in alerts_inmem_db:
                alerts_inmem_db[client_info["name"]] = {
                    'healthy': {
                        "failed": 0,
                        "resolved": 0
                    },
                    'ssl_status': {
                        "failed": 0,
                        "resolved": 0
                    }
                }

            for alert_type in alert_types:
                update_inmem_db(alert_type, client_info[alert_type])

        for client in alerts_inmem_db:
            send_alert(config, client)

        time.sleep(config["alerts"]["check_period"])
