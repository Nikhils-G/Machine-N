#!/bin/bash
apt-get update
apt-get install -y wget unzip xvfb libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libxshmfence1 libxss1 libx11-xcb1 libxtst6

python -m playwright install --with-deps
