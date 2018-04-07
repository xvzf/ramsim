import os

INITIAL_REDIRECT = "/core"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../db-testing.sqlite3')