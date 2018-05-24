#!/bin/bash

VIRTUALENV_LOCATION=${VIRTUALENV_LOCATION:=venv}
PYTHON=${PYTHON:=/usr/bin/python3}

if [ ! -d "$VIRTUALENV_LOCATION" ]; then

    echo "Setting up Python virtualenv..."

    virtualenv -p "$PYTHON" "$VIRTUALENV_LOCATION/"

fi

source "$VIRTUALENV_LOCATION/bin/activate"

echo "Installing software components..."

pip install -r requirements.txt

echo "Setting environment variables..."

export CARTOGRAM_DATA_DIR="/home/jansky/cartogram" #Do not include a trailing slash
export CARTOGRAM_COLOR="#aaaaaa"
export CARTOGRAM_DEBUG=TRUE
export CARTOGRAM_HOST=127.0.0.1
export CARTOGRAM_PORT=5000

echo "Done."