from sqlite3 import *
try:
    open("memory.db")
except:
    open("memory.db","a")
conn=connect("memory.db")
conn.isolation_level=None
key=conn.cursor()
try:
    SQL_create_query=open("../tests/SQL/SQL_Create_Database_Query.txt")
    sql_query=SQL_create_query.read().split("\n")
    for i in sql_query:
        print(i)
        conn.execute(i)
except:
    print("Database already exists")

def add_language(language,regex):
    global conn
    conn.execute("INSERT INTO Language (COUNT, Language, Regex) VALUES(0,"+str(language)+","+str(regex)+");")