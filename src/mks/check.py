# -*- coding: utf-8 -*-
import logging

import prettytable as pt
import requests


def check_status(clients):
    table = pt.PrettyTable(['клиент', 'версия', 'статус', 'TLS', 'облако'])

    for client in clients:
        try:
            response = requests.get(
                url=f"{client['url']}/",
                timeout=60
            )
            response.raise_for_status()
            status = "✅"
            ssl_status = "✅"
        except requests.exceptions.SSLError as ex:
            logging.error(f"SSL certificate error: {ex}")
            status = "❌"
            ssl_status = "❌"
        except Exception as ex:
            logging.error(ex)
            status = "❌"
            ssl_status = "❌"

        try:
            response = requests.get(
                url=f"{client['url']}/{client['endpoint']}",
                timeout=60,
                verify=False
            )
            response.raise_for_status()
            version = response.text
        except Exception as ex:
            logging.error(ex)
            version = "❓"

        table.add_row([
            client['name'], version, status, ssl_status, client['type']
        ])

    print(table)

    return table
