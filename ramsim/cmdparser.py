import re
from . import ParserException

class CmdParser(object):


    regular_jump_regex = r"jump\s*(\d+)\s*"

    if_then_regex = r"if\s*(i0|i1|a|s\[\d+\])\s*(<|<=|>=|>|==|!=)\s*0\s*then\s*jump\s*(\d+)"

    arithmetic_regex = r"" #@TODO

    index_regex = r"" #@TODO


    def __init__(self):
        """
        Initializes the class and all matcher
        """
        self.regular_jump = re.compile(self.regular_jump_regex)
        self.if_then = re.compile(self.if_then_regex)
        self.arithmetic = re.compile(self.arithmetic_regex)
        self.index = re.compile(self.index_regex)
    

    def match(self, line: str) -> dict:
        """
        Tries to match a line, throws a ParserException if not possible
        """
        pass
    

    def match_if_then_jump(self, line: str):
        """
        Tries to match a line to an "if then jump" statement
        throws a ParserException if not possible
        """
        matched = self.if_then.match(line)

        if not matched:
            raise ParserException("Not an if->then")
        
        return {
                "type":             "ifthenjump",
                "left":             matched.group(1),
                "comparetozero":    matched.group(2),
                "jumpto":           matched.group(3)
                }
        

    def match_regular_jump(self, line: str):
        """
        Tries to match a line to an "jump " statement
        throws a ParserException if not possible
        """
        matched = self.regular_jump.match(line)

        if not matched:
            raise ParserException("Not a regular jump")
        
        return {
            "type":     "jump",
            "jumpto":   matched.group(1)
            }
    

    def match_arithmetic(self, line: str) -> dict:
        """
        Tries to match a line to an "a <- a _ b" statement
        throws a ParserException if not possible
        """
        matched = self.arithmetic.match(line)

        if not matched:
            raise ParserException("Not an arithmetic expression")
        
        return {
                "type":     "arithmetic",
                "target":   matched.group(1),
                "left":     matched.group(2),
                "operator": matched.group(3),
                "right":    matched.group(4)
                }


    def match_index(self, line):
        """
        Tries to match a line to an "i_ <- i_ +/- 1" statement
        throws a ParserException if not possible
        """
        matched = self.index.match(line)

        if not matched:
            raise ParserException("Not affecting an index register")
        
        return {
            # @TODO
                }