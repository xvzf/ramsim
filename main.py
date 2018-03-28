from ramsim import Parser, ParserException, Runner
from pprint import pprint
from sys import argv

if __name__ == "__main__":
    p = Parser(argv[1])

    r = Runner(p.get_parsed_dict(), debug=True)

    r.fill_input([1,2])
 
    val = r.execute_program()
 
    print("====DONE====")
    print(val)