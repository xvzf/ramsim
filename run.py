#!/bin/env python3
#
#                       RAMSIM
#
#
#   Author:   Matthias Riegler <matthias@xvzf.tech>
#   Filename: run.py
#
#   License:  GPLv3, see LICENSE.md
#
#

from ramsim import create_app, db
from os import urandom
from importlib import import_module


def generate_secret_key(configtype):

    with open(f"config/{configtype}.py", "a") as config:
        config.write(f"\nSECRET_KEY = {urandom(16)}\n")


if __name__ == "__main__":
    configtype = "testing"

    # Check if config file contains a secret key, otherwise generate it
    if not hasattr( import_module(f"config.{configtype}"), "SECRET_KEY"):
        generate_secret_key(configtype)

    # Create app
    app = create_app(configtype)
    
    with app.app_context():
        # Initialize Database
        db.create_all()

    app.run(host="0.0.0.0", port=80)
