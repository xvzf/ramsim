#!/bin/env python3
#
#                       RAMSIM
#
#
#   Author:   Matthias Riegler <matthias@xvzf.tech>
#   Filename: forms.py
#
#   License:  GPLv3, see LICENSE.md
#
#

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ProcessForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    svar = StringField('svar', validators=[DataRequired()])