#!/bin/bash

if [ -f DO_NOT_START ]; then
  echo "Not starting. Magic file found: DO_NOT_START"
else
  python rpi-music-by-light.py
fi

