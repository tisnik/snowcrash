from app import ErrorClass
from app import bug_search
from app import language_identity
from app.sql_alchemy import *

import os

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
    errors[i] = language_identity.identify(errors[i])
    print(errors[i])

d = Database()

d.delete_all(Error)
d.delete_all(Language)
d.delete_all(Type)
d.delete_all(Solution)

d.add("Language", language="Java", regex=r"\tat [a-zA-Z.\/]+\([A-Za-z:.-_0-9 ]+\)", version="openjdk version 1.8.0_222")
d.add("Type", language="Java", type_name="NameError", msg="name resoult is not defined")
d.add("Error", "Java", "NameError", msg="name resoult is not defined", path="/home/", line=5)
d.add("Solution", "Java", "NameError", priority=0, solution="CTRL + DELETE")
d.update(Type, Type.count, 1, 2)
