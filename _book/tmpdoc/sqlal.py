# -*- coding: utf-8 -*-
import random
import string

from sqlalchemy import create_engine
from sqlalchemy import inspect, func
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
    title = Column(String(128), default='')
    create_at = Column(DateTime, default=0)

    def add(self, name, title):
        session.add(Blog(name=name, title=title))


# blog = Blog(name="Blog")
# session.add(blog)
# ins = inspect(blog)
# print ins.transient
# print ins.__dict__
# print dir(ins)
# print ins.session
# print('Transient: {0}; Pending: {1}; Persistent: {2}; Detached: {3}'.format(ins.transient, ins.pending, ins.persistent, ins.detached))
# b = session.query(Blog).filter(Blog.name == 'test').first()
# print b
# print b.name
# b = session.query(Blog).filter(Blog.name == 'test').delete(synchronize_session='evaluate')
# session.commit()
blog = session.query(Blog).filter(Blog.name == 'Blog').first()
session.query(Blog).filter(Blog.name == 'Blog').update({Blog.name: Blog.name + 'x'}, synchronize_session=False)
print blog.name
session.commit()
print blog.name

# i = 200000
# blogs = []
# while i:
#     chars = string.ascii_uppercase + string.digits
#     name = 'name'.join(random.choice(chars) for _ in range(5))
#     title = 'title'.join(random.choice(chars) for _ in range(5))
#     blogs.append(Blog(name=name, title=title))
#     i -= 1
# session.add_all(blogs)
# session.commit()
