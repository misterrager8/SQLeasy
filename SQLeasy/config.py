import os

import dotenv

dotenv.load_dotenv()

DEBUG = os.getenv("debug")
ENV = os.getenv("env")

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
