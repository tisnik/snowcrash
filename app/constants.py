from ErrorClass import *

DICTIONARY = [Python_error, Java_error, Node_JS_error, C_error, C_sharp_error, C_plus_plus_error]
patterns = {"File \"[a-zA-Z./]+\", line [0-9]+, in ": Python_error,
           "\tat [a-zA-Z./]+\([A-Za-z ]+\)": Java_error}
