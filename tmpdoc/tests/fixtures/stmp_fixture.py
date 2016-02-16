# -*- coding: utf-8 -*-


import pytest


@pytest.fixture
# 当scope=moudle 在这个模块里面多次调用smtp fixture，都调用的是同一个对象
# 可以观察到，smtp = <smtplib.SMTP instance at 0x10aaf0050>的值没有变化
# 当scope=function 每个函数都会生成一个新的smtp
# 当scope=session the returned fixture value will be shared for all tests needing it  # noqa
def test_fixture():
    print 'call fixture from anthor dict'
