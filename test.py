from app import ErrorClass
from app import bug_search
from app import language_identity
from app.sql_database import *

import os

sql_database = Sql_database()

errors = []
for root, dirs, files in os.walk("./tests/logs/python"):
    for filename in files:
        errors.append(open("./tests/logs/python/" + filename))
for root, dirs, files in os.walk("./tests/logs/java"):
    for filename in files:
        errors.append(open("./tests/logs/java/" + filename))
for i in range(len(errors)):
    errors[i] = bug_search.get_error_from_log(errors[i].read())
for i in range(len(errors)):
    pass
    #errors[i] = language_identity.identify(errors[i])
    #sql_database.add_Error(errors[i])

    
# try something
test = Sql_database()  # Create Test connect to database memory.db
#print("Deleted?")
#print(test.restart_all())

