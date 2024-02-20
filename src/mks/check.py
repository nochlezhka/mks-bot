# -*- coding: utf-8 -*-
import logging

import requests
import idna


def get_short_status(clients, default_version_endpoint):
    header = ['клиент', 'версия', 'статус']
    data = []

    for client in clients:
        try:
            response = requests.get(
                url=f"https://{client['url']}/",
                timeout=10
            )
            response.raise_for_status()
            status = "ok"
        except Exception as ex:
            logging.error(ex)
            status = "fail"

        endpoint = client['endpoint'] if client.get('endpoint') else default_version_endpoint

        try:
            response = requests.get(
                url=f"https://{client['url']}/{endpoint}",
                timeout=10,
                verify=False
            )
            response.raise_for_status()
            version = response.text

            version = (version[:8] + '..') if len(version) > 8 else version
        except Exception as ex:
            logging.error(ex)
            version = "?"

        data.append([client['name'], version, status])

    return header, data


def get_long_status(clients, default_version_endpoint):
    header = ['клиент', 'версия', 'статус', 'TLS', 'облако', 'URL']
    data = []

    for client in clients:
        try:
            response = requests.get(
                url=f"https://{client['url']}/",
                timeout=10
            )
            response.raise_for_status()
            status = "ok"
            ssl_status = "ok"
        except requests.exceptions.SSLError as ex:
            logging.error(f"SSL certificate error: {ex}")
            status = "ok"
            ssl_status = "fail"
        except Exception as ex:
            logging.error(ex)
            status = "fail"
            ssl_status = "fail"

        endpoint = client['endpoint'] if client.get('endpoint') else default_version_endpoint

        try:
            response = requests.get(
                url=f"https://{client['url']}/{endpoint}",
                timeout=10,
                verify=False
            )
            response.raise_for_status()
            version = response.text

            version = (version[:8] + '..') if len(version) > 8 else version
        except Exception as ex:
            logging.error(ex)
            version = "?"

        data.append([client['name'], version, status, ssl_status, client['type'], idna.decode(client['url'])])

    return header, data
