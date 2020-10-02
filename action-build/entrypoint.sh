#!/bin/sh

cd /github/workspace
echo "Install Python dependencies..."
pip3 install -r requirements.txt
echo "Building the website..."
python3 build.py
echo "Done!"