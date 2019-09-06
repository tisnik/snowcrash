"""This is module for import classes to sorting Errors\n
Errors, Python_error, Java_error, Node_JS_error, C_error, C_sharp_error, C_plus_plus_error
"""

class Error:
    """This is the class for sorting each type of errors\n
    Line is a pozition of error"""
    def __init__(self,log):
        self.line=None
        self.error_type = None
        self.error_msg = None
        self.path = None
        self.log=log

    def __str__(self):
        output = ""#Error Log: \n"
        #output+="".join(list(map(lambda x: x+"\n", self.log)))
        output+="----------\n"
        output+="Error Type: "+str(self.error_type)
        output+="\nError massage: "+str(self.error_msg)
        output+="\nError File: "+str(self.path)
        output+="\nError Line: "+str(self.line)
        output+="\n----------"
        return output



class Python_error(Error):
    """This is the class for sorting Python errors\n
    Line is a pozition of error"""
    def __init__(self,log):
        super().__init__(log)
        self.remake_log()


    def remake_log(self):
        self.add_error_type_and_msg(self.log[len(self.log)-1])
        self.control_line()
        self.add_fill_path()
        #print(super())

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
    def __init__(self,log):
        super().__init__(log)
        self.remake_log()

    def remake_log(self):
        first, last = self.log[0], self.log[-1]
        if ":" in first:
            first, *self.error_msg = first.split(":")
            self.error_msg = "".join(self.error_msg)
        else:
            self.error_msg = "None"
        self.error_type = first.split(" ")[-1]

        if ":" in last:
            last = last.split("(")[1].split(":")
            self.path = last[0]
            self.line = int(last[1].replace(")", ""))
        #print(super())

class C_error(Error):
    """This is the class for sorting C errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        super().__init__(log, line)

class C_sharp_error(Error):
    """This is the class for sorting C# errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        super().__init__(log, line)


class C_plus_plus_error(Error):
    """This is the class for sorting C++ errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        super().__init__(log, line)


class Node_JS_error(Error):
    """This is the class for sorting JavaScript errors\n
    Line is a pozition of error"""
    def __init__(self,log,line):
        super().__init__(log, line)
