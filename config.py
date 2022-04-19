import os

import dotenv

dotenv.load_dotenv()

DEBUG = os.getenv("debug")
ENV = os.getenv("env")
SECRET_KEY = os.getenv("secret_key")
SQLALCHEMY_DATABASE_URI = os.getenv("db_url")
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 60}
