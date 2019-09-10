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


    def execute(self, sql):
        self.conn.execute(sql)

    def add_Error(self, error: ErrorClass.Error) -> bool:
        """
        This method takes Error class and inserting it to the database
        :param error: is instance Error class  
        :return: True or False 
        """
        lang = type(error).__name__
        if not (lang in self.get_table("Language", "Language")):
            for regex, language in constants.patterns:
                if type(language).__name__ == lang:
                    self.add_to_table("Language", [lang, regex])

        return self.add_to_table("Error", [lang, error.error_type, error.path, error.line,
                                           error.error_msg, False, False])

    def add_to_table(self, table, variables=[]) -> bool:
        """
        the table is the name of the table to write. It can take values (Errors, Type, Language, Solution)
        variables are a list of variables to tables. It can take the values listed below.
        Variables must be defined, even those that are optional.
        If you don't want to set a variable, enter it as False.
        """ 
        tables={'Errors':['SELECT TypeID FROM Type WHERE TypeName=\"'+str(variables[1])+'\" AND Language=\"'+str(variables[0])+'\"',
                         'INSERT INTO Errors('],
                'Type':['INSERT INTO Type('],
                'Language':['INSERT INTO Language('],
                'Solution':['SELECT TypeID FROM Type WHERE TypeName=\"'+str(variables[1])+'\" AND Language=\"'+str(variables[0])+'\"',
                            'INSERT INTO Solution(']}
        values={'Errors':["Path", "Line", "MSG", "First", "Last", "TypeID"],
                'Type':["Language", "TypeName", "MSG"],
                'Language':["Language", "Regex"],
                'Solution':["Priority", "Soulution", "TypeID"]}
        if table in values:
            for query in tables[str(table)]:
                if query[0:6]=="SELECT":
                    try:
                        self.key.execute(query)
                        id=self.key.fetchall()[0]
                        variables.append(id[1:-2])
                    except:
                        self.key.execute("SELECT Language FROM Language")
                        if variables[0] not in self.key.fetchall():
                            regex=input("add regex to language "+str(variables[0]+":"))
                            regex2=""
                            for i in regex:
                                if i == "\"":
                                    regex2+="\"\""
                                else:
                                    regex2+=i
                            self.add_to_table("Language",[variables[0],regex2])
                        self.add_to_table("Type",[variables[0],variables[1],False])
                        self.key.execute(query)
                        id=self.key.fetchall()[0]
                        variables.append(id[1:-2])
                elif query[0:6]=="INSERT" and table in ["Errors","Solution"]:
                    for i in range(len(values[table])):
                        if variables[i+2]!=False:
                            query+=values[table][i]+","
                    if table=="Errors":
                        query+="ErrorID,COUNT) VALUES(\""
                    else:
                        query+="SolutionID,COUNT) VALUES(\""
                    for i in range(len(values[table])):
                        if variables[i+2]!=False:
                            query+=str(variables[i+2])+"\",\""
                    if table=="Errors":
                        id=self.key.execute("SELECT max(ErrorID) FROM Errors").fetchall()[0]
                        if id is not int:
                            query=query[:-1]+"0"
                        else:
                            query=query[:-1]+str(int(id)+1)
                        query+=",0)"
                    else:
                        id=self.key.execute("SELECT max(SoulutionID) FROM Solution").fetchall()[0]
                        if id is not int:
                            query=query[:-1]+"0"
                        else:
                            query=query[:-1]+str(int(id)+1)
                        query+=",0)"
                    try:
                        self.conn.execute(query)
                        return True
                    except:
                        return False
                elif query[0:6]=="INSERT" and table in ['Type','Language']:
                    for i in range(len(values[table])):
                        if variables[i]!=False:
                            query+=values[table][i]+","
                    if table=="Type":
                        query+="TypeID,COUNT) VALUES(\""
                    else:
                        query+="COUNT) VALUES(\""
                    for i in range(len(values[table])):
                        if variables[i]!=False:
                            query+=str(variables[i])+"\",\""
                    if table=="Type":
                        id=self.key.execute("SELECT max(TypeID) FROM Type").fetchall()[0]
                        if id is not int:
                            query=query[:-1]+"0"
                        else:
                            query=query[:-1]+str(int(id)+1)
                        query+=",0)"
                    else:
                        query=query[:-1]+"0)"
                    try:
                        self.conn.execute(query)
                        return True
                    except:
                        return False
        else:
            return False
        return False
some=Sql_database()
some.add_to_table("Errors",["Python","TypeError","some.py",5,False,False,False])
