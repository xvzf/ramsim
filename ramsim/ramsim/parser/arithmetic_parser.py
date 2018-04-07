#!/bin/env python3
#
#                       RAMSIM
#
#
#   Author:   Matthias Riegler <matthias@xvzf.tech>
#   Filename: arithmetic_parser.py
#
#   License:  GPLv3, see LICENSE.md
#
#

from types import FunctionType
from .operators import add, substract, multiply, divide, modulo
from . import ParserException

class ArithmeticParser(object):
    
    def __init__(self):
        pass
    
    def parse(self, operator) -> FunctionType:
        if operator == "+":
            return add
        elif operator == "-":
            return substract
        elif operator == "*":
            return multiply
        elif operator == "div":
            return divide
        elif operator == "mod":
            return modulo
        
        # Not an supported operator
        raise ParserException(f"{operator} is not supported")