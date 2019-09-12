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
        ret_str="Language: "+str(self.get_table("Language","Language, COUNT"))
        ret_str+="\nType: "+str(self.get_table("Type","TypeName, Language, COUNT"))
        ret_str+="\nErrors: "+str(self.get_table("Errors","ErrorID, Path, Line, MSG, COUNT"))
        ret_str+="\nSolution: "+str(self.get_table("Solution","Priority, Solution"))
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

    def add_language(self, language_name: str, regex_for_language=False) -> bool:
        """
        Adding language to database
        :param language_name: Name of the language (language class without _error)
        :param regex_for_language: Optional argument, only for initial addition
        :return: True or False
        """
        if len(self.execute("SELECT Language FROM Language where Language=\'" + language_name+"\'")) == 0:
            return self.add_to_table("Language", [language_name, regex_for_language])
        else:
            return self.count_increase("Language",language_name)

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

    def remove_row_via_ID(self, table, table_pk, table_pk_value) -> bool:
        try:
            self.key.execute("DELETE FROM " + str(table) + " WHERE " + str(table_pk) + "=" + str(table_pk_value))
            return True
        except:
            return False

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

    def restart_all(self) -> bool:
        try:
            self.execute("DELETE FROM Errors")
            self.execute("DELETE FROM Solution")
            self.execute("DELETE FROM Type")
            self.execute("DELETE FROM Language")
            return True
        except Exception as error:
            print(error)
            return False
        
    def get_TypeID(self, TypeName, Language):
        list1=self.get_table("Type WHERE TypeName=\'"+str(TypeName)+"\'","TypeID")
        list2=self.get_table("Type WHERE Language=\'"+str(Language)+"\'","TypeID")
        for id1 in list1:
            for id2 in list2:
                if id1[0]==id2[0]:
                    return id1[0]
        return False

    def count_increase(self, table: str, id):
        ids = {'Errors': "ErrorID", 'Type': "TypeID", 'Language': "Language", 'Solution': "SolutionID"}
        self.execute("UPDATE {} SET COUNT=COUNT + 1 WHERE {} = '{}'".format(table, ids[table], str(id)))

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
                    self.count_increase("Type", row[0])
                    self.count_increase("Language", row[1])
                    errors_control = self.get_table("Errors", "MSG, Path, Line, COUNT, ErrorID")
                    for row in errors_control:
                        if row[0] == error.error_msg and row[1] == error.path and row[2] == error.line:
                            self.count_increase("Errors", row[4])
                            return True

        if not ((lang,) in self.get_table("Language", "Language")):
            for regex, language in constants.patterns.items():
                if (type(language).__name__).replace("_error", "") == lang:
                    self.add_to_table("Language", [lang, regex])
        else:
            language = self.get_table("Language WHERE Language=\'" + lang + "\'", "COUNT")
            self.count_increase("Language", lang)
        return self.add_to_table("Errors",
                                 [[lang, error.error_type], [error.path, error.line, error.error_msg, False, False]])

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
        if table in values.keys():
            for template in values:
                if table == "Type":
                    condition = "Language"
                    value = self.parse_table(values[condition], variables)
                    sql = select.format(condition, condition, condition,
                                        value[condition], "\'1\'", 1)

                    self.key.execute(sql)
                    response = len(self.key.fetchall())
                    if response == 0:
                        while True:
                            language_id=self.get_table("Language", "Language")
                            languages=[]
                            for list in language_id:
                                languages.append(list[0])
                            print(languages)
                            if language_id==[] or variables[0] not in languages:
                                self.add_language(variables[0])
                            else:
                                break

                if template == table:
                    if table in ["Language","Type"]:
                        value = self.parse_table(values[table], variables)
                    else:
                        value = self.parse_table(values[table], variables[1])
                    if table == "Solution":
                        value["Solved"] = "0"
                        value["Unsolved"] = "0"
                    else:
                        value["COUNT"] = "0"
                    if table in ["Errors", "Solution"]:
                        while True:
                            type_id=self.get_TypeID(variables[0][1], variables[0][0])
                            if type_id==False:
                                self.add_type(variables[0][0], variables[0][1])
                            else:
                                break
                        value["TypeID"] = type_id
                    
                    str1=["",""]
                    for diction in value:
                        val1=[str(value[diction]),""]
                        for val in val1[0]:
                            if val=="\'":
                                val1[1]+="\'"
                            val1[1]+=val
                        if str1[0]!="":
                            str1[0]+=", "+str(diction)
                            str1[1]+="\', \'"+val1[1]
                        else:
                            str1[0]+=str(diction)
                            str1[1]+=val1[1]

                    sql = insert.format(table, str1[0], str1[1])
                    try:
                        self.key.execute(sql)
                    except IntegrityError:
                        print("Language {} already in database"
                            .format(value[table]))
                    return True
        return False