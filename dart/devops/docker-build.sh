#!/bin/bash

PROJECT=corp-sync
GROUP=hyeongjin0319

TODAY=$(date +'%Y%m%d')
echo  "Build Docker for $PROJECT - $1 - $TODAY" 

if [ ${#1} -gt 0 ]; then

docker build --tag $PROJECT:${1}latest --tag $PROJECT:${1}$TODAY -f ./Dockerfile .. || exit
docker image tag $PROJECT:${1}latest $GROUP/$PROJECT:${1}latest
docker image tag $PROJECT:${1}latest $GROUP/$PROJECT:${1}$TODAY
docker image push -a $GROUP/$PROJECT

else

docker build --tag $PROJECT:${1}latest  -f ./Dockerfile .. || exit
docker image tag $PROJECT:${1}latest $GROUP/$PROJECT:${1}latest
docker image push -a $GROUP/$PROJECT

fi

