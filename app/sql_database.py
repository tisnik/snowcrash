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
                "SELECT TypeName, MSG FROM Type WHERE TypeName=\'{}\' AND MSG=\'{}\'".format(type_name,
                                                                                             str(msg)))) == 0:
            return self.add_to_table("Type", [language, type_name, msg])
        else:
            return self.execute(
                "UPDATE Type SET COUNT=COUNT + 1 WHERE TypeName=\'{}\' AND MSG=\'{}\' AND Language=\'{}\'".format(
                    str(type_name), str(msg), str(language)))

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

    def add_solution(self, language: str, type_name: int, priority: int, solution: str, solved: bool = False):
        if len(self.execute("SELECT * FROM Solution WHERE Solution=" + solution)) == 0:
            self.add_to_table("Solution", [language, type_name, priority, solution])
        else:
            edit_sql = "UPDATE Solution SET {}={} WHERE Solution={}"
            if solved:
                self.execute(edit_sql.format("Solved", "Solved + 1", solution))
            else:
                self.execute(edit_sql.format("Unsolved", "Unsolved + 1", solution))

    def get_TypeID(self, TypeName, Language):
        list1 = self.get_table("Type WHERE TypeName=\'" + str(TypeName) + "\'", "TypeID")
        list2 = self.get_table("Type WHERE Language=\'" + str(Language) + "\'", "TypeID")
        for id1 in list1:
            for id2 in list2:
                if id1[0] == id2[0]:
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

    def parse_table(self, template, variables) -> bool:
        i = 0
        if len(variables) < len(template):
            variables = variables +\
                [None for _ in range(len(template) - len(variables))]
        for attribute in template:
            template[attribute] = str(variables[i])
            i += 1
        return template
        
    def add_to_table(self, table, variables) -> bool:
        """
        the table is the name of the table to write.
        It can take values (Errors, Type, Language, Solution)
        variables are a list of variables to tables.
        It can take the values listed below.
        Variables must be defined, even those that are optional.
        If you don't want to set a variable, enter it as False.
        """
        select = "SELECT {} FROM {} WHERE {} = \'{}\' AND {} = \'{}\';"
        insert = "INSERT INTO {}({}) VALUES(\'{}\');"
        values = {'Errors': {"Path": None, "Line": None, "MSG": None,
                            "First": None, "Last": None, "TypeID": None},
                'Type': {"Language": None, "TypeName": None, "MSG": None},
                'Language': {"Language": None, "Regex": None},
                'Solution': {"Solution": None, "Priority": None, "TypeID": None}}

        if table in values:
            for template in values:
                if template in ["Errors", "Solution"] and template == table:
                    sql = select.format("TypeID", "Type",
                                        "Language", variables[0][0],
                                        "TypeName", variables[0][1])

                    variables = variables[1]
                    self.key.execute(sql)

                if table == "Type":
                    condition = "Language"
                    value = self.parse_table(values[condition], variables)
                    sql = select.format(condition, condition, condition,
                                        value[condition], "\'1\'", 1)

                    self.key.execute(sql)
                    response = len(self.key.fetchall())
                    if response == 0:
                        print("Not {} for curren {}".format(condition, table))
                        return False

                if template == table:
                    value = self.parse_table(values[table], variables)
                    if table == "Solution":
                        value["Solved"] = "0"
                        value["Unsolved"] = "0"
                    else:
                        value["COUNT"] = "0"
                    if table in ["Errors", "Solution"]:
                        response = self.key.fetchall()[0][0]
                        value["TypeID"] = str(response)

                    sql = insert.format(table, ", " .join(value),
                                        "\', \'".join(value.values()))
                    try:
                        self.key.execute(sql)
                    except IntegrityError:
                        print("Language {} already in database"
                            .format(value[table]))

                    print(sql)
                    return True