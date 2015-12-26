# contextlib

标签（空格分隔）： python

contextlib 是一个上下文管理模块
那什么是上下文管理，什么时候需要用到上下文管理?

我的理解就是，比如你打开文件的时候，最终你需要改变这个打开的文件资源，如果在关闭文件资源之前，你的代码发生了错误，很有可能导致文件不会被关闭，这会导致“资源泄露”

在这种情况下，我们需要一个上下文管理器，保证无论代码是否出错，打开的'资源'最终都会被释放

所以，当你自定义了一个`资源`,那你就需要使用到`contextclib`去管理这个资源



```python
with file('test,'r') as f:
    print f.readline()

# 代码执行完毕之后，不管是在哪种情况下，程序都会“自动关闭文件
```

使用`with`修辞，资源在引用完成之后，python会自动关闭这个资源
`with` 可以自动关闭打开的资源，但是，我们自定义的一些特殊资源，怎么关闭，我们可以这样做:
```
import contextlib

@contextlib.contextmanager
def session_stack():
    if not hasattr(db_ctx, 'session_stack'):
        db_ctx.session_stack = 0
    try:
        db_ctx.session_stack += 1
        yield # 注意yield的使用
    finally:
        db_ctx.session_stack -= 1

# 使用with调用这个函数
with session_stack():
    pass
# 这个函数首先会执行`yield`之前的代码，给资源`session_stack=1`, 然后会执行`session_stack -= 1`

```
`with`修饰一个可执行对象，我们需要理解什么是可执行对象，在python中，常见的有函数，类，类的实例化对象，类方法，实例化对象方法等，所以with可以修饰以上几类对象

`with`到底做了什么事情, 请看下面：

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
下面是`python contextlib` 的源代码：
```
class GeneratorContextManager(object):
    """Helper for @contextmanager decorator."""

    def __init__(self, gen):
        self.gen = gen

    def __enter__(self):
        try:
            return self.gen.next()
        except StopIteration:
            raise RuntimeError("generator didn't yield")

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                self.gen.next()
            except StopIteration:
                return
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = type()
            try:
                self.gen.throw(type, value, traceback)
                raise RuntimeError("generator didn't stop after throw()")
            except StopIteration, exc:
                # Suppress the exception *unless* it's the same exception that
                # was passed to throw().  This prevents a StopIteration
                # raised inside the "with" statement from being suppressed
                return exc is not value
            except:
                # only re-raise if it's *not* the exception that was
                # passed to throw(), because __exit__() must not raise
                # an exception unless __exit__() itself failed.  But throw()
                # has to raise the exception to signal propagation, so this
                # fixes the impedance mismatch between the throw() protocol
                # and the __exit__() protocol.
                #
                if sys.exc_info()[1] is not value:
                    raise


def contextmanager(func):

    @wraps(func)
    def helper(*args, **kwds):
        return GeneratorContextManager(func(*args, **kwds))
    return helper
```
至此，我们搞清楚了上下文的两个关键字：`contextlib`, `with`, 也知道了什么时候该使用上下文管理

