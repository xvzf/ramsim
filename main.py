from ramsim import Parser, ParserException, Runner
from pprint import pprint
from sys import argv

if __name__ == "__main__":
    p = Parser(argv[1])

    r = Runner(p.get_parsed_dict(), debug=False)

    r.fill_input([13, 12])
 
    val = r.execute_program()

    r.export_exec_table("test.csv")
 
    print(val)