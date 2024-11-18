#!/bin/bash

cd src || { echo "Directory 'src' not found."; exit 1; }

gunicorn --bind 0.0.0.0:8008 config.wsgi