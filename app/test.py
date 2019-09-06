import ErrorClass
import bug_search
import language_identity

with open("../tests/logs/java/StackOwerFlow.log") as java, open("../tests/logs/python/AssertionError.txt") as python:
    err1 = bug_search.get_error_from_log(java.read())
    err2 = bug_search.get_error_from_log(python.read())

    print(err1)
    print(type(err1))
    err1 = language_identity.identify(err1)
    print(type(err1))

    print(err1)

    print(err2)
    print(type(err2))
    err2 = language_identity.identify(err2)
    print(type(err2))

    print(err2)
