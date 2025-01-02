#!/bin/bash

# export PROJECT=nginx-media-server
# export GROUP=dev

PROJECT=corp-sync
GROUP=hyeongjin0319

# export MYPORT=$((UID+9100))
# export CPATH=`pwd`
# export CURRENT_UID=$(id -u):$(id -g) 
# export PLATFORM=$(uname -r)


# if echo "$CPATH" | grep -q "/hyeongjin/"; then
#     export ME="hyeongjin"
#     export MYPORT=11100
# fi
# # export COMPOSE_PROJECT_NAME="${PROJECT}_${ME}"


# echo "$ME => PORT: $MYPORT"
# # exit 1

docker compose down
docker compose pull

docker compose up -d --remove-orphans  