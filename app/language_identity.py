#!/usr/bin/env python3

from re import match
try:
    from app.constants import *
except:
    from constants import *

def identify(log):
    for pattern in patterns:
        if match(pattern, log[1]) or match(pattern, log[0]):
            error = patterns[pattern](log)
            return error
    return False
