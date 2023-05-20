#!/bin/bash

cd "$(dirname "$0")"
while true; do
  termine="$(./termine.py "https://termin.bremen.de/termine/directentry?..." "2023-05-20 13:50")"
  if [[ $? -eq 0 ]]; then
    echo "$termine" | mail -s "Neue Termine" "!jEsUZKDJdhlrceRyVU:example.org"
  fi
  sleep 15m
done
