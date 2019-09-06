import ErrorClass
import bug_search
import language_identity

import os

errors=[]
for root, dirs, files in os.walk("../tests/logs/python"):
    for filename in files:
        errors.append(open("../tests/logs/python/"+filename))
for root, dirs, files in os.walk("../tests/logs/java"):
    for filename in files:
        errors.append(open("../tests/logs/java/"+filename))
for i in range(len(errors)):
    errors[i]=bug_search.get_error_from_log(errors[i].read())
for i in range(len(errors)):
    errors[i] = language_identity.identify(errors[i])
    print(errors[i])
for i in range(len(errors)):
    print(errors[i])

