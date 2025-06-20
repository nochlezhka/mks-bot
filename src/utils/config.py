# -*- coding: utf-8 -*-

import os
import yaml


def load(yaml_path):
    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)

    if "TG_BOT_TOKEN" in os.environ:
        config["telegram"] = {
            "token": os.environ["TG_BOT_TOKEN"]
        }

    if "LOG_DIR" in os.environ:
        config["log"]["dir"] = os.environ["LOG_DIR"]

    if "MKS_API_TOKEN" in os.environ:
        config["github"] = {
            "token": os.environ["MKS_API_TOKEN"]
        }

    return config
