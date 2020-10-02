FROM python:3.7-buster

VOLUME . /app
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r research-group-static-web/requirements.txt

# Build the website
RUN python3 research-group-static-web/build.py