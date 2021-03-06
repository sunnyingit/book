# -*- coding: utf-8 -*-

import os
import sha
import gevent
import contextlib
import functools
import random
import uuid
import time
import threading

from sqlalchemy import event
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


RAISE_CLOSING_EXCEPTION = False
db_ctx = threading.local()


def scope_func():
    if not hasattr(db_ctx, 'session_stack'):
        db_ctx.session_stack = 0
    return (threading.current_thread().ident, db_ctx.session_stack)


@contextlib.contextmanager
def session_stack():
    if not hasattr(db_ctx, 'session_stack'):
        db_ctx.session_stack = 0

    try:
        db_ctx.session_stack += 1
        yield
    finally:
        db_ctx.session_stack -= 1


class RoutingSession(Session):
    _name = None

    def __init__(self, engines, *args, **kwds):
        super(RoutingSession, self).__init__(*args, **kwds)
        self.engines = engines
        self.slave_engines = [e for role, e in engines.items()
                              if role != 'master']
        assert self.slave_engines, ValueError("DB slave configs is wrong!")
        self._id = self.gen_id()
        sql_logger.ctx.current_session_id = self._id

    def get_bind(self, mapper=None, clause=None):
        if self._name:
            return self.engines[self._name]
        elif self._flushing:
            return self.engines['master']
        else:
            return random.choice(self.slave_engines)

    def using_bind(self, name):
        self._name = name
        return self

    def rollback(self):
        with gevent.Timeout(5):
            super(RoutingSession, self).rollback()

    def close(self):
        with gevent.Timeout(5):
            super(RoutingSession, self).close()

    def gen_id(self):
        pid = os.getpid()
        tid = threading.current_thread().ident
        clock = time.time() * 1000
        address = id(self)
        hash_key = self.hash_key
        return sha.new('{0}\0{1}\0{2}\0{3}\0{4}'.format(
            pid, tid, clock, address, hash_key)).hexdigest()[:20]


def patch_engine(engine):
    pool = engine.pool
    pool._origin_recyle = pool._recycle
    del pool._recycle
    setattr(pool.__class__, '_recycle', RecycleField())
    return engine


def create_engine(*args, **kwds):
    engine = patch_engine(sqlalchemy_create_engine(*args, **kwds))
    sql_logger.register(engine)
    event.listen(engine, 'before_cursor_execute', sql_commenter, retval=True)
    return engine


def make_session(engines, force_scope=False, info=None):
    if settings.DEVELOP_MODE or force_scope:
        scopefunc = scope_func
    else:
        scopefunc = None

    session = scoped_session(
        sessionmaker(
            class_=RoutingSession,
            expire_on_commit=False,
            engines=engines,
            info=info or {"name": uuid.uuid4().hex},
        ),
        scopefunc=scopefunc
    )
    return session


def gen_commit_deco(DBSession, raise_exc, error_code):
    def decorated(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            session = DBSession()
            try:
                session.flush()
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise_exc(error_code, repr(e))
            finally:
                session.close()
            return ret
        return wrapper
    return decorated


def sql_commenter(conn, cursor, statement, params, context, executemany):
    if hasattr(g, 'call_meta_data') and 'request_id' in g.call_meta_data:
        request_id = g.call_meta_data['request_id']
        statement = "/* E:rid=%s:E */" % request_id + statement
    return statement, params


class ModelMeta(DeclarativeMeta):

    def __new__(self, name, bases, attrs):
        cls = DeclarativeMeta.__new__(self, name, bases, attrs)

        from .cache import CacheMixinBase
        for base in bases:
            if issubclass(base, CacheMixinBase) and hasattr(cls, "_hook"):
                cls._hook.add(cls)
                break
        return cls


def model_base():
    return declarative_base(metaclass=ModelMeta)


class RecycleField(object):

    def __get__(self, instance, klass):
        if instance is not None:
            return int(random.uniform(0.75, 1) * instance._origin_recyle)
        raise AttributeError


class DBManager(object):

    def __init__(self):
        self.session_map = {}

    def create_sessions(self):
        for db, db_configs in settings.DB_SETTINGS.iteritems():
            self.add_session(db, db_configs)

    def get_session(self, name):
        try:
            return self.session_map[name]
        except KeyError:
            raise KeyError(
                '`%s` session not created, check `DB_SETTINGS`' % name)

    def add_session(self, name, config):
        if name in self.session_map:
            raise ValueError("Duplicate session name {},"
                             "please check your config".format(name))
        session = self._make_session(name, config)
        self.session_map[name] = session
        return session

    @classmethod
    def _make_session(cls, db, config):
        urls = config['urls']
        pool_size = config.get('pool_size', settings.DB_POOL_SIZE)
        max_overflow = config.get(
            'max_overflow', settings.DB_MAX_OVERFLOW)
        pool_recycle = config.get(
            'pool_recycle', settings.DB_POOL_RECYCLE)
        engines = {
            role: cls.create_engine(
                dsn, pool_size=pool_size, max_overflow=max_overflow,
                pool_recycle=pool_recycle)
            for role, dsn in urls.iteritems()
        }
        return make_session(engines, info={"name": db})

    def close_sessions(self, should_close_connection=False):
        dbsessions = self.session_map
        for dbsession in dbsessions.itervalues():
            if should_close_connection:
                session = dbsession()
                for engine in session.engines.itervalues():
                    for parent in session.transaction._iterate_parents():
                        conn = parent._connections.get(engine)
                        if conn:
                            conn = conn[0]
                            conn.invalidate()
            dbsession.remove()

    @classmethod
    def create_engine(cls, *args, **kwds):
        engine = patch_engine(sqlalchemy_create_engine(*args, **kwds))
        sql_logger.register(engine)
        event.listen(engine, 'before_cursor_execute', sql_commenter,
                     retval=True)
        return engine

db_manager = DBManager()
db_manager.create_sessions()

SHOPPING_DB_SETTINGS = {
    "master": "mysql+pymysql://eleme:eleme@localhost:3306/dev_shopping?charset=utf8",  # noqa
    "slave": "mysql+pymysql://eleme:eleme@localhost:3306/dev_shopping?charset=utf8",  # noqa
    "slave2": "mysql+pymysql://eleme:eleme@localhost:3306/dev_shopping?charset=utf8",  # noqa
}

DB_SETTINGS = {
    'shopping': {
        'urls': SHOPPING_DB_SETTINGS,
        'max_overflow': -1,
        'pool_size': 10,
        'pool_recycle': 1200,
    }
}

