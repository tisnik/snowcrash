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
        tables={'Errors':['SELECT TypeID FROM Type WHERE Type=='+str(variables[1])+' AND Language =='+str(variables[0]),
                         'INSERT INTO Errors'],
                'Type':['INSERT INTO Type'],
                'Language':['INSERT INTO Language'],
                'Solution':['SELECT TypeID FROM Type WHERE Type=='+str(variables[1])+' AND Language =='+str(variables[0]),
                            'INSERT INTO Solution']}
        values={'Errors':["Path", "Line", "MSG", "First", "Last", "TypeID"],
                'Type':["Language", "TypeName", "MSG"],
                'Language':["Language", "Regex"],
                'Solution':["Priority", "Soulution", "TypeID"]}
        if table in ['Errors','Type','Language','Solution']:
            for query in tables[str(table)]:
                if query[0:5]=="SELECT":
                    try:
                        self.key.execute(query)
                        variables.append(self.key.fetchall()[0])
                    except:
                        if variables[0] not in self.key.fetchall():
                            self.add_to_table("Language",[variables[0],input("add regex to language "+str(variables[0]))+":"])
                        self.add_to_table("Type",[variables[0],variables[1],False])
                        self.key.execute("SELECT Language FROM Language")
                        self.key.execute(query)
                        variables.append(self.key.fetchall()[0])
                elif query[0:5]=="INSERT" and table in ["Errors","Solution"]:
                    for i in range(len(values[table])):
                        if variables[i+2]!=False:
                            query+=values[table][i]+","
                    if table=="Errors":
                        query+="ErrorID,COUNT) VALUES("
                    else:
                        query+="SolutionID,COUNT) VALUES("
                    for i in range(len(values[table])):
                        if variables[i+2]!=False:
                            query+=str(variables[i+2])+","
                    if table=="Errors":
                        query+=str(int(self.key.execute("SELECT max(ErrorID)FROM Errors").fetchall()[0])+1)+",0)"
                    else:
                        query+=str(int(self.key.execute("SELECT max(SolutionID)FROM Solution").fetchall()[0])+1)+",0)"
                    try:
                        self.conn.execute(query)
                        return True
                    except:
                        return False
                elif query[0:5]=="INSERT" and table in ['Type','Language']:
                    for i in range(len(values[table])):
                        if variables[i]!=False:
                            query+=values[table][i]+","
                    if table=="Type":
                        query+="TypeID,COUNT) VALUES("
                    else:
                        query+="COUNT) VALUES("
                    for i in range(len(values[table])):
                        if variables[i]!=False:
                            query+=str(variables[i])+","
                    if table=="Type":
                        query+=str(int(self.key.execute("SELECT max(TypeID)FROM Type").fetchall()[0])+1)+",0)"
                    else:
                        query+="0)"
                    try:
                        self.conn.execute(query)
                        return True
                    except:
                        return False
        else:
            return False
