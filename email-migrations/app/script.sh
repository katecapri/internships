#!/bin/bash

cd src || { echo "Directory 'src' not found."; exit 1; }

alembic upgrade head
