import constants
import re


def get_line_of_error(log):
    errors = constants.IDENTIFICATORS
    for l in range(len(log)):
        for err in errors:
            if log.startswith(err[0]):
                return l


def get_error_from_log(log):
    line = get_error_from_log(log)
    return log.substring(line-1)
