#!/usr/bin/env python3

from re import match
from constants import *


def identify(log):
    for pattern in patterns:
        if match(pattern, log[1]):
            error = patterns[pattern]
            return error
    return False
