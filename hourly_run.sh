#!/bin/bash

LOCKFILE="/tmp/hourly_run.lock"

if [ -e "$LOCKFILE" ]; then
    echo "Hourly update is already running. Exiting."
    exit 1
fi

touch "$LOCKFILE"

cd ~/services/ATG

source .venv/bin/activate

python main.py
deactivate

rm "$LOCKFILE"
