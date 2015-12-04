# contextlib

标签（空格分隔）： python

contextlib 是一个上下文管理模块, 那什么是上下文管理，什么时候需要用到上下文管理。

我的理解就是，比如你打开文件的时候，最终你需要改变这个打开的文件资源，如果在关闭文件资源之前，你的代码发生了错误，很有可能导致文件不会被改变，所以遇到这种“资源问题”，我们需要一个上下文管理器，保证打开的资源都会被释放，这里不得不提到`with`

```python
with file('test,'r') as f:
    print f.readline()

# 代码执行完毕之后，程序会“自动”改变打开的资源
```
想文件这种资源，在使用`with`修辞，资源在引用完成之后，python会自动关闭这个资源，但是，我们自定义的一些特殊资源，就需要我们“手动去关闭”了

怎么去实现这一套“上下文管理机制”，这就需要我们知道`with`的原理了

### with

with修饰一个可执行对象，我们需要理解什么是可执行对象，在python中，常见的有函数，类，类的实例化对象，类方法，实例化对象方法等，所以with可以修饰以上几类对象

```python

class Context(object):

    def __init__(self):
        print 'execute __init__ ...'

    def __enter__(self):
        print 'execute __enter__ ...'
        return 'hello'

    def __exit__(self, *args):
        print 'execute __exit__ ...'

# with 修饰的实例化对象
with Context() as e:
    print 'execute with code'
    # e就是__entry__函数的返回值
    print e

# 必须得搞清楚这段代码的执行过程：
# outputs:
# execute __init__ ...
# execute __enter__ ...
# execute with code
# hello
# execute __exit__ ...
```
通过以上代码可以发现，调用with的时候，实际上依次执行了被with修饰的对象的`__init__`, `__entry__` `__exit__`  函数

试想一下，我们可以实现这样一个类，在`__entry__`函数中`打开资源`, 在`__exit__`函数中`关闭资源`, 然后在用类去装饰某个函数，那么我们就可以用这个类去管理函数执行的上下文了

```python
class Contextlib(object):
    def __init__(self, func):
        print 'init decoration class'
        # 生成generation
        self.gen = func()

    def __enter__(self):
        print 'excute code  before yield'
        self.gen.next()

    def __exit__(self, *agrs):
        print 'excute code after yield'
        try:
            self.gen.next()
        except (StopIteration):
            print 'done'
@Contextlib
def context_lib(*args):
    print 'outputs  before run into yield'
    yield 'yield return value'
    print 'outputs after excute yield'

# 请注意这个细节, 一个函数被类装饰之后，类型就变成一个类
print type(context_lib)
# outputs:
# <class '__main__.Contextlib'>

print type(context_lib())
# outputs:
# <type 'generator'>

# 注意context_lib被Contextlib对象装饰，返回的结果是Contextlib对象，所以会调用Contextlib的__entry__方法

# 不要使用with context_lib() as f , 因为context_lib()执行之后，返回的是一个generator,generator可没有__entry__方法，因而会报错
with context_lib as f:
    print f
# outputs:
# init decoration class
# excute code  before yield
# first called
# yield return value  "f" 就是yielf的返回值
# excute code after yield
# last called
# done

```


