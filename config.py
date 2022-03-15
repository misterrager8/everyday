import os

import dotenv

dotenv.load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("db_url")
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 60}
SQLALCHEMY_TRACK_MODIFICATIONS = False
ENV = os.getenv("env")
DEBUG = os.getenv("debug")
SECRET_KEY = os.getenv("secret_key")
