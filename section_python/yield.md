# yield的使用
标签（空格分隔）： python php

---
<!-- toc -->


### Generators
使用()即可构建出一个迭代器，可以在for 循环中被使用，和迭代列表不一样的地方在于， 生成器并没有将所有值放入内存中，而是实时地生成这些值，并且不会保存上一次迭代生成的值，因而，在迭代一个比较大的数据的时候，使用迭代器更好

```python
# 注意是(), 而非[]
 mygenerator = (x*x for x in range(3))
 for i in mygenerator:
    print(i)
# outputs:
# 0
# 1
# 4
```
### yield execute process

yield 的作用就是返回迭代器，作为迭代器，调用next()方法可以进行迭代，那yield是如何执行的？

```python
def yield_func(i):
    print 'before yield'
    yield i
    print 'after yield'

# 调用yield_func的时候, 函数里面的代码还没有执行 只是返回了一个generator,没有输出任何内容，理解这一点非常重要
a = yield_func(1)

print type(a)
# outputs:
# <type 'generator'>

# 执行yield_func的代码，直到遇到关键字yield之后，中断代码执行，返回i
a.next()
# before yield
# outputs:
# 1

# 再次调用，会执行yield之后的代码，同时会报抛出异常，如何避免这个异常， try ... except ?
a.next()
# outputs:
# after yield
# Traceback (most recent call last):
#   File "yield.py", line 13, in <module>
#     print a.next()
# StopIteration
```
对于StopIteration，我们除了使用try...except, 还有没有其他方法，试试 ?

既然`yield_func`返回的是一个生成器，那我们就可以使用`for`迭代， 可避免迭代的异常
```python
for i in a:
    print i
# outputs:
# before yield
# 1
# after yield
```

### Mutli Yield

yield 后面的值，就是每次迭代需要返回的值
```python
def city_generator():
    yield("London")
    yield("Hamburg")
    yield("Konstanz")
a = city_generator()
# 函数执行到第一个yield 中断，输出的yield的返回值“London”
a.next()
# 执行第一个yield之后的代码，直到遇到第二个yield，输出第二个yield的返回值"Hamburg"
a.next()
#执行第二个yiel......
a.next()
```
除了`for` python还有哪些函数可以触发迭代器开始迭代
```python
# nodes = []
# # 调用extend的时候，会执行create_node函数返回的迭代器的next()方法
# nodes.extend(create_node(1))
# print nodes
# # output:
# # [1]

# while True:
# 调用extend的时候，会执行create_node函数返回的迭代器的next()方法
#     nodes.extend(create_node(1))
#     if len(nodes) > 5:
#         break
# print nodes
# outputs:
# [1, 1, 1, 1, 1, 1]
```

### send method
send 函数就是给yield语句赋值，
```python
def h():
    print 'before yield',
    m = yield 5  # send 函数发送Fighting，m被赋值为Fighting
    print m # 将输出‘Fighting’
    d = yield 12
    print d
    print 'after yield!'

c = h()
print c.next()
# 执行到第一个yield，output:
# before yield
# 5  # 这是yield返回值，send并不会改变yield的返回值
c.send('Fighting!')
# 从第一个后面的代码开始执行，直到执行到第二个yeild, output
# Fighting! 执行print m, (yield 5) m 被赋予了'Fighting!'
# 12， 这里第二个yield的返回值
```

### use yield
项目中如何使用yield，使用的思路就是，中断代码执行，在yield之前打开一个资源，然后在yield之后关闭这个资源，这样可以很好地保证每次只有一个资源被打开，同时执行完成之后资源会被关闭

第二个思路，就是节约内存，不要一下子加载所有的资源

```python

# 这是tornada的例子
def get_all(self):
   """Returns an iterable of all (name, value) pairs.

    If a header has multiple values, multiple pairs will be
    returned with the same name.
    """

    for name, list in self.headers.iteritems():
        for value in list:
            # 之前我们可能自己定义一个list，然后把(name, value)extend到list中，现在只需要返回生成器，迭代get_all的返回值，就可以获取到一个list
            yield(name, value)


# 在python的上下文管理中，经常会使用到yield
@contextlib.contextmanager
def session_stack():
    if not hasattr(db_ctx, 'session_stack'):
        db_ctx.session_stack = 0

    try:
        # yield之前，创建资源 + 1
        db_ctx.session_stack += 1
        yield
    finally:
        # yield之后，销毁资源 - 1
        db_ctx.session_stack -= 1
```

对于contextlib模块不太了解，对装饰器不太了解，下一篇文章，重点分析`装饰器`，`with`，`contextlib`的知识体系

值得一提的是，php也有`yield`关键字, 使用的方法和python差不多

[在PHP中使用协程实现多任务调度](http://www.laruence.com/2015/05/28/3038.html)
