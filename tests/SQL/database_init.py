from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Language(Base):
    __tablename__ = "Language"
    id = Column(Integer, primary_key=True, nullable=False)
    language = Column(String(250), nullable=False)
    regex = Column(String(250), nullable=False)
    version = Column(String(250))
    count = Column(Integer, nullable=False)

class Type(Base):
    __tablename__ = "Type"
    id = Column(Integer, primary_key=True, nullable=False)
    language_id = Column(Integer, ForeignKey("Language.id"), nullable=False)
    language = relationship(Language)
    type_name = Column(String(250), nullable=False)
    msg = Column(String(250))
    count = Column(Integer, nullable=False)

class Error(Base):
    __tablename__ = "Error"
    id = Column(Integer, primary_key=True, nullable=False)
    type_id = Column(Integer, ForeignKey("Type.id"), nullable=False)
    type = relationship(Type)
    path = Column(String(250))
    line = Column(Integer)
    msg = Column(String(250))
    first = Column(Integer)
    last = Column(Integer)
    count = Column(Integer, nullable=False)

class Solution(Base):
    __tablename__ = "Solution"
    id = Column(Integer, primary_key=True, nullable=False)
    type_id = Column(Integer, ForeignKey("Type.id"), nullable=False)
    type = relationship(Type)
    priority = Column(Integer, nullable=False)
    solution = Column(String, nullable=False)
    solved = Column(String, nullable=False)
    unsolved = Column(String, nullable=False)




engine = create_engine("sqlite:///snowcrash_database.db")
Base.metadata.create_all(engine)
