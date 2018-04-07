from pprint import pprint
from time import time
from . import RunnerException
from .assertions import assert_true
from ..parser.var_parser import VarParser


class Runner(object):

# @WTF @TODO
#   state = {
#       "s":    {},
#       "a":    0,
#       "i0":   0,
#       "i1":   0,
#       "line": 0
#   }
#
#
#   initialized = False
#   executed = False
#   exec_table = []

    
    def __init__(self, parsed_dict, debug=False, timeout=3):
        """
        Initialize
        """
        self.parsed_dict = parsed_dict
        self.program = self.parsed_dict["program"]
        self.debug = debug
        self.timeout=timeout

        # For whatever reason this is not cleared after the object is destroyed?!
        # @TODO
        self.exec_table = []
        self.initialized = False
        self.executed = False
        self.state = {
            "s":    {},
            "a":    0,
            "i0":   0,
            "i1":   0,
            "line": 0
        }
    

    def debug_print(self, function_name=""):
        """
        Just for debugging
        """
        if self.debug:
            print(f"Runner.{function_name}:")
            pprint(self.state)
    

    def add_to_exec_table(self):
        """
        Adds the current line & state to the execution table
        """

        # Create new dict otherwise just the reference gets stored

        toappend = self.state.copy()
        toappend["s"] = toappend["s"].copy()
        self.exec_table.append(toappend)

    
    def get_exec_table(self):
        """
        Returns the execution table
        """
        return self.exec_table
    

    def export_exec_table(self, filename):
        """
        Exports the execution table to a csv file
        """
        def write_csv_row(f, towrite):
            f.write(
                ";".join(
                    map(
                        lambda x: f"\"{x}\"",
                        towrite
                    )
                ) + "\r\n"
            )

        try:

            with open(filename, "w") as f:
                write_csv_row(f, self.state.keys())

                for s in self.exec_table:
                    write_csv_row(f, s.values())
        
        except IOError:

            raise RunnerException("Could not export to csv")


    
    def fill_input(self, input_array):
        """
        Populates the input
        """
        a = self.parsed_dict["header"]["input"]["from"]
        e = self.parsed_dict["header"]["input"]["to"]

        # More than 1 value
        if e:
            # Check correct input length
            calculated_input_length = e - a + 1
            assert_true(0, len(input_array) == calculated_input_length, msg="invalid variable initialization")

            for i in range(calculated_input_length):
                self.state["s"][i + a] = input_array[i]
        
        # Just 1 value
        else:
            assert_true(0, len(input_array) == 1)
            self.state["s"][0] = input_array[0]
        

        # Set internal state to initialized
        self.initialized = True
        
        #For debugging purpouses
        self.debug_print("fill_input")
    

    def execute_program(self):
        """
        Executes the program
        """
        
        if not self.initialized:
            raise RunnerException("Input needs to be filled first!")

        a = self.parsed_dict["header"]["output"]["from"]
        e = self.parsed_dict["header"]["output"]["to"]

        if not self.executed:
            self.starttime = time()
            self.execute()
            self.executed = True

        toret = []

        if e:
            for i in range(a, e + 1):
                toret.append(self.state["s"][i])
        else:
            toret.append(self.state["s"][a])
        
        return toret



    def execute(self):
        """
        Execution loop, returns when finished
        throws an Exception when the execution time is exceeded
        """
        currpos = 0 # Start at line 0

        while True:
            if time() - self.starttime > self.timeout:
                raise RunnerException("Execution took to long, aborting")

            try:
                toexec = self.program[currpos]
                self.state["line"] = currpos

                # End of program
                if toexec["type"] == "halt":
                    break
                
                # Execute jump
                elif toexec["type"] == "jump":
                    currpos = int(toexec["jumpto"])
                    continue

                # Execute assign
                elif toexec["type"] == "assign":
                    self.eval_assign(toexec["target"], toexec["value"])
                
                # Execute Arithmetic
                elif toexec["type"] == "arithmetic":
                    self.eval_assign(toexec["target"],
                                    self.eval_arithmetic(
                                        toexec["operator"],
                                        toexec["left"],
                                        toexec["right"]
                                    ))
                
                # Execute conditional jump
                elif toexec["type"] == "ifthenjump":
                    if self.eval_ifthenjump(
                            toexec["comparator"],
                            toexec["left"]):

                        currpos = int(toexec["jumpto"])
                        continue

                    else:
                        pass
                
                else:
                    raise RunnerException(f"Line {currpos}: Invalid")
            
            except ValueError:
                raise RunnerException(f"Line {currpos}: Invalid")
            
            except KeyError:
                raise RunnerException(f"Line {currpos}: Invalid") 
            
            # Debug output
            self.add_to_exec_table()
            self.debug_print("execute")

            # execute next instruction
            currpos = currpos + 1 
    

    ##### Eval #####

    def eval_assign(self, key, value):
        """
        Assigns a value either out of memory or fixed to a storage position
        """

        if VarParser().is_svar(key):
            self.state["s"][VarParser().get_svar_index(key)] = self.eval_var_val(value)

        else:
            self.state[key] = self.eval_var_val(value)
    

    def eval_var_val(self, value):
        """
        Evaluates the value of a variable
        """
        # Check if already an int
        if type(value) == int:
            return value

        # get value out of storage
        if VarParser().is_svar(value):
            return self.state["s"][VarParser().get_svar_index(value)]

        # take value out of an index register
        elif VarParser().is_ivar(value) or VarParser().is_avar(value):
            return self.state[value]
        
        # Is a constant
        else:
            return int(value)


    def eval_arithmetic(self, operator, left, right):
        """
        Evaluates the result of an arithmetic expression
        """
        return operator(self.eval_var_val(left),
                        self.eval_var_val(right))

    
    def eval_ifthenjump(self, comparator, left):
        return comparator(self.eval_var_val(left))
