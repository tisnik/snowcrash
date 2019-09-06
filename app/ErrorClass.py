"""This is module for import classes to sorting Errors\n
Errors, Python_error, Java_error, Node_JS_error, C_error, C_sharp_error, C_plus_plus_error
"""


class Error:
    """This is the class for sorting each type of errors\n
    Line is a pozition of error"""

    def __init__(self, log):
        self.line = None
        self.log = log





class Python_error(Error):
    """This is the class for sorting Python errors\n
    Line is a pozition of error"""
    def __init__(self,log):
        super().__init__(log)
        self.remake_log()

    def __str__(self):
        output=""
        for row in self.log:
            output+=row+"\n"
        output+="----------\n"
        output+="Error Type: "+self.error_type
        output+="\nError massage: "+self.error_msg
        output+="\nError File: "+self.path
        output+="\nError Line: "+str(self.line)
        output+="\n----------"
        return output 

    def remake_log(self):
        self.add_error_type_and_msg(self.log[len(self.log)-1])
        self.control_line()
        self.add_fill_path()
        print(self)

    def add_error_type_and_msg(self,last):
        self.error_type=last.split(":")[0]
        self.error_msg=last.split(":")[1][1::]

    def control_line(self):
        for row in self.log:
            if "File \"" in row and ", line " in row:
                line=row.split(",")[-2]
                line=line[1::].split(" ")[-1]
        self.line=int(line)


    def add_fill_path(self):
        self.path=""
        for row in self.log:
            if "File \"" in row and ", line " in row:
                path=row.split("\"")[1:len(row.split("\""))-1]
                fill_path=""
                for i in path:
                    fill_path+=i
        self.path=fill_path
                    
                

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
        
Python_error(["Traceback (most recent call last):",  "File \"tests/Python_Errors/AssertionError.py\", line 15, in <module>", " assertSom(\"as\")", "  File \"tests/Python_Errors/Letadlo23.py\", line 11, in assertSom","    assert (some==\"\"), \"Somefing","AssertionError: Somefing"])
Python_error(["Traceback (most recent call last):","  File \"tests/Python_Errors/TypeError.py\", line 1, in <module>","    print(\"Hallo world \"+1) # can only concatenate str (not \"int\") to str","TypeError: must be str, not int"])

