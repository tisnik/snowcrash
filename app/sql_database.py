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
        key = self.conn.cursor()
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

    def add_language(self, language, regex):
        self.execute(
            "INSERT INTO Language (COUNT, Language, Regex) VALUES(0,{},{});".format(str(language), regex))
