from sqlite3 import *
import os
import sys
from app import constants
from app import ErrorClass


class Sql_database:

    def __init__(self, db_path="memory.db"):
        self.conn = None
        self.key = None
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """
        Init's database
        """
        if os.path.isfile(self.db_path):
            try:
                open(self.db_path, "a")
            except PermissionError as err:
                print(err)
                sys.exit(1)

        self.conn = connect(self.db_path)
        self.conn.isolation_level = None
        self.key = self.conn.cursor()
        try:
            create_sql = open(constants.database_create_script)
            query = create_sql.read().split("\n")
            for row in query:
                self.execute(row)
        except Error:
            print("Database already exists")

    def get_table(self, name, *columns):
        if len(columns) > 1:
            columns = ", ".join(columns)
        else:
            columns = columns[0]
        sql = "SELECT {} FROM {};".format(columns, name)
        self.key.execute(sql)
        return self.key.fetchall()

    def edit_row_table(self, table: str, values: dict, primary_key, pk_value) -> bool:
        """
        Updates values in table
        :param pk_value: Primary key value to match in the table
        :param primary_key: Primary key of the table
        :param table: Name of the table
        :param values: Dictionary of the values to change
        :return: True or False
        """
        vals = ""
        for key, value in values.items():
            vals += " " + key + " = \'" + str(value) + "\',"
        values = vals[:-1]
        query = "UPDATE {} SET{} WHERE {}=\'{}\';".format(table, values, primary_key, str(pk_value))
        try:
            self.key.execute(query)
            return True
        except Error:
            return False

    def execute(self, sql) -> list:
        self.key.execute(sql)
        return self.key.fetchall()

    def add_language(self, language_name: str, regex_for_language=False) -> bool:
        """
        Adding language to database
        :param language_name: Name of the language (language class without _error)
        :param regex_for_language: Optional argument, only for initial addition
        :return: True or False
        """
        if len(self.execute("SELECT Language FROM Language where Language=" + language_name)) == 0:
            return self.add_to_table("Language", [language_name, regex_for_language])
        else:
            return self.edit_row_table("Language", {"COUNT": "COUNT + 1"}, "Language", language_name)

    def add_type(self, language: str, type_name: str, msg="NULL"):
        """
        Adding type of error to DB
        :param language: name of existing language
        :param type_name: like (AssertionError)
        :param msg: msg of the type of the error
        :return: True or False
        """
        if len(self.execute(
                "SELECT TypeName, MSG FROM Type WHERE TypeName=\'{}\' AND MSG=\'{}\'".format(type_name, str(msg)))) == 0:
            return self.add_to_table("Type", [language, type_name, msg])
        else:
            return self.execute("UPDATE Type SET COUNT=COUNT + 1 WHERE TypeName=\'{}\' AND MSG=\'{}\' AND Language=\'{}\'".format(str(type_name), str(msg), str(language)))

    def remove_row_via_ID(self, table, table_pk, table_pk_value):
        self.key.execute("DELETE FROM " + str(table) + " WHERE " + str(table_pk) + "=" + str(table_pk_value))

    def get_errors(self) -> [tuple]:
        """Getting all errors from the Database - WIP"""
        return self.execute(
            "SELECT Path, Line, Errors.MSG, First, Last, Errors.COUNT, Type.Language, Type.TypeName FROM Errors LEFT "
            "JOIN Type ON Errors.TypeID=Type.TypeID")

    def get_rows_ID(self, table, table_var, table_value_min, table_value_max=False):
        ids = {'Errors': "ErrorID", 'Type': "TypeID", 'Language': "Language", 'Solution': "SolutionID"}
        if table_value_max in [False, True]:
            return self.get_table(table + " WHERE " + table_var + "=" + str(table_value_min), ids[table])
        else:
            return self.get_table(
                table + " WHERE " + table_var + " BETWEEN \'" + str(table_value_min) + "\' AND \'" + str(
                    table_value_max) + "\'", ids[table])

    def get_TypeID(self, TypeName, Language):
        list1=self.get_table("Type WHERE TypeName=\'"+str(TypeName)+"\'","TypeID")
        list2=self.get_table("Type WHERE Language=\'"+str(Language)+"\'","TypeID")
        for id1 in list1:
            for id2 in list2:
                if id1[0]==id2[0]:
                    return id1[0]
        return False

    def add_Error(self, error: ErrorClass.Error) -> bool:
        """
        This method takes Error class and inserting it to the database
        :param error: is instance Error class  
        :return: True or False 
        """
        types = self.get_table("Type", "*")
        lang = (type(error).__name__).replace("_error", "")
        if types != []:
            for row in types:
                if row[2] == error.error_type and row[1] == lang:
                    language = self.get_table("Language WHERE Language=\'" + row[1] + "\'", "COUNT")
                    self.edit_row_table("Type", {"COUNT": int(row[4] + 1)}, "TypeID", row[0])
                    self.edit_row_table("Language", {"COUNT": language[0][0] + 1}, "Language", row[1])
                    errors_control = self.get_table("Errors", "MSG, Path, Line, COUNT, ErrorID")
                    for row in errors_control:
                        if row[0] == error.error_msg and row[1] == error.path and row[2] == error.line:
                            self.edit_row_table("Error", {"COUNT": int(row[3]) + 1}, "ErrorID", row[4])
                            return True

        if not ((lang,) in self.get_table("Language", "Language")):
            print("SOME")
            for regex, language in constants.patterns.items():
                if (type(language).__name__).replace("_error", "") == lang:
                    self.add_to_table("Language", [lang, regex])
        else:
            language = self.get_table("Language WHERE Language=\'" + lang + "\'", "COUNT")
            self.edit_row_table("Language", {"COUNT": int(language[0][0]) + 1}, "Language", lang)
        return self.add_to_table("Error",
                                 [lang, error.error_type, error.path, error.line, error.error_msg, False, False])

    def add_to_table(self, table, variables=[]) -> bool:
        """
table is name of table to write. It can take values (Errors, Type, Language, Solution)
    
variables is list of variables to tables. It can take values listed below. Variables must be defined, even those that are optional. If you don't want to set a variable, enter it as False.
    
Table Errors has: 
    Language - It's a File Language (VARCHAR NOT NULL)
    Type - It's a Error type's name (VARCHAR NOT NULL)
    Path - It's a Fill Path of error (VARCHAR NULL) 
    Line - It's a Line of error (INT NULL)
    MSG - It's a Message of error (VARCHAR NULL)
    First - It's a First time of error record (YYYY-MM-DD HH-MM-SS NULL) 
    Last - It's a Last time of error record (YYYY-MM-DD HH-MM-SS NULL) 
    
Table Type has:
    Language - It's a Error Language (VARCHAR NOT NULL)
    TypeName - It's a Error type (VARCHAR NOT NULL)
    MSG - It's a Moustly use message (VARCHAR) NULL
    
Table Language has:
    Language - It's a Name of programing language (VARCHAR NOT NULL)
    Regex - It's a string to recognition File (VARCHAR NOT NULL)
    
Table Solution has: 
    Language - It's a File Language (VARCHAR NOT NULL)
    Type - It's a Error type's name (VARCHAR NOT NULL)
    Priority - It's a Priority to use Soulution, it's 1(First Use) to 999(Last Use) (INT NOT NULL)      
    Solution - It's a Solution of error (VARCHAR NOT NULL)
        """
        tables = {'Errors': [
            'SELECT TypeID FROM Type WHERE TypeName=\"' + str(variables[1]) + '\" AND Language=\"' + str(
                variables[0]) + '\"',
            'INSERT INTO Errors('],
            'Type': ['INSERT INTO Type('],
            'Language': ['INSERT INTO Language('],
            'Solution': [
                'SELECT TypeID FROM Type WHERE TypeName=\"' + str(variables[1]) + '\" AND Language=\"' + str(
                    variables[0]) + '\"',
                'INSERT INTO Solution(']}
        values = {'Errors': ["Path", "Line", "MSG", "First", "Last", "TypeID"],
                  'Type': ["Language", "TypeName", "MSG"],
                  'Language': ["Language", "Regex"],
                  'Solution': ["Priority", "Soulution", "TypeID"]}
        if table in values:
            for query in tables[str(table)]:
                if query[0:6] == "SELECT":
                    try:
                        self.key.execute(query)
                        id = self.key.fetchall()[0]
                        variables.append(id[1:-2])
                    except:
                        self.key.execute("SELECT Language FROM Language")
                        if variables[0] not in self.key.fetchall():
                            regex = input("add regex to language " + str(variables[0] + ":"))
                            regex2 = ""
                            for i in regex:
                                if i == "\"":
                                    regex2 += "\"\""
                                else:
                                    regex2 += i
                            self.add_to_table("Language", [variables[0], regex2])
                        self.add_to_table("Type", [variables[0], variables[1], False])
                        self.key.execute(query)
                        id = self.key.fetchall()[0]
                        variables.append(id[1:-2])
                elif query[0:6] == "INSERT" and table in ["Errors", "Solution"]:
                    for i in range(len(values[table])):
                        if variables[i + 2] != False:
                            query += values[table][i] + ","
                    if table == "Errors":
                        query += "ErrorID,COUNT) VALUES(\""
                    else:
                        query += "SolutionID,COUNT) VALUES(\""
                    for i in range(len(values[table])):
                        if variables[i + 2] != False:
                            query += str(variables[i + 2]) + "\",\""
                    if table == "Errors":
                        id = self.key.execute("SELECT max(ErrorID) FROM Errors").fetchall()[0]
                        if id is not int:
                            query = query[:-1] + "0"
                        else:
                            query = query[:-1] + str(int(id) + 1)
                        query += ",0)"
                    else:
                        id = self.key.execute("SELECT max(SoulutionID) FROM Solution").fetchall()[0]
                        if id is not int:
                            query = query[:-1] + "0"
                        else:
                            query = query[:-1] + str(int(id) + 1)
                        query += ",0)"
                    try:
                        self.conn.execute(query)
                        return True
                    except:
                        return False
                elif query[0:6] == "INSERT" and table in ['Type', 'Language']:
                    for i in range(len(values[table])):
                        if variables[i] != False:
                            query += values[table][i] + ","
                    if table == "Type":
                        query += "TypeID,COUNT) VALUES(\""
                    else:
                        query += "COUNT) VALUES(\""
                    for i in range(len(values[table])):
                        if variables[i] != False:
                            query += str(variables[i]) + "\",\""
                    if table == "Type":
                        id = self.key.execute("SELECT max(TypeID) FROM Type").fetchall()[0]
                        if id is not int:
                            query = query[:-1] + "0"
                        else:
                            query = query[:-1] + str(int(id) + 1)
                        query += ",0)"
                    else:
                        query = query[:-1] + "0)"
                    try:
                        self.conn.execute(query)
                        return True
                    except:
                        return False
        else:
            return False
        return False
