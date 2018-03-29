import os

INITIAL_REDIRECT = "/core"

DEBUG = True
SECRET_KEY = 'ramsim@development'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../db-dev.sqlite3')
