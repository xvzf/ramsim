import re
from fileinput import FileInput
from . import ParserException, CmdParser


class Parser(object):

    parse_inout_line_regex = r"[\s]*(INPUT|OUTPUT)[\s]+([\d]+)(\.\.([\d]+)[\s]*){0,1}"
    parse_program_line_regex = r"[\s]*([\d]+)[\s]*:[\s]*(.*)"


    def __init__(self, filename: str) -> None:
        """
        @TODO
        """
        self.filename = filename

        # Initialize
        self.parse_inout_line = re.compile(self.parse_inout_line_regex)
        self.parse_program_line = re.compile(self.parse_program_line_regex)
        self.program_dict = {}
        
        self.cmdparser = CmdParser()


        # Parse
        self.parse_file()

    
    def parse_inout_dict(self, f: FileInput) -> None:
        """
        Parses Input and Output
        """
        input_storage_matcher =     self.parse_inout_line.match(f.readline())
        output_storage_matcher =    self.parse_inout_line.match(f.readline())

        self.inout_dict = {
                "input": {
                    "from": int(input_storage_matcher.group(2)),
                    "to":   -1#int(input_storage_matcher.group(4))
                },
                "output": {
                    "from": int(output_storage_matcher.group(2)),
                    "to":   -1#int(output_storage_matcher.group(4))
                }
            }
        

    def parse_program_dict(self, line: str) -> None:
        """
        Parses one line of the program
        """
        matched = self.parse_program_line.match(line)

        if not matched:
            raise ParserException("Misformated line, check reference")
        
        self.program_dict[int(matched.group(1))] = matched.group(2).replace(r"\s", "")

        #self.program_dict[int(matched.group(1))] = re.sub("[\s]*", "", matched.group(2))

    
    def parse_file(self) -> None:
        """
        Parses a RAM program
        """
        with open(self.filename, "r") as f:
            self.parse_inout_dict(f)

            line_counter = 2

            for l in f.readlines():
                line_counter += 1
                
                try:
                    self.parse_program_dict(l)
                except ParserException as pe:
                    print(f"{line_counter}: {pe}")


    def get_parsed_dict(self) -> dict:
        """
        Returns the parsed program
        """

        return {"header": self.inout_dict, "program": self.program_dict}