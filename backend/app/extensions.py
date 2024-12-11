from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler
from redis import Redis

from app.config import Config

mongo = PyMongo()
scheduler = APScheduler()
request_cache = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)
