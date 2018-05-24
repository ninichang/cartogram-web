#!/bin/bash

if [ "${CARTOGRAM_DEBUG,,}" = "true" ]
then
    echo "Warning: You are running a production server in development mode. Is this what you want?"
fi

gunicorn --bind $CARTOGRAM_HOST:$CARTOGRAM_PORT web:app