#!/usr/bin/env python3
from ErrorClass import *

identficators = [["Traceback", 0], ["Exception", 0]]
dictionary = [Python_error, Java_error, Node_JS_error, C_error, C_sharp_error, C_plus_plus_error]

def identify(log):
    for identificator in indentificators:
        if identificator[0] == log[0][identificator[1]:identificator[1]+len(identificator[0])]:
            error = dictionary[0](log)
    return error

