from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests.SQL.database_init import Type, Error, Solution, Language 
from sqlalchemy import update
from time import time
 
class Database:

    def __init__(self):
        self.engine = create_engine('sqlite:///snowcrash_database.db')
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def check_Language(self, table):
        return self.session.query(table.__class__)\
                                     .filter(table.__class__.language == table.language)\
                                     .filter(table.__class__.regex == table.regex)\
                                     .filter(table.__class__.version == table.version)\
                                     .first()

    def check_Error(self, table):
        return self.session.query(table.__class__)\
                                       .filter(table.__class__.path == table.path)\
                                       .filter(table.__class__.msg == table.msg)\
                                       .filter(table.__class__.line == table.line)\
                                       .first()

       
        
    def check_Type(self, table):
        return self.session.query(table.__class__)\
                                       .filter(table.__class__.msg == table.msg)\
                                       .filter(table.__class__.type_name == table.type_name)\
                                       .first()
    
    def check_Solution(self, table):
        return self.session.query(table.__class__)\
                                       .filter(table.__class__.priority == table.priority)\
                                       .filter(table.__class__.solution == table.solution)\
                                       .first()

    def get(self, table, id):
        return self.session.query(table).filter(table.id == id).first()

    def get_all(self, table):
        return self.session.query(table).all()

    def delete(self, table, id):
        self.session.query(table).filter(table.id == id).delete()
        self.session.commit()

    def delete_all(self, table):
         self.session.query(table).delete()
         self.session.commit()

    def add(self, name, *args, **kwargs):
        if name == "Language":
            table = Language(**kwargs)
            result = self.check_Language(table)
        if name == "Type":
            table = Type(**kwargs)
            result = self.check_Type(table)
            if not result:
                language = self.session.query(Language)\
                                      .filter(Language.language == table.language)\
                                      .first()
                table.language_id = language.id
                table.language = language
        
        if name in ["Error", "Solution"]:
            if name == "Error":
                table = Error(**kwargs)
                result = self.check_Error(table)
            if name == "Solution":
                table = Solution(**kwargs)
                result = self.check_Solution(table)
            if not result:
                print(args)
                type = self.session.query(Type)\
                                      .filter(self.get(Type, Type.language_id).language.language == args[0])\
                                      .filter(Type.type_name == args[1])\
                                      .first()
                print(type)
                print(type.id)
                table.type_id = type.id
                table.type = type
        if name == "Error":
            if not result:
                table.first = time()
            else:
                result.last = time()
        if name == "Solution" and not result:
            table.solved = 0
            table.unsolved = 0
        if not result and table != "Solution":
            table.count = 0
    
        if result:
            if table.__class__.__name__ != "Solution":
                result.count += 1
            else:
                return False
        else:
            self.session.add(table)
        self.session.commit()
        return True
        
        



        