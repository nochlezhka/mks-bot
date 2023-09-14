# -*- coding: utf-8 -*-

import prettytable as pt
import requests
import json


def fetch_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()  # Parse JSON response
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {url}: {e}")
        return None


def check_status(clients):
    table = pt.PrettyTable(['клиент', 'версия', 'статус', 'облако'])



    for client in clients:
        response = requests.get(f"{client['url']}/{client['endpoint']}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        plain_text = response.text  # Get plain text response

        if plain_text:
            table.add_row([
                client['name'], plain_text, "✅", client['type']
            ])


    print(table)


    return table
