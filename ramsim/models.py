#!/bin/env python3
#
#                       RAMSIM
#
#
#   Author:   Matthias Riegler <matthias@xvzf.tech>
#   Filename: models.py
#
#   License:  GPLv3, see LICENSE.md
#
#

from . import db
from sqlalchemy.exc import IntegrityError
import os

class CodeExec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False)
    codepath = db.Column(db.String, unique=True, nullable=False)
    svars = db.Column(db.String, nullable=False)

    # Fill out after running
    errors = db.Column(db.String, nullable=True)
    result = db.Column(db.String, nullable=True)
    error = db.Column(db.Boolean, nullable=True)
    csvpath = db.Column(db.String, unique=True, nullable=True)

    def __repr__(self):
        return f"< CodeExec {self.uuid}>"
    
    @staticmethod
    def add_to_db(uuid, svars):
        codepath = os.path.join(os.getcwd(), f"ramsim/static/code/{uuid}.ramsim")
        toadd = CodeExec(uuid=uuid, codepath=codepath, svars=svars)
        db.session.add(toadd)
        db.session.commit()

        return codepath