#!/bin/bash

VIRTUALENV_LOCATION=${VIRTUALENV_LOCATION:=venv}
PYTHON=${PYTHON:="/usr/bin/env python3"}
PIP=${PIP:="/usr/bin/env pip"}

if [ ! -d "$VIRTUALENV_LOCATION" ]; then

    echo "Setting up Python virtualenv..."

    virtualenv -p "$PYTHON" "$VIRTUALENV_LOCATION/"

fi

source "$VIRTUALENV_LOCATION/bin/activate"

echo "Installing software components..."

$PIP install -r requirements.txt

echo -n "Setting environment variables... "

source ./envsettings.sh

if [ $? -eq 0 ]; then

    echo "OK"
else

    echo "FAIL"
    echo
    echo "Please make sure that envsettings.sh exists."
    deactivate
fi

echo "Done."