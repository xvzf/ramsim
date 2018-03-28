import re
from . import ParserException
from . import ArithmeticParser, ConditionalParser

class CmdParser(object):


    # matches "jump _"
    regular_jump_regex = \
        r"^jump\s*(\d+)$"

    # matches "if _ .. 0 then jump _"
    if_then_jump_regex = \
        r"^if\s*(i0|i1|a|s\[\d+\])\s*(<|<=|>=|>|==|!=)\s*0\s*then\s*jump\s*(\d+)$"

    # matches "_ <- _ .. _"
    arithmetic_regex = \
        r"^(a|i0|i1)\s*<-\s*(s[\d+]|a|i0|i1|\d+)\s*(\+|-|\*|mod|div)\s*(\d+|a|s\[\d+\])$"

    # matches "_ <- _"
    value_assign_regex = \
        r"^(a|i0|i1|s\[\d+\])\s*<-\s*(s\[\d+\]|a|\d+)$"

    # matches "HALT"
    halt_regex = \
        r"^HALT$"


    # determines the order of parsing operations
    matcher = ["regular_jump", "value_assign", "arithmetic", "if_then_jump", "halt"]


    def __init__(self):
        """
        Initializes the class and all matcher
        """
        self.regular_jump = re.compile(self.regular_jump_regex)
        self.if_then =      re.compile(self.if_then_jump_regex)
        self.arithmetic =   re.compile(self.arithmetic_regex)
        self.value =        re.compile(self.value_assign_regex)
        self.halt =         re.compile(self.halt_regex)

        # Subparser
        self.cond_parser =  ConditionalParser()
        self.arith_parser = ArithmeticParser()
    

    def parse(self, line: str) -> dict:
        """
        Tries to match a line, throws a ParserException if not possible
        """

        for m in self.matcher:
            try:
                return getattr(self, f"match_{m}")(line)
            except ParserException:
                pass
        
        raise ParserException("Could not parse the program line")


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
                "comparator":       self.cond_parser.parse(matched.group(2)),
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
                "operator": self.arith_parser.parse(matched.group(3)),
                "right":    matched.group(4)
                }

    
    def match_value_assign(self, line:str) -> dict:
        """
        Tries to match a line to an "a <- b" statement
        throws a ParserException if not possible
        """
        matched = self.value.match(line)

        if not matched:
            raise ParserException("Not a value assign expression")
        
        return {
            "type":     "assign",
            "target":   matched.group(1),
            "value":    matched.group(2)
        }


    def match_halt(self, line:str) -> dict:
        """
        Tries to match a line to an "a <- b" statement
        throws a ParserException if not possible
        """
        matched = self.halt.match(line)

        if not matched:
            raise ParserException("Not a HALT expression")
        
        return {
            "type": "halt"
        }