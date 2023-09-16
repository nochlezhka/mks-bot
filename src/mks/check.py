# -*- coding: utf-8 -*-
import logging

import prettytable as pt
import requests


def check_status(clients):
    table = pt.PrettyTable(['клиент', 'версия', 'статус', 'облако'])

    for client in clients:
        try:
            response = requests.get(
                url=f"{client['url']}/{client['endpoint']}",
                timeout=60
            )
            response.raise_for_status()
            version = response.text
            status = "✅"
        except Exception as ex:
            logging.error(ex)
            version = "❓"
            status = "❌"

        table.add_row([
            client['name'], version, status, client['type']
        ])

    print(table)

    return table
