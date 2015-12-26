# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

DeclarativeBase = declarative_base()
DB_SETTING = "mysql+pymysql://eleme:eleme@localhost:3306/blog?charset=utf8"
engine = create_engine(DB_SETTING)
DBsession = sessionmaker(engine)
session = DBsession()


class Blog(DeclarativeBase):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), default='')
    create_at = Column(DateTime, default=0)

    def add(self):
        session.add(Blog(name="t"))


blog = Blog(name="Blog")
ins = inspect(blog)
print ins.transient
print ins.__dict__
print dir(ins)
print ins.session
print('Transient: {0}; Pending: {1}; Persistent: {2}; Detached: {3}'.format(ins.transient, ins.pending, ins.persistent, ins.detached))
#b = session.query(Blog).filter(Blog.name == "t").first()
#print b.name
