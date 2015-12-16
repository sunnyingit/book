# sqlalchemy session


-------
### What does the Session do?
1 session创建和管理数据库连接的会话
2 model object 通过session对象访问数据库，并把访问到的数据以 [Identity Map](http://martinfowler.com/eaaCatalog/identityMap.html)的方式，映射到Model object中

### A typical lifespan of a Session

理解：
1 session在刚被创建的时候，还没有和任何model object 绑定，可认为是无状态的
2 session 接受到query查询语句, 执行的结果或保持或者关联到session中
3 任意数量的model object被创建，并绑定到session中，session会管理这些对象
4 一旦session 里面的objects 有变化，那可是要commit/rollback提交或者放弃changs

### how to use Session
```
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# configure Session class with desired options
Session = sessionmaker()

# later, we create the engine
engine = create_engine('postgresql://...')

# associate it with our custom Session class
Session.configure(bind=engine)

# work with the session
session = Session()
```

如果需要改变关联的engine, 比如数据库是主从设计，某些时候我们需要从主数据库，我们可能需要切换不同的数据库
```
# at the module level, the global sessionmaker,
# bound to a specific Engine
Session = sessionmaker(bind=engine)

# later, some unit of code wants to create a
# Session that is bound to a specific Connection
conn = engine.connect()
session = Session(bind=conn)
```

### When do I construct a Session, when do I commit it, and when do I close it?

一般来说，session在需要访问数据库的时候创建，在session访问数据库的时候，准确来说，应该是“add/update/delete”数据库的时候，会开启`database transaction`, 假设没有修改`autocommit`的默认值(False), 那么，`database transaction` 一直会保持，只有等到session rolled back, committed, or closed的时候才结束，一般建议，当`database transaction`结束的时候，同时close session, 保证，每次发起请求，都创建一个新的session

特别是对web应用来说，发起一个请求，若请求使用到Session访问数据库，则创建session，处理完这个请求后，关闭session，如图：
```
Web Server          Web Framework        SQLAlchemy ORM Code
--------------      --------------       ------------------------------
startup        ->   Web framework        # Session registry is established
                    initializes          Session = scoped_session(sessionmaker())

incoming
web request    ->   web request     ->   # The registry is *optionally*
                    starts               # called upon explicitly to create
                                         # a Session local to the thread and/or request
                                         Session()

                                         # the Session registry can otherwise
                                         # be used at any time, creating the
                                         # request-local Session() if not present,
                                         # or returning the existing one
                                         Session.query(MyClass) # ...

                                         Session.add(some_object) # ...

                                         # if data was modified, commit the
                                         # transaction
                                         Session.commit()

                    web request ends  -> # the registry is instructed to
                                         # remove the Session
                                         Session.remove()

                    sends output      <-
outgoing web    <-
response
```

还有一点需要注意的是，保证session是一个全局的对象，所以和数据库通信的session在任何时候只有一个，为毛，因为我们只需要一个session对象，同时，管理一个session对象远比管理两个对象简单

#### 不要这么做：
```
class ThingOne(object):
    def go(self):
        session = Session()
        try:
            session.query(FooBar).update({"x": 5})
            session.commit()
        except:
            session.rollback()
            raise

class ThingTwo(object):
    def go(self):
        session = Session()
        try:
            session.query(Widget).update({"q": 18})
            session.commit()
        except:
            session.rollback()
            raise

def run_my_program():
    ThingOne().go()
    ThingTwo().go()
```

推荐这么做：
```
class ThingOne(object):
    def go(self, session):
        session.query(FooBar).update({"x": 5})

class ThingTwo(object):
    def go(self, session):
        session.query(Widget).update({"q": 18})

def run_my_program():
    session = Session()
    try:
        ThingOne().go(session)
        ThingTwo().go(session)

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
```

### Is the Session a cache
 session 没有任何缓存

### Is the session thread-safe
session 不是线程安全的，上面提到，我们需要保证session object是全局的，在多线程的环境中，默认情况下，多个线程将会共享同一个session， 试想一下，假设A线程正在使用session处理数据库，B线程已经执行完成，把session给close了，那么此时A在使用session就会报错，怎么避免这个问题

必须保证每个线程使用的session都不一样

### Thread-local Sessions
```
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

session_factory = sessionmaker(bind=some_engine)
Session = scoped_session(session_factory)
some_session = Session()
some_other_session = Session()
some_session is some_other_session #True
```
使用了`scoped_session` 默认情况下，创建的session都是`Thread-Local Scope`，创建的session对象具体有两点变化：
1 使用Session()创建的session对象都是一样的，这可以保证代码在不同的多次调用session()依然获得到相同的session 对象
2 使用Session()创建的session对象 是 `Thread-local`, session在线程与线程之间没有任何联系

sqlalchemy怎么做的，[猛击 thrending.local()](http://docs.python.org/library/threading.html#threading.local)

### how to close session
```
Session.remove()

# This will first call Session.close() method on the current Session, which releases any existing transactional/connection resources still being held; transactions specifically are rolled back. The Session is then discarded. Upon next usage within the same scope, the scoped_session will produce a new Session object

# 注意，未commit的transactions会被回滚

```
那么session.close会做什么事情呢，文章开头说道，session创建和管理对数据库的连接，当调用close的时候，注意，sqlalchemy不会关闭与mysql的连接，而是把连接返回到连接池。

### model object关联到session的状态
Session Object States

Since we have already seen an Session object in action, it's important to also know the four different states of session objects:

Transient: an instance that's not included in a session and has not been persisted to the database.
Pending: an instance that has been added to a session but not persisted to a database yet. It will be persisted to the database in the next session.commit().
Persistent: an instance that has been persisted to the database and also included in a session. You can make a model object persistent by committing it to the database or query it from the database.
Detached: an instance that has been persisted to the database but not included in any sessions.

```
>>> from sqlalchemy import inspect
>>> david = User(name='David')
>>> ins = inspect(david)
>>> print('Transient: {0}; Pending: {1}; Persistent: {2}; Detached: {3}'.format(ins.transient, ins.pending, ins.persistent, ins.detached))
Transient: True; Pending: False; Persistent: False; Detached: False
>>> s.add(david)
>>> print('Transient: {0}; Pending: {1}; Persistent: {2}; Detached: {3}'.format(ins.transient, ins.pending, ins.persistent, ins.detached))
Transient: False; Pending: True; Persistent: False; Detached: False
>>> s.commit()
>>> print('Transient: {0}; Pending: {1}; Persistent: {2}; Detached: {3}'.format(ins.transient, ins.pending, ins.persistent, ins.detached))
Transient: False; Pending: False; Persistent: True; Detached: False
>>> s.close()
>>> print('Transient: {0}; Pending: {1}; Persistent: {2}; Detached: {3}'.format(ins.transient, ins.pending, ins.persistent, ins.detached))
Transient: False; Pending: False; Persistent: False; Detached: True

```







