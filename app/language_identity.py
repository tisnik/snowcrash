#!/usr/bin/env python3
from constants import *


def identify(log, indentificators=IDENTIFICATORS):
    for identificator in indentificators:
        if identificator[0] == log[0][identificator[1]:identificator[1] + len(identificator[0])]:
            error = DICTIONARY[0](log)
            return error
    return False
