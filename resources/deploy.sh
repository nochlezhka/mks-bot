#!/bin/bash

VERSION="rc-0.1.0"
TBOT_TOKEN="<TOKEN>"

docker run -d \
    --name=mks_bot \
    --restart=always \
    -e TG_BOT_TOKEN=${TBOT_TOKEN} \
    kvendingoldo/mks_bot:${VERSION}
