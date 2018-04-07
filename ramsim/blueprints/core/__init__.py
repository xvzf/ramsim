#!/bin/env python3
#
#                       RAMSIM
#
#
#   Author:   Matthias Riegler <matthias@xvzf.tech>
#   Filename: __init__.py
#
#   License:  GPLv3, see LICENSE.md
#
#

from ...util.framework.blueprint import create_blueprint

blueprint = create_blueprint("core", __name__)

from . import views
