from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests.SQL.database_init import Type, Error, Solution, Language 
from sqlalchemy import update
from datetime import datetime
import sys
 
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
        data = self.session.query(table).filter(table.id == id).first()
        if not data:
            print("Not found record with this id: {} in table {}".format(id, table.__name__))
            sys.exit(2)
        return data

    def get_all(self, table):
        data = self.session.query(table).all()
        if not data:
            print("Not found records  in table {}".format(table.__name__))
            sys.exit(3)
        return data

    def update(self, table, column, id, data):
        table = self.get(table, id)
        try:
            table.column = data
        except AttributeError as error:
            print(error)
            sys.exit(5)
        self.session.commit()

    def delete(self, table, id):
        self.session.query(table).filter(table.id == id).delete()
        self.session.commit()

    def delete_all(self, table):
         self.session.query(table).delete()
         self.session.commit()

    def add_Language(self, *args, **kwargs):
        table = Language(**kwargs)
        return table, self.check_Language(table)

    def add_Type(self, *args, **kwargs):
        table = Type(**kwargs)
        result = self.check_Type(table)
        if not result:
            language = self.session.query(Language)\
                                    .filter(Language.language == table.language)\
                                    .first()
            if language:
                table.language_id = language.id
                table.language = language
            else:
                print("Missing row {} in table Language".format(table.language))
                sys.exit(1)

        return table, result

    def get_Type(self, table, *args):
        try:
            data =  self.session.query(Type)\
                                      .filter(self.get(Type, Type.language_id).language.language == args[0])\
                                      .filter(Type.type_name == args[1])\
                                      .first()
            return data
        except AttributeError:
            print("This type or Language does not exist")
            sys.exit(4)

    def add_Error(self, *args, **kwargs):
        table = Error(**kwargs)
        result = self.check_Error(table)
        if not result:
            type = self.get_Type(table, *args)
            table.type_id = type.id
            table.type = type
            table.first = datetime.utcnow().timestamp()
        else:
            result.last = datetime.utcnow().timestamp()
        return table, result      
                
    def add_Solution(self, *args, **kwargs):
        table = Solution(**kwargs)
        result = self.check_Solution(table)
        if not result:
            type = self.get_Type(table, *args)
            table.type_id = type.id
            table.type = type
            table.solved = 0
            table.unsolved = 0
        return table, result

    def add(self, name, *args, **kwargs):
        if name == "Language":
            table, result = self.add_Language(*args, **kwargs)            
        elif name == "Type":
            table, result = self.add_Type(*args, **kwargs)
        elif name == "Error":
            table, result = self.add_Error(*args, **kwargs)
        elif name == "Solution":
            table, result = self.add_Solution(*args, **kwargs)

        if not result:
            if name != "Solution":
                table.count = 0
            tmp = table
        else:
            if name != "Language":
                tmp = result
        
        if name == "Type":
            self.get(Language, tmp.language_id).count += 1
        elif name != "Language":
            type = self.get(Type, tmp.type_id)
            type.count += 1
            self.get(Language, type.language_id).count += 1
        
        if result:
            if name != "Solution":
                result.count += 1
        else:
            self.session.add(table)
        self.session.commit()
        return True
