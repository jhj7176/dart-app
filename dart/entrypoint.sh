#!/bin/bash
NAME=dart
# APP_RUN=$1
mkdir -p ./logs

# if [[ $SERVER_MODE != "production" ]]; then
#     # bash -c "celery -A $NAME worker --beat --loglevel=debug --polsol solo" &
#     # ./manage.py kafka_consumer plai_dropped_words &
#     # uvicorn $NAME.asgi:application --host 0.0.0.0 --reload --workers 1
#     ./manage.py runserver 0.0.0.0:8000
# else # start prod ===============================

if [ $APP_RUN == "all" ] || [ $APP_RUN == "web" ]; then
    uvicorn $NAME.asgi:application --host 0.0.0.0 --limit-concurrency 2000 --backlog 1000 --limit-max-requests 30000 --timeout-graceful-shutdown 120 --workers 1
fi

if [ $APP_RUN == "all" ] || [ $APP_RUN == "celery" ]; then
    # celery -A $NAME flower --port=8091 &
    celery -A $NAME flower --port=8091 --basic_auth=${ADMIN_ID}:${ADMIN_PASSWORD} &
    celery -A $NAME beat  --loglevel=DEBUG

fi  

if [ $APP_RUN == "all" ] || [ $APP_RUN == "celery-worker" ]; then
    HOSTNAME=$(hostname)
    CELERY_HOSTNAME="worker@${HOSTNAME}"
    bash -c "celery -A $NAME worker --loglevel=info --pool solo --concurrency=1 --max-tasks-per-child=100 -E --hostname=$CELERY_HOSTNAME" 
    # bash -c "celery -A $NAME worker --loglevel=info --pool threads --concurrency=1 --max-tasks-per-child=100 -E --hostname=$CELERY_HOSTNAME" &
fi

if [[ $APP_RUN != "all" ]]; then
    sleep infinity
fi

# fi

echo "Finish $NAME"