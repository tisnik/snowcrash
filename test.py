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
#for i in range(len(errors)):
    #errors[i] = language_identity.identify(errors[i])
    #sql_database.add_Error(errors[i])
    #print(errors[i])

# Working
test = Sql_database()  # Create Test connect to database memory.db
print(test.get_table("Language", "Language, COUNT"))  # SELECT Language, COUNT FROM Language
test.edit_row_table("Type", {"COUNT": 1, "MSG": "NULL"}, "TypeID", 0)  # UPDATE type SET COUNT='2', MSG="NULL" WHERE TypeID="0" (need have in table some Type Error where ID is 0)
test.edit_row_table("Language", {"COUNT": 1}, "Language", "Python")
print(test.get_rows_ID("Type", "COUNT", 0, 3))  # SELECT TypeID FROM Tpe WHERE COUNT BETWEEN '0' AND '3'
try:
    test.remove_row_via_ID("Errors", "ErrorID",
                           test.get_rows_ID("Errors", "First", "NULL"))  # the part below must work first
except Exception as error:
    print("Error: " + str(error) + "the part \"Not Working#1\" must work first")
# Not Working
print(test.add_Error(language_identity.identify(bug_search.get_error_from_log("""Traceback (most recent call last):
  File \"tests/Python_Errors/IndexError.py\", line 2, in <module>
    print(list[4]) #list index out of range
IndexError: list index out of range
"""))))  # (Not Working#1)
