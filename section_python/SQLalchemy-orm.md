# Object Relational Mapping
ORM 即为用户自定义类和数据库的表的映射关系，通俗来说，一个类映射到一张表，一个类的实例(对象)对应数据库表里面的一行数据，实例的属性和数据库row的数据保持实时同步

# Declare a Mapping
`Engine`提供了数据库的入口，在ORM中，我们依然需要创建`Engine`, 要实现ORM，我们自定义类必须继承`declarative_base()`函数生成的类, 自定义类必须指定`__tablename__`和至少主键字段(primary_key)

```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
# create the base class
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
```
使用`Blog.__table__`可以查看自定义表结构, 更多的数据类型参考：
```
Integer/BigInteger/SmallInteger
整形.
Boolean
布尔类型. Python 中表现为 True/False , 数据库根据支持情况, 表现为 BOOLEAN 或 SMALLINT . 实例化时可以指定是否创建约束(默认创建).
Date/DateTime/Time (timezone=False)
日期类型, Time 和 DateTime 实例化时可以指定是否带时区信息.
Interval
时间偏差类型. 在 Python 中表现为 datetime.timedelta() , 数据库不支持此类型则存为日期.
Enum (*enums, **kw)
枚举类型, 根据数据库支持情况, SQLAlchemy 会使用原生支持或者使用 VARCHAR 类型附加约束的方式实现. 原生支持中涉及新类型创建, 细节在实例化时控制.
Float
浮点小数.
Numeric (precision=None, scale=None, decimal_return_scale=None, ...)
定点小数, Python 中表现为 Decimal .
LargeBinary (length=None)
字节数据. 根据数据库实现, 在实例化时可能需要指定大小.
PickleType
Python 对象的序列化类型.
String (length=None, collation=None, ...)
字符串类型, Python 中表现为 Unicode , 数据库表现为 VARCHAR , 通常都需要指定长度.
Unicode
类似与字符串类型, 在某些数据库实现下, 会明确表示支持非 ASCII 字符. 同时输入输出也强制是 Unicode 类型.
Text
长文本类型, Python 表现为 Unicode , 数据库表现为 TEXT .
UnicodeText
参考 Unicode
```

# Create an Instance of the Mapped Class
首先实例化类，然后把实例化对象加入到session中，最后选择`commit or rollback`, 需要注意的是，使用`session.add()`会自动开启一个事物，在未调用`commit()`之前，Blog Instance的状态为`Pending`, 也就是说，没有任何SQL语句发送到数据库，此时数据库里面没有`name=Blog`这条记录，如果其他操作查询`Blog.name=Blog`将没有任何数据
```
blog = Blog(name="Blog")
session.add(blog)

print blog.name
Blog
# 特别注意，此时id的值为None
print blog.id
None

# 一次添加多个object
session.add_all([Blog(name="blog"), Blog(name="new_blog")])
```

那么什么时候，Blog Instance的数据会被发送到数据库中呢，答案是调用`flush`操作之后
```
blog = Blog(name="Blog")
session.add(blog)
# add之后，加入了flush操作
session.flush()
# 此时可以输出id的值， 不再是None，说明blog的数据已经发送到了mysql，并且还更新了session中blog的id属性值
print blog.id
1
```

除了`flush`操作，还可以通过`query`去`flush`数据到数据库中，文档中有一句话
```If we query the database for Ed Jones, all pending information will first be flushed, and the query is issued immediately thereafter， , the query will return results both from the database and from the flushed parts of the uncommitted transaction it holds. By default, Session objects autoflush their operations, but this can be disabled```

需要注意的是 `session.autoflush = False`之后，`session.query`不会发送sql到数据库, 但默认开启了`autoflush`
```
blog = Blog(name="Blog")
session.add(blog)
session.query(Blog).filter(Blog.name == 'Blog').first()

# query之后，处于pending状态被发送到数据库
print blog.id
1
```
# commit
此时查看数据库，数据库依然没有任何数据，也就是说数据库还么有把数据写入到磁盘中，通过`commit()`可实现写入磁盘，持久化数据, 需要理解的时候，当执行`session.commit()`之后，被`session`引用的`connection resources`会被返回到`connection pool`中， 同时commit之后，session会过期
```
blog = Blog(name="Blog")
session.add(blog)
session.commit()
```
此时其他session可通过`Blog.name=Blog`查询该数据，那有一个问题，如果数据被`flush`到数据库但没有`commit()`，其他session会该记录吗，答案是取决与数据库的隔离级别，如果数据库的隔离级别是`Read uncommitted`，允许脏读，也就是可能读取到其他会话中未提交事务修改的数据, 即可获取到改记录

session就是一个容器，把对象加入到session中后，依然可以修改对象的值
```
blog = Blog(name='Blog')
session.add(blog)
print blog in session
True
# 在commit之前，修改了blog.name的值
blog.name = ‘new_blog’
session.commmit()
# 最后提交到数据库的数据是`new_blog`
```

# Rolling Back
回滚`session.add()`操作，`blog`被提出了`session`, 也就是`session`不再管理`blog`了。
```
blog = Blog(name="Blog")
session.add(blog)
session.rollback()
print blog in session
False
```

