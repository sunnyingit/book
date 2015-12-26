# -*- coding: utf8 -*-


def yield_func(i):
    print 'before yield'
    yield i
    print 'after yield'

a = yield_func(1)

for i in a:
    print i
# before yield
# 1
# after yield
# 调用yield_func的时候,并没有输出before yield, 而是返回了一个generator
# print type(a)
# print a.next()
# print a.next()
# Traceback (most recent call last):
#   File "yield.py", line 13, in <module>
#     print a.next()
# StopIteration
# output:
# <type 'generator'>
# before yield
# 1
# 当执行next的时候，输出了before yield 1, 没有输出after yield 说明 yield后面的代码没有执行

# 再次调用next
# print a.next()
# output
# after yield
# Traceback (most recent call last):
#   File "yield.py", line 19, in <module>
#     print a.next()
# StopIteration
# 输出了after yield，同时抛出了StopIteration异常


def create_node(i):
    yield i

nodes = tuple()
# 调用extend的时候，会执行create_node函数返回的迭代器的next()方法
nodes.update(create_node(1))
print nodes
# output:
# [1]

# while True:
#     # 调用extend的时候，会执行create_node函数返回的迭代器的next()方法
#     nodes.extend(create_node(1))
#     if len(nodes) > 5:
#         break
# print nodes
# # output:
# # [1, 1, 1, 1, 1, 1]
# #


def h():
    print 'before yield',
    m = yield 5  # Fighting!
    print m
    d = yield 12
    print d
    print 'after yield!'

c = h()
print c.next()
# 执行到第一个yield，output:
# before yield 5
# print c.send('Fighting!')  #
# 从第一个后面的代码开始执行，直到执行到第二个yeild, output
# Fighting! 执行print m, (yield 5) m 被赋予了'Fighting!'
# 12


# c.send(111)
# can't send non-None value to a just-started generator
# 需要提醒的是，第一次调用时，请使用next()语句或是send(None)，不能使用send发送一个非None的值，否则会出错的，因为没有yield语句来接收这个值。


def get_all(self):
    """Returns an iterable of all (name, value) pairs.

    If a header has multiple values, multiple pairs will be
    returned with the same name.
    """
    for name, list in self._as_list.iteritems():
        for value in list:
            yield (name, value)
