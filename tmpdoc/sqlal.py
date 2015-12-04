# -*- coding: utf-8 -*-
import datetime

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
DB_SETTING = "mysql+pymysql://eleme:eleme@localhost:3306/blog?charset=utf8",  # noqa
engine = create_engine(DB_SETTING)
DBsession = sessionmaker(engine)
session = DBsession()


class Blog(DeclarativeBase):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), default='')
    created_at = Column(DateTime, default=datetime.datetime.now)

session.add(Blog(name=u"测试"))

session.commit()
