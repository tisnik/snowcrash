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

    def __str__(self):
        ret_str = "Language: " + str(self.get_table("Language", "Language, Version, COUNT"))
        ret_str += "\nType: " + str(self.get_table("Type", "TypeName, Language, COUNT"))
        ret_str += "\nError: " + str(self.get_table("Error", "ErrorID, Path, Line, MSG, COUNT"))
        ret_str += "\nSolution: " + str(self.get_table("Solution", "Priority, Solution"))
        return ret_str

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

    def add_language(self, language_name: str, language_version=False, regex_for_language=False) -> bool:
        """
        Adding language to database
        :param language_version: Version of the language
        :param language_name: Name of the language (language class without _error)
        :param regex_for_language: Optional argument, only for initial addition
        :return: True or False
        """
        language_version = str(language_version)
        language_ids = self.execute(
            "SELECT LanguageID FROM Language where Language=\'" + str(language_name) + "\' AND " +
            "Version=\'" + str(language_version) + "\';")
        if len(language_ids) == 0:
            return self.add_to_table("Language", [language_name, regex_for_language, language_version])
        else:
            return self.count_increase("LanguageID", language_ids[0][0])

    def add_type(self, language: str, type_name: str, language_version: int = False, msg="NULL"):
        """
        Adding type of error to DB
        :param language_version:
        :param language: language of the string
        :param type_name: like (AssertionError)
        :param msg: msg of the type of the error
        :return: True or False
        """
        if len(self.execute(
                "SELECT TypeName, MSG FROM Type WHERE TypeName=\'{}\' AND MSG=\'{}\'".format(type_name,
                                                                                             str(msg)))) == 0:
            return self.add_to_table("Type", [type_name, msg], [language, language_version])
        else:
            return self.execute(
                "UPDATE Type SET COUNT=COUNT + 1 WHERE TypeName=\'{}\' AND MSG=\'{}\' AND LanguageID ="
                " (SELECT LanguageID FROM Language WHERE Language=\'{}\' AND Version=\'{}\')".format(
                    str(type_name), str(msg), str(language), str(language_version)))

    def remove_row_via_ID(self, table, table_pk, table_pk_value) -> bool:
        try:
            self.key.execute("DELETE FROM " + str(table) + " WHERE " + str(table_pk) + "=" + str(table_pk_value))
            return True
        except Error:
            return False

    def get_errors(self) -> [tuple]:
        """Getting all errors from the Database - WIP"""
        return self.execute(
            "SELECT Path, Line, Error.MSG, First, Last, Error.COUNT, Type.Language, Type.TypeName FROM Error LEFT "
            "JOIN Type ON Error.TypeID=Type.TypeID")

    def get_rows_ID(self, table, table_var, table_value_min, table_value_max=False):
        ids = {'Error': "ErrorID", 'Type': "TypeID", 'Language': "LanguageID", 'Solution': "SolutionID"}
        if table_value_max in [False, True]:
            return self.get_table(table + " WHERE " + table_var + "=" + str(table_value_min), ids[table])
        else:
            return self.get_table(
                table + " WHERE " + table_var + " BETWEEN \'" + str(table_value_min) + "\' AND \'" + str(
                    table_value_max) + "\'", ids[table])

    def add_solution(self, language: str, type_name: int, priority: int, solution: str, solved: bool = False):
        if len(self.execute("SELECT * FROM Solution WHERE Solution=" + solution)) == 0:
            self.add_to_table("Solution", [priority, solution], [language, False, type_name])
        else:
            edit_sql = "UPDATE Solution SET {}={} WHERE Solution={}"
            if solved:
                self.execute(edit_sql.format("Solved", "Solved + 1", solution))
            else:
                self.execute(edit_sql.format("Unsolved", "Unsolved + 1", solution))

    def restart_all(self) -> bool:
        try:
            self.execute("DELETE FROM Error")
            self.execute("DELETE FROM Solution")
            self.execute("DELETE FROM Type")
            self.execute("DELETE FROM Language")
            return True
        except Exception as error:
            print(error)
            return False

    def get_ID(self, table: str, value1: list, value2: list):
        list1 = self.get_table(table + " WHERE " + str(value1[0]) + "=\'" + str(value1[1]) + "\'", table + "ID")
        list2 = self.get_table(table + " WHERE " + str(value2[0]) + "=\'" + str(value2[1]) + "\'", table + "ID")
        for id1 in list1:
            for id2 in list2:
                if id1[0] == id2[0]:
                    return id1[0]
        return False

    def count_increase(self, table: str, id: int):
        self.execute("UPDATE {} SET COUNT=COUNT + 1 WHERE {} = '{}'".format(table, table + "ID", str(id)))

    def add_Error(self, error: ErrorClass.Error) -> bool:
        """
        This method takes Error class and inserting it to the database
        :param error: is instance Error class  
        :return: True or False 
        """
        lang = type(error).__name__.replace("_error", "")
        list_of_error_types = self.execute(
            "SELECT Language.Language, Type.TypeName FROM Language, Type WHERE Type.LanguageID=Language.LanguageID")
        list_of_langues = self.execute("SELECT Language, Version FROM Language")
        error_list = self.execute("SELECT TypeID, Path, Line, MSG FROM Error")
        if (lang, error.error_type) in list_of_error_types:
            self.count_increase("Language", self.get_ID("Language", ["Language", lang], ["Version", False]))
            type_id = self.get_ID("Type", ["TypeName", error.error_type],
                                  ["LanguageID", self.get_ID("Language", ["Language", lang], ["Version", False])])
            self.count_increase("Type", type_id)
            if (type_id, error.path, error.line, error.error_msg) in error_list:
                self.count_increase("Error", self.get_ID("Error", ["TypeID", type_id], ["Path", error.path]))
                return True
        elif (lang, False) in list_of_langues:
            self.count_increase("Language", self.get_ID("Language", ["Language", lang], ["Version", False]))

        if not ((lang,) in self.get_table("Language", "Language")):
            for regex, language in constants.patterns.items():
                if type(language).__name__.replace("_error", "") == lang:
                    self.add_to_table("Language", [lang, regex, version])
        else:
            language = self.get_table("Language WHERE Language=\'" + lang + "\'", "COUNT")
            self.count_increase("Language", lang)
        return self.add_to_table("Error",
                                 [error.path, error.line, error.error_msg], [lang, False, error.error_type])

    def parse_table(self, template, variables) -> bool:
        i = 0
        if len(variables) < len(template):
            variables = variables + \
                        [None for _ in range(len(template) - len(variables))]
        for attribute in template:
            template[attribute] = str(variables[i])
            i += 1
        return template

    def add_to_table(self, table: str, variables: list, help_variables=False) -> bool:
        """
        the table is the name of the table to write.
        It can take values (Error, Type, Language, Solution)
        variables are a list of variables to tables.
        It can take the values listed below.
        Variables must be defined, even those that are optional.
        If you don't want to set a variable, enter it as False.
        """
        insert = "INSERT INTO {}({}) VALUES(\'{}\');"
        values = {'Error': {"Path": None, "Line": None, "MSG": None,
                            "First": None, "Last": None, "TypeID": None},
                  'Type': {"TypeName": None, "MSG": None, "LanguageID": None},
                  'Language': {"Language": None, "Regex": None, "Version": None},
                  'Solution': {"Solution": None, "Priority": None, "TypeID": None}}
        if table in values.keys():
            value = self.parse_table(values[table], variables)
            if table == "Solution":
                value["Solved"] = "0"
                value["Unsolved"] = "0"
            else:
                value["COUNT"] = "0"
        trys = 0
        while table in ["Error", "Solution", "Type"] and help_variables != False:
            lang_id = self.get_ID("Language", ["Language", help_variables[0]], ["Version", help_variables[1]])
            if lang_id == False:
                self.add_language(help_variables[0])
                if trys >= 5:
                    return False
                else:
                    trys += 1
            else:
                if table == "Type":
                    value["LanguageID"] = lang_id
                break
        trys = 0
        while table in ["Error", "Solution"] and len(help_variables) == 3:
            type_id = self.get_ID("Type", ["LanguageID", lang_id], ["TypeName", help_variables[2]])
            if type_id == False:
                self.add_type(help_variables[0], help_variables[2])
                if trys >= 5:
                    return False
                else:
                    trys += 1
            else:
                value["TypeID"] = type_id
                break
        keys = ""
        vals = "\'"
        for key in value:
            keys += str(key) + ", "
        for val in value.values():
            val2 = ""
            for i in str(val):
                if i == "\'":
                    val2 += "\'"
                val2 += i
            vals += str(val2) + "\', \'"
        try:
            sql = insert.format(table, keys[:-2], vals[:-3])
            self.key.execute(sql)
            return True
        except Error as exp:
            print(exp)
        return False
