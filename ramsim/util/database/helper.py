#!/bin/env python3
#
#                       RAMSIM
#
#
#   Author:   Matthias Riegler <matthias@xvzf.tech>
#   Filename: helper.py
#
#   License:  GPLv3, see LICENSE.md
#
#

from ... import db

def remove_from_db(db_object, id):
    todel = db_object.query.filter_by(id=id).first()
    if todel:
        db.session.delete(todel)
        db.session.commit()
        return True
    return False
    