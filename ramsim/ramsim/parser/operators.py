#!/bin/env python3
#
#                       RAMSIM
#
#
#   Author:   Matthias Riegler <matthias@xvzf.tech>
#   Filename: operators.py
#
#   License:  GPLv3, see LICENSE.md
#
#



# Arithmetic operations

def add(a: int, b: int):
    return a + b

def substract(a: int, b: int):
    return a - b

def multiply(a:int, b: int):
    return a * b

def divide(a: int, b: int):
    return a / b

def modulo(a: int, b: int):
    return a % b



# Comparators

def greater_zero(a: int) -> bool:
    return a > 0

def greater_or_equal_zero(a: int) -> bool:
    return a >= 0

def less_than_zero(a:int) -> bool:
    return a < 0

def less_or_equal_zero(a:int) -> bool:
    return a <= 0

def equal_zero(a: int) -> bool:
    return a == 0

def not_equal_zero(a:int) -> bool:
    return a != 0