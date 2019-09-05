"""This is module for import classes to sorting Errors\n
Errors, Python_error, Java_error, Node_JS_error, C_error, C_sharp_errors, C_plus_plus_errors
"""

class Error:
    """This is the class for sorting each type of errors\n
    Line is a pozition of error"""
    def __init__(self,line):
        self.line=line

class Python_error(Error):
    """This is the class for sorting Python errors\n
    Line is a pozition of error"""
    def __init__(self,line):
        self.error=Error(line)
class Java_error(Error):
    """This is the class for sorting Java errors\n
    Line is a pozition of error"""
    def __init__(self,line):
        self.error=Error(line)
class C_error(Error):
    """This is the class for sorting C errors\n
    Line is a pozition of error"""
    def __init__(self,line):
        self.error=Error(line)
class C_sharp_errors(Error):
    """This is the class for sorting C# errors\n
    Line is a pozition of error"""
    def __init__(self,line):
        self.error=Error(line)
class C_plus_plus_errors(Error):
    """This is the class for sorting C++ errors\n
    Line is a pozition of error"""
    def __init__(self,line):
        self.error=Error(line)
class Node_JS_error(Error):
    """This is the class for sorting JavaScript errors\n
    Line is a pozition of error"""
    def __init__(self,line):
        self.error=Error(line)