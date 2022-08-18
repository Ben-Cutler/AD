import os

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))

MEAN_SEND_TIME = float(os.environ.get('MEAN_SEND_TIME', 2))
HOST = '127.0.0.1'
PORT = 8080