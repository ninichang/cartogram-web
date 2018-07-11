#!/bin/bash

if [ "${CARTOGRAM_DEBUG,,}" = "true" ]
then
    echo "Warning: You are running a production server in development mode. Is this what you want?"
fi

WORKERS=$(echo `cat /proc/cpuinfo | grep -c processor` "*2 + 1" | bc)

echo "Starting gunicorn in daemon mode with " $WORKERS " worker(s)."

gunicorn --bind $CARTOGRAM_HOST:$CARTOGRAM_PORT -w $WORKERS -D web:app
