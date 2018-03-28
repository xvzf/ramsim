import re
from . import ParserException

class VarParser(object):

    svar_regex = r"^s\[(\d+)\]$"
    avar_regex = r"^a$"
    ivar_regex = r"^i[01]$"

    def __init__(self):
        self.svar = re.compile(self.svar_regex)
        self.ivar = re.compile(self.ivar_regex)
        self.avar = re.compile(self.avar_regex)

    
    def is_svar(self, var):
        """
        Checks if a variable has the form s[_]
        """

        if self.svar.match(var):
            return True
        
        return False
    

    def is_ivar(self, var):
        """
        Checks if a variable has the form i0 or i1
        """

        if self.ivar.match(var):
            return True
        
        return False
    

    def is_avar(self, var):
        """
        Checks if a variable has the form a
        """

        if self.avar.match(var):
            return True
        
        return False
        

    def get_svar_index(self, var):
        """
        Returns the i out of s[i]
        """
        matched = self.svar.match(var)
    
        if not matched:
            raise ParserException(f"Could not parse the variable '{var}''")
        
        return int(matched.group(1))