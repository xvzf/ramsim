from types import FunctionType
from .operators import greater_or_equal_zero, greater_zero, equal_zero, less_or_equal_zero, less_than_zero
from . import ParserException

class ConditionalParser(object):
    
    def __init__(self):
        pass
    
    def parse(self, operator) -> FunctionType:
        if operator == "<":
            return less_than_zero
        elif operator == "<=":
            return less_or_equal_zero
        elif operator == "==" or operator == "=":
            return equal_zero
        elif operator == ">=":
            return greater_or_equal_zero
        elif operator == ">":
            return greater_zero
        
        # Not an supported operator
        raise ParserException(f"{operator} is not supported")