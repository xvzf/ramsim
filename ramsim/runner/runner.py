from pprint import pprint
from .assertions import assert_true
from . import RunnerException
from ..parser.var_parser import VarParser


class Runner(object):

    state = {
        "s":    {},
        "a":    0,
        "i0":   0,
        "i1":   0
    }


    initialized = False
    executed = False

    
    def __init__(self, parsed_dict, debug=False):
        """
        Initialize
        """
        self.parsed_dict = parsed_dict
        self.program = self.parsed_dict["program"]
        self.debug = debug
    

    def debug_print(self, function_name=""):
        if self.debug:
            print(f"Runner.{function_name}:")
            pprint(self.state)

    
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
            assert_true(0, len(input_array) == calculated_input_length)

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
            self.execute()
            self.executed = True

        toret = []

        if e:
            for i in range(a, e + 1):
                toret.append(self.state["s"][i])
        else:
            toret.append(self.state["s"][a])
        
        return toret



    def execute(self,currpos=0):
        """
        Executes one line at a time, calls recursive
        """
        toexec = self.program[currpos]

        try:
            # End of program
            if toexec["type"] == "halt":
                return
            
            # Execute jump
            elif toexec["type"] == "jump":
                return self.execute( int(toexec["jumpto"]) )

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

                    return self.execute(int(toexec["jumpto"]))

                else:
                    pass
            
            else:
                raise RunnerException(f"Line {currpos}: Invalid")
        
        except ValueError:
            raise RunnerException(f"Line {currpos}: Invalid")
        
        except KeyError:
            raise RunnerException(f"Line {currpos}: Invalid") 
        
        # Debug output
        self.debug_print("execute")
        # execute next instruction
        return self.execute( currpos + 1 )
    

    ##### Eval #####

    def eval_assign(self, key, value):
        """
        Assigns a value either out of memory or fiexed to a storage position
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