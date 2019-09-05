"""This is module for import classes to sorting Errors\n
Errors, Python_error, Java_error, Node_JS_error, C_error, C_sharp_error, C_plus_plus_error
"""

class Error:
    """This is the class for sorting each type of errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        self.line=line
        self.log=log






class Python_error(Error):
    """This is the class for sorting Python errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        super.__init__(log,line)
    
    def remake_log(self):
        pass


class Java_error(Error):
    """This is the class for sorting Java errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        self.error=Error(log,line)


class C_error(Error):
    """This is the class for sorting C errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        self.error=Error(log,line)


class C_sharp_error(Error):
    """This is the class for sorting C# errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        self.error=Error(log,line)


class C_plus_plus_error(Error):
    """This is the class for sorting C++ errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        self.error=Error(log,line)


class Node_JS_error(Error):
    """This is the class for sorting JavaScript errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        self.error=Error(log,line)