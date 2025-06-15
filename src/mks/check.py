# -*- coding: utf-8 -*-
import logging
import os
import requests
import idna
import json

MKS_API_TOKEN = os.getenv("MKS_API_TOKEN")


def get_latest_version() -> str:
    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {MKS_API_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        resp = requests.get(f"https://api.github.com/repos/nochlezhka/mks/tags", headers=headers)
        resp.raise_for_status()

    except requests.exceptions.RequestException as ex:
        logging.error(f"Failed to fetch tags page: {ex}")
        return None

    try:
        content = json.loads(resp.content.decode("utf-8"))
        return content[0].get("name").replace("/", "-") if len(content) != 0 else None

    except UnicodeDecodeError as ex:
        logging.error(f"Failed to decode response content: {ex}")
        return None

    except json.JSONDecodeError as ex:
        logging.error(f"Failed to parse JSON: {ex}")
        return None


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
