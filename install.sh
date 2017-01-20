#!/usr/bin/env bash

# Install dependencies either into the virtual environment, or locally for the user
if [[ -z "$VIRTUAL_ENV" ]]; then
    args='--user'
else
    args=''
fi

pip3 install $args flask flask-assets markdown bleach sqlalchemy sqlalchemy_utils flask-scss

