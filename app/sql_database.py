from sqlite3 import *
import os
import sys
from app import constants


class Sql_database:

    def __init__(self, db_path="memory.db"):
        self.conn = None
        self.db_path = db_path
        self.init_db()

    def init_db(self):
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

    def query(self, sql):
        return self.conn.query(sql)

    def add_to_table(table,variables=[]):
        """
table is name of table to write. It can take values (Error, Type, Language, Solution)
    
variables is list of variables to tables. It can take values listed below.
    
Table Error has: 
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
    Type - It's a Error type's name (VARCHAR NOT NULL)
    Language - It's a File Language (VARCHAR NOT NULL)
    Priority - It's a Priority to use Soulution, it's 1(First Use) to 999(Last Use) (INT NOT NULL)      
    Solution - It's a Solution of error (VARCHAR NOT NULL)
        """
        tables={'Error':['SELECT TypeID FROM Type WHERE Type=='+str(variables[1])+' and Language =='+str(variables[0]),
                         'INSERT INTO Error'],
                'Type':['INSERT INTO Type'],
                'Language':['INSERT INTO Language'],
                'Solution':['SELECT TypeID FROM Type WHERE Type=='+str(variables[1])+' and Language =='+str(variables[0]),
                            'INSERT INTO Solution']}
        if table in ['Error','Type','Language','Solution']:
        for query in tables[str(table)]:
            if query[0:5]=="SELECT":
                key.execute(query)
                get=key.fetchall()
                print(get)
    else:
        return "This table isn't Exist"
