from app import constants
from app.ErrorClass import *
import re

''' Getting start line of error'''


def get_line_of_error(log):
    errors = constants.patterns
    for line_number, line in enumerate(log.split("\n"), 1):
        for err in errors.keys():
            if re.match(err, line):
                if not (line[0] == " ") and errors[err] is Python_error:
                    return line_number - 2
                else:
                    return line_number - 1


''' Separating error form log '''


def get_error_from_log(log):
    line = get_line_of_error(log)
    log = log.split("\n")
    return log[line:-1]


if __name__ == "__main__":
    with open("../tests/logs/java/ConnectException.log") as f:
        print(get_error_from_log("jsah\ndjk\nash\n" + f.read()))
