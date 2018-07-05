import os

CARTOGRAM_DATA_DIR = os.environ['CARTOGRAM_DATA_DIR']
CARTOGRAM_COLOR = os.environ['CARTOGRAM_COLOR']
DEBUG = True if os.environ['CARTOGRAM_DEBUG'].lower() == "true" else False
DATABASE_URI = os.environ['CARTOGRAM_DATABASE_URI']

HOST = os.environ['CARTOGRAM_HOST']
PORT = int(os.environ['CARTOGRAM_PORT'])