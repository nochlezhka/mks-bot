# -*- coding: utf-8 -*-
import logging
import re
import requests
import idna


def get_latest_version() -> str:
    try:
        resp = requests.get("https://github.com/nochlezhka/mks/tags", timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as ex:
        logging.error(f"Failed to fetch tags page: {ex}")
        return None

    try:
        content = resp.content.decode("utf-8")
    except UnicodeDecodeError as ex:
        logging.error(f"Failed to decode response content: {ex}")
        return None

    pattern = r'(?:rc/)?\d{1,2}\.\d{1,2}\.\d{1,2}</a>'
    versions = re.findall(pattern, content)
    versions = [version.replace("</a>", "") for version in versions]

    if not versions:
        logging.error("No version strings found in HTML content.")
        return None

    return versions[0]


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
            version = response.text.strip()

            version = (version[:12] + '..') if len(version) > 12 else version
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
            version = response.text.strip()

            version = (version[:12] + '..') if len(version) > 12 else version
        except Exception as ex:
            logging.error(ex)
            version = "?"

        data.append([client['name'], version, status, ssl_status, client['type'], idna.decode(client['url'])])

    return header, data
