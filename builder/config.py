import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_PATH = os.path.join(BASE_PATH, 'docs')
DATA_URL = os.getenv('INPUT_DATA_URL', 'https://docs.google.com/spreadsheets/d/1EDLlUuY2Ia5MKNbCTOftxxSxBaK3C9pRFOIUvMY30eY/edit?usp=sharing')
API_KEY = os.getenv('INPUT_API_KEY', '')