# Querying
使用`query`函数可以创建`query object` [详细文档](http://docs.sqlalchemy.org/en/latest/orm/query.html), 这个对象提供了一系列方法丰富查询条件, 下面的例子，`session.query()`返回是一个迭代器，使用`for`可以获取到查询的所有结果，使用迭代器去优化查询结果
```
>>> for instance in session.query(User).order_by(User.id):
...     print(instance.name, instance.fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone
```

查询指定的列
```
for name, fullname in session.query(User.name, User.fullname):
...     print(name, fullname)
```

The tuples returned by Query are named tuples, supplied by the KeyedTuple class, and can be treated much like an ordinary Python object. The names are the same as the attribute’s name for an attribute, and the class name for a class

```
 for row in session.query(User, User.name).all():
    print(row.User, row.name)
```

常用的还有
```
query.filter(User.name == 'ed')
query.filter(User.name != 'ed')
query.filter(User.name.like('%ed%'))
query.filter(User.name.in_(['ed', 'wendy', 'jack']))
query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
query.filter(User.name == None) or query.filter(User.name != None)
query.filter(User.name.is_(None))

# and
from sqlalchemy import and_
query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
query.filter(User.name == 'ed', User.fullname == 'Ed Jones')
query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
session.query(Blog).filter(Blog.create >= 0 | Blog.title == 'A').first()


# or
from sqlalchemy import or_
query.filter(or_(User.name == 'ed', User.name == 'wendy'))
session.query(Blog).filter(Blog.create >= 0 & Blog.title == 'A').first()

# 直接使用查询结果
session.query(Blog.id, Blog.title).filter(Blog.create >= 0).first().title

# 基于主键查询
session.query(User).get(1)
some_object = session.query(VersionedFoo).get((5, 10))

```
# Using Textual SQL
```
>>> from sqlalchemy import text
>>> for user in session.query(User).\
...             filter(text("id<224")).\
...             order_by(text("id")).all():
...     print(user.name)
```

# Returning Lists and Scalars
是时候关心查询结果的返回值了，前面我们提到过返回一个迭代器
```
# all() returns a list
>>> query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
SQL>>> query.all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>,
      <User(name='fred', fullname='Fred Flinstone', password='blah')>]

first() applies a limit of one and returns the first result as a scalar, 如果查询数据为空，则返回None
>>> query.first()
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>

one() 在返回的rows中获取到一行，需要注意的是，no row found or Multiple rows were found  都会抛出异常，这是和first()不同的地方

scalar() invokes the one() method, and upon success returns the first column of the row:
>>> query = session.query(User.id).filter(User.name == 'ed'). order_by(User.id)
>>> query.scalar()
1
```

# Counting
```
>>> from sqlalchemy import func
>>> session.query(func.count(User.name), User.name).group_by(User.name).all()
[(1, u'ed'), (1, u'fred'), (1, u'mary'), (1, u'wendy')]

>>> session.query(User).filter(User.name.like('%ed')).count()
2
```

# Deleting
```
blog = session.query(Blog).filter(Blog.name == 'Blog').first()
session.delete(blog)
# 提交之后，即可删除blog数据
session.commit()
```

`query`之后可以直接删除
```
session.query(RegionActivity).\
        filter(RegionActivity.activity_id == act.id).\
        delete(synchronize_session=False)
# False - don’t synchronize the session. This option is the most efficient and is reliable once the session is expired, which typically occurs after a commit(), or explicitly using expire_all(). Before the expiration, objects may still remain in the session which were in fact deleted which can lead to confusing results if they are accessed via get() or already loaded collections
```

# updating
和delete一样，还是有两种操作
```
session.query(User).filter(User.username == 'abc').update({'name': '123'})
session.commit()

user = session.query(User).filter_by(username='abc').scalar()
user.name = '223'
session.commit()
```

试试这个操作
```
session.query(Blog).filter(Blog.name == 'Blog').update({Blog.name: Blog.name + 'x'})

# InvalidRequestError: Could not evaluate current criteria in Python Specify 'fetch' or False for the synchronize_session parameter
```
默认情况下，`update`操作会修改`session`的操作，但是需要引用到`blog.name`的时候就会报错，保险的做法是
```
# 修改数据的时候，并不修改session里面的数据
session.query(Blog).filter(Blog.name == 'Blog').update({Blog.name: Blog.name + 'x'}, synchronize_session=False)
```
需要注意的是，`session.commit`之后，session就过期了，再次获取相关属性值的时候，会通过id去数据库查询对应的值，如果把id修改了，那就会出事了
```
blog = session.query(Blog).filter(Blog.name == 'Blog').first()
session.query(Blog).filter(Blog.name == 'Blog').update({Blog.name: Blog.name + 'x'}, synchronize_session=False)
print blog.name # 'Blog' 并没有修改session里面的值
session.commit()
print blog.name # 'Blogx' 获取的是最新的值，说明是从数据库重新获取的新的值
```

以上总结orm 基本的使用情况 [API文档](http://docs.sqlalchemy.org/en/latest/orm/query.html)，现在最后一个需要搞清楚的问题是session的生命周期以及在实际的情况下，如何去架构session, engine的初始化代码

