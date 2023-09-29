# -*- coding: utf-8 -*-
import logging

import prettytable as pt
import pandas as pd
import requests
import idna


def get_short_status(clients, pretty_table=False):
    if pretty_table:
        table = pt.PrettyTable(['клиент', 'версия', 'статус'])
    else:
        data = []

    for client in clients:
        try:
            response = requests.get(
                url=f"https://{client['url']}/",
                timeout=60
            )
            response.raise_for_status()
            status = "✅"
        except Exception as ex:
            logging.error(ex)
            status = "❌"

        try:
            response = requests.get(
                url=f"https://{client['url']}/{client['endpoint']}",
                timeout=60,
                verify=False
            )
            response.raise_for_status()
            version = response.text

            version = (version[:8] + '..') if len(version) > 8 else version
        except Exception as ex:
            logging.error(ex)
            version = "?"

        if pretty_table:
            table.add_row([
                client['name'], version, status
            ])
        else:
            data.append([client['name'], version, status])

    if not pretty_table:
        table = pd.DataFrame(data)
        table.columns = ['клиент', 'версия', 'статус']
        table.style.hide(axis="columns")

    return table


def get_long_status(clients, pretty_table=False):
    if pretty_table:
        table = pt.PrettyTable(['клиент', 'версия', 'статус', 'TLS', 'облако', 'URL'])
    else:
        data = []

    for client in clients:
        try:
            response = requests.get(
                url=f"https://{client['url']}/",
                timeout=60
            )
            response.raise_for_status()
            status = "✅"
            ssl_status = "✅"
        except requests.exceptions.SSLError as ex:
            logging.error(f"SSL certificate error: {ex}")
            status = "✅"
            ssl_status = "❌"
        except Exception as ex:
            logging.error(ex)
            status = "❌"
            ssl_status = "❌"

        try:
            response = requests.get(
                url=f"https://{client['url']}/{client['endpoint']}",
                timeout=60,
                verify=False
            )
            response.raise_for_status()
            version = response.text

            version = (version[:8] + '..') if len(version) > 8 else version
        except Exception as ex:
            logging.error(ex)
            version = "❓"

        if pretty_table:
            table.add_row([
                client['name'], version, status, ssl_status, client['type'], idna.decode(client['url'])
            ])
        else:
            data.append([client['name'], version, status, ssl_status, client['type'], idna.decode(client['url'])])

    if not pretty_table:
        table = pd.DataFrame(data)
        table.columns = ['клиент', 'версия', 'статус', 'TLS', 'облако', 'URL']
        table.style.hide(axis="columns")

    return table
