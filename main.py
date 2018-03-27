from ramsim import Parser, ParserException
from pprint import pprint

if __name__ == "__main__":
    p = Parser("test.ram")

    for _, line in p.get_parsed_dict()["program"].items():
        try:
            pprint(p.cmdparser.match_if_then_jump(line))
        except ParserException:
            pass
