"""This is module for import classes to sorting Errors\n
Errors, Python_error, Java_error, Node_JS_error, C_error, C_sharp_error, C_plus_plus_error
"""


class Error:
    """This is the class for sorting each type of errors\n
    Line is a pozition of error"""

    def __init__(self, log, line):
        self.line = line
        self.log = log





class Python_error(Error):
    """This is the class for sorting Python errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        super().__init__(log,line)
        self.remake_log()
        self.control_line()

    def remake_log(self):
        self.add_error_type(self.log[len(self.log)-1])

    def add_error_type(self,last):
        stop=False
        self.error_type=""
        for char in last:
            if char==":":
                stop=True
            elif stop==False:
                self.error_type+=char

    def control_line(self):
        for row in self.log:
            if "File \"" in row and ", line " in row:
                loaded=False
                number=""
                for index in range(len(row)):
                    if row[index]==",":
                        loaded=False
                    if loaded==True and row[index]!=" ":
                        number+=row[index]
                    if row[index]=="e":
                        if row[index-3:index+1]=="line":
                            loaded=True
        if self.line!=int(number):
            self.line=int(number)


class Java_error(Error):
    """This is the class for sorting Java errors\n
    Line is a pozition of error"""

    def __init__(self, log, line):
        self.error = Error(log, line)


class C_error(Error):
    """This is the class for sorting C errors\n
    Line is a pozition of error"""

    def __init__(self, log, line):
        self.error = Error(log, line)


class C_sharp_error(Error):
    """This is the class for sorting C# errors\n
    Line is a pozition of error"""

    def __init__(self, log, line):
        self.error = Error(log, line)


class C_plus_plus_error(Error):
    """This is the class for sorting C++ errors\n
    Line is a pozition of error"""

    def __init__(self, log, line):
        self.error = Error(log, line)


class Node_JS_error(Error):
    """This is the class for sorting JavaScript errors\n
    Line is a pozition of error"""

    def __init__(self,log,line):
        self.error=Error(log,line)
        
Python_error(["Traceback (most recent call last):",  "File \"tests/Python_Errors/AssertionError.py\", line 15, in <module>", " assertSom(\"as\")", "  File \"tests/Python_Errors/AssertionError.py\", line 11, in assertSom","    assert (some==\"\"), \"Somefing","AssertionError: Somefing"],2)
Python_error(["Traceback (most recent call last):","  File \"tests/Python_Errors/TypeError.py\", line 1, in <module>","    print(\"Hallo world \"+1) # can only concatenate str (not \"int\") to str","TypeError: must be str, not int"],1)

