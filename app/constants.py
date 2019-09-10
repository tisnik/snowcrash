from app.ErrorClass import *

DICTIONARY = [Python_error, Java_error, Node_JS_error, C_error, C_sharp_error, C_plus_plus_error]
patterns = {r"[ ]*File \"[ -ž]*\", line [0-9]+": Python_error,
            r"\tat [a-zA-Z.\/]+\([A-Za-z:.-_0-9 ]+\)": Java_error}
database_create_script = "./tests/SQL/SQL_Create_Database_Query.sql"
