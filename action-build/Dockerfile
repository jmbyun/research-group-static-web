FROM python:3.7-buster

VOLUME . /app
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Run the script
ENTRYPOINT ["/entrypoint.sh"]