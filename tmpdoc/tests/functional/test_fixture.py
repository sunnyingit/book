# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope='session')
def o_fixture():
    print 'other fixture'
# 当scope=moudle 在这个模块里面多次调用smtp fixture，都调用的是同一个对象
# 可以观察到，smtp = <smtplib.SMTP instance at 0x10aaf0050>的值没有变化
# 当scope=function 每个函数都会生成一个新的smtp
# 当scope=session the returned fixture value will be shared for all tests needing it  # noqa


@pytest.fixture(scope='session', params=["smtp.gmail.com", "mail.python.org"])
# 加入参数之后，通过‘request.param’去访问参数，因为加入了两个参数导致每个调用到此
# fixture都会执行两次
# fixture 可以使用其他的fixture, 注意smtp和o_fixture的scope必须保持一致
def smtp(o_fixture, request):
    # 如果使用fixture之后，需要执行finalization code, 可以通过`request.addfinalizer(func)`来实现 # noqa
    # 如果fixture的scope是`function`, 那么每次调用完fixture后，都会执行fin()
    import smtplib
    smtp = smtplib.SMTP(request.param)

    def fin():
        smtp.close()
    request.addfinalizer(fin)
    return smtp


def test_hello(smtp):
    response, msg = smtp.ehlo()
    assert response == 250


def test_noop(smtp):
    response, msg = smtp.ehlo()
    assert response == 250
