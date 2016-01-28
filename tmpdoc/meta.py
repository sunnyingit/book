# -*- conding: utf-8 -*-
from sqlalchemy import *


scheme = 'mysql+pymysql://root:123456@localhost:3306/dev_shopping?charset=utf8'  # noqa
engine = create_engine(scheme, pool_size=10)
conn = engine.connect()

metadata = MetaData()
metadata.bind = engine

user = Table('user', metadata,
             Column('user_id', Integer, primary_key=True),
             Column('user_name', String(16), nullable=False),
             Column('email_address', String(60)),
             Column('password', String(20), nullable=False)
             )

# metadata.create_all(engine)
ins = user.insert().values({"user_id": 1, "user_name": "sunli",
                            "email_address": "xxxx@qq.com", "password": "123456"})  # noqa

ups = user.update().\
    where(user.c.user_id == 1).\
    values('user_name' == 'lili')


id, name = Column("user_id"), Column("user_name")
stmt = select([id, name]).where(user.c.user_id == 1)

engine.execute(stmt)

import pdb
pdb.set_trace()
