# -*- coding: utf-8 -*-
import random
import string

from sqlalchemy import create_engine
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
    price = Column(Integer, default=0)
    amount = Column(Integer, default=0)
    status = Column(Integer, default=0)
    create_at = Column(DateTime, default=0)

    def add(self, name, title, amount, price, status):
        session.add(Blog(name=name, title=title, amount=amount, price=price, status=status)) # noqa


# blog = Blog(name="Blog")
# session.add(blog)
# ins = inspect(blog)
# print ins.transient
# print ins.__dict__
# print dir(ins)
# print ins.session
# print('Transient: {0}; Pending: {1}; Persistent: {2}; Detached: {3}'.format(ins.transient, ins.pending, ins.persistent, ins.detached)) # noqa
# b = session.query(Blog).filter(Blog.name == 'test').first()
# print b
# print b.name
# b = session.query(Blog).filter(Blog.name == 'test').delete(synchronize_session='evaluate') # noqa
# session.commit()
# blog = session.query(Blog).filter(Blog.name == 'Blog').first()
# session.query(Blog).filter(Blog.name == 'Blog').update({Blog.name: Blog.name + 'x'}, synchronize_session=False) # noqa
# print blog.name
# session.commit()
# print blog.name

i = 20000
blogs = []
while i:
    chars = string.ascii_lowercase + string.digits
    name = 'name'.join(random.choice(chars) for _ in range(5))
    title = 'title'.join(random.choice(chars) for _ in range(5))
    amount = random.randint(1, 2000)
    price = random.randint(1, 1000)
    status = random.randint(0, 1)
    blogs.append(Blog(name=name, title=title, amount=amount, price=price, status=status)) # noqa
    i -= 1
session.add_all(blogs)
session.commit()
