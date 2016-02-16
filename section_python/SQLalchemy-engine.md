# Engine Configuration

`Engine` 是访问数据库的入口，`Engine`引用`Connection Pool`和 `Dialect`实现了对数据库的访问, `Dialect`指定了具体的数据库类型 `MYSQL, SQLSERVER`等, 三者关系如图所示:
![file-list](http://docs.sqlalchemy.org/en/rel_1_0/_images/sqla_engine_arch.png)

只有当调用`connect(),execute()`函数的时候，才会创建数据库的连接


# create_engine
使用 `create_engine`创建我们需要的`DB  starting point`
```
from sqlalchemy import create_engine

scheme = 'mysql+pymysql://root:123456@localhost:3306/dev_shopping?charset=utf8'
engine = create_engine(scheme, pool_size=10 , max_overflow=-1, pool_recycle=1200)
```

`create_engine` 函数常用参数：
```
pool_size=10 # 连接池的大小，0表示连接数无限制

pool_recycle=-1 # 连接池回收连接的时间，如果设置为-1，表示没有no timeout, 注意，mysql会自动断开超过8小时的连接，所以sqlalchemy沿用被mysql断开的连接会抛出MySQL has gone away

max_overflow=-1 # 连接池中允许‘溢出’的连接个数，如果设置为-1，表示连接池中可以创建任意数量的连接

pool_timeout=30 # 在连接池获取一个空闲连接等待的时间

echo=False # 如果设置True, Engine将会记录所有的日志，日志默认会输出到sys.stdout
```
创建`Engine`之后，接下来的问题，就是如何使用`Engine`

在单进程中，建议在在初始化的模块的时候创建`Engine`, 使`Engine`成为全局变量， 而不是为每个调用`Engine`的对象或者函数中创建, `Engine`不同于`connect`, `connect`函数会创建数据库连接的资源，`Engine`是管理`connect`创建的连接资源

在多进程中，为每个子进程都创建各自的`Engine`, 因为进程之间是不能共享`Engine`

# connect
使用`connect` 创建连接数据库资源, 如上所说，即使创建了`Engine`, 还是没有创建对数据库的连接，调用`connect`才会创建真正的连接
```
connection = engine.connect()
result = connection.execute("select * from tmp")
print type(result) # <class 'sqlalchemy.engine.result.ResultProxy'>
for row in result:
    print "target_name:", row['target_name']
connection.close()
```
这里有两个问题需要搞清楚，`result`返回对象类型和对象提供的方法，第二个是`close`函数调用之后，发生了什么事情，先说`close`

# close
当调用`connection.close()`之后，由`connect`函数创建的连接会被释放到连接池中, 可以供下次使用.

上面这段代码可以简写为:
```
result = engine.execute("select username from users")
for row in result:
    print "username:", row['username']
```
`execute`函数会创建自己的连接，并执行声明的sql语句，返回`ResultProxy`对象，在这个情况下，`ResultProxy`会有个标记`close_with_result`， 如果`ResultProxy`的值被全部取出来，`Engine`会自动`close`本次连接，并把连接释放到连接池里面去

如果`ResultProxy`里面还有数据没有取出来(rows remaining)，可使用`result.close()`释放本次连接，如果没有使用`result.close()`释放连接，`python garbage collection` 最终为释放本次连接到连接池中

# ResultProxy
现在来看一下`execute()`执行之后返回的结果类型 [详细文档](http://docs.sqlalchemy.org/en/rel_1_0/core/connections.html#sqlalchemy.engine.ResultProxy)。

常用的API如下：
```
fetchone() 取出一行， 当所有的行被取出来之后 connect resource会被释放到连接池中，再次调用fetchone()将返回None

result = connection.execute("select * from tmp")

row = result.fetchone()
print row[0] # access via integer position
print row['id'] # access via name
print type(row) # <class 'sqlalchemy.engine.result.RowProxy'>

# 类似还有
first()  获取第一行，同时无条件的释放连接
scalar() 获取第一行第一列的数据，同时无条件的释放连接
rowcount 获取row count
lastrowid 使用insert()方法的时候，获取最后一行的id
```

到目前为止，我们学会了如何去创建`Egnine`并使用`Engine`执行简单的sql语句，现在还有两个问题

一，我们还没有涉及到的是如何使用`sqlalchemy`提供的API去构建`insert, update, delete, create table`等相应的SQL

二，当我们使用`insert, update`等sql的时候`sqlalchemy`是否使用到事物，如何使用事物。

先从第二个问题说起
# Using Transactions
```
This section describes how to use transactions when working directly with Engine and Connection objects. When using the SQLAlchemy ORM, the public API for transaction control is via the Session object, which makes usage of the Transaction object internally. See Managing Transactions for further information
```

`Connection`对象提供了一个`begin()`函数返回` Transaction`对象
```
connection = engine.connect()
trans = connection.begin()
try:
    r1 = connection.execute(table1.select())
    connection.execute(table1.insert(), col1=7, col2='this is some data')
    trans.commit()
except:
    trans.rollback()
    raise
```
上面代码可以简写为:
```
with engine.begin() as connection:
    r1 = connection.execute(table1.select())
    connection.execute(table1.insert(), col1=7, col2='this is some data')
```
在一次连接中，两个函数同时开启了事物
```
# method_a starts a transaction and calls method_b
def method_a(connection):
    trans = connection.begin() # open a transaction
    try:
        method_b(connection)
        trans.commit()  # transaction is committed here
    except:
        trans.rollback() # this rolls back the transaction unconditionally
        raise

# method_b also starts a transaction
def method_b(connection):
    trans = connection.begin() # open a transaction - this runs in the context of method_a's transaction
    try:
        connection.execute("insert into mytable values ('bat', 'lala')")
        connection.execute(mytable.insert(), col1='bat', col2='lala')
        trans.commit()  # transaction is not committed yet
    except:
        trans.rollback() # this rolls back the transaction unconditionally
        raise

# open a Connection and call method_a
conn = engine.connect()
method_a(conn)
conn.close()
```
当调用`method_a()`函数时开启事物，然后在调用`methon_b`, `method_b`也会开启事物，这时候会有一个计算器，记录开启事物的个数，当调用用`commit()`函数之后，计数器为减1，不管是`method_a or method_b`调用了`rollback()`, 整个事物都会回滚。只有当`method_a`调用了`commit()`之后，整个事物才算结束

# Understanding Autocommit
在使用`INSERT, UPDATE or DELETE`, 如果没有声明` Transaction`,即如果没有开启事物 并且`autocommit=True`, `SQLAlchemy`会自动`commit()`执行SQL语句 如果没有设置这个参数，`SQLAlchemy`会根据正则表达式匹配出SQL语句里面的`INSERT, UPDATE or DELETE` 自动提交

```
result = connection.execution_options(autocommit=True).\
                    execute(stmt)
```

值得注意的是:
`TAhe ORM, as the Session object by default always maintains an ongoing Transaction.`


# SQL Expression Language Tutorial

[详细教程](http://docs.sqlalchemy.org/en/rel_1_0/core/tutorial.html)

使用SQL的基础是创建`Table`
### Define and Create Tables
```
>>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
>>> metadata = MetaData()
>>> users = Table('users', metadata,
...     Column('id', Integer, primary_key=True),
...     Column('name', String),
...     Column('fullname', String),
... )

# users 即为返回的table类型，下面的insert, update等语句都需要使用到users
```
### INSERT
```
ins = users.insert().values(name='jack', fullname='Jack Jones')
ins.compile().params # 获取插入的参数
result = conn.execute(ins) # 执行SQL
```
一次插入多个值
```
>>> conn.execute(addresses.insert(), [
...    {'user_id': 1, 'email_address' : 'jack@yahoo.com'},
...    {'user_id': 1, 'email_address' : 'jack@msn.com'},
...    {'user_id': 2, 'email_address' : 'www@www.org'},
...    {'user_id': 2, 'email_address' : 'wendy@aol.com'},
... ])

还有select等其他SQL可查看文档
```
以上接下来，我们需要了解ORM的知识点


