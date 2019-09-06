from ErrorClass import *

DICTIONARY = [Python_error, Java_error, Node_JS_error, C_error, C_sharp_error, C_plus_plus_error]
patterns = {r"  File \"[a-zA-Z0-9.\/_-]+\", line [0-9]+, in ": Python_error,
            r"\tat [a-zA-Z.\/]+\([A-Za-z:.-_0-9 ]+\)": Java_error}
