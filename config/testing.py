#!/bin/env python3
#
#                       RAMSIM
#
#
#   Author:   Matthias Riegler <matthias@xvzf.tech>
#   Filename: testing.py
#
#   License:  GPLv3, see LICENSE.md
#
#

import os

INITIAL_REDIRECT = "/core"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../db-testing.sqlite3')