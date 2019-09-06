import ErrorClass
import bug_search
import language_identity

with open("../tests/logs/java/ConnectException.log") as java, open("../tests/logs/python/AssertionError.txt") as python:
    errors = [bug_search.get_error_from_log(java.read()),bug_search.get_error_from_log(python.read())]
    for error in errors:
        error = language_identity.identify(error)
        print(error)

