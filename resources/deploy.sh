#!/bin/bash

VERSION="rc-0.1.0"
TG_BOT_TOKEN="<TOKEN>"
MKS_API_TOKEN="<TOKEN>"

docker run -d \
    --name=mks_bot \
    --restart=always \
    -e TG_BOT_TOKEN==${TG_BOT_TOKEN} \
    -e MKS_API_TOKEN=${MKS_API_TOKEN} \
    kvendingoldo/mks_bot:${VERSION}
