FROM python:3.7-buster

WORKDIR $GITHUB_WORKSPACE

# Install Git
RUN apt-get update \
    && apt-get install -y git

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Build the website
RUN python3 build.py