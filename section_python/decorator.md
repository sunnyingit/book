# python 装饰器

[原文链接](http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python/1594484#1594484)


-------------------

<!-- toc -->

### function is object
在python中，函数是一个对象，所以函数可以赋值给变量
```python

def shout(word="yes"):
    return word.capitalize() + "!"

print shout()
# outputs : 'Yes!'

# 通过函数名赋值给变量
scream = shout
print scream()
# outputs: 'Yes!'

# 删除shout之后，依然可以执行scream
del shout
try:
    print shout()
except NameError, e:
    print e
    #outputs: "name 'shout' is not defined"

print scream()
# outputs: 'Yes!'

# 作为函数的参数
def shout_yes(scream):
    scream()

shout_yes(scream)
# outputs: 'Yes!'

```
### 函数引用
>函数是对象，意味着函数可以想任何其他变量一下，**[赋值给其他变量]**，**[删除]**，**[修改]**，**[作为函数的参数]**，**[作为函数的返回值]**

```python
def getTalk(type="shout"):

    # 定义函数, 和定义其他任何对象一样
    def shout(word="yes"):
        return word.capitalize()+"!"

    def whisper(word="yes") :
        return word.lower()+"...";

    # 返回函数，和返回其他任何对象一样
    if type == "shout":
        # 没有使用"()", 并不是要调用函数，而是要返回函数对象
        return shout
    else:
        return whisper


# 将函数返回值赋值给一个变量
talk = getTalk()

# 我们可以打印下这个函数对象
print talk
#outputs : <function shout at 0xb7ea817c>

# 这个对象是函数的返回值
print talk()
#outputs : Yes!

# 直接执行函数的返回值
print getTalk("whisper")()
#outputs : yes...

# 如果你想重新给函数赋值， 也是没有问题的
talk = int
talk(2.1)
# outputs: 2
```


### 自己写一个装饰器
> 函数装饰器的本质就是"装饰"函数，在不改动函数的情况下，给被装饰的函数加上其他功能

```python
# 参数就是需要被装饰的函数
def my_shiny_new_decorator(a_function_to_decorate):

    # 对原始函数进行包装
    def the_wrapper_around_the_original_function():

        # 将你要在原始函数之前执行的代码放到这里
        print "Before the function runs"

        # 调用原始函数(需要带括号)
        a_function_to_decorate()

        # 将你要在原始函数之后执行的代码放到这里
        print "After the function runs"

    # 代码到这里，函数‘a_function_to_decorate’还没有被执行
    # 我们将返回刚才创建的这个包装函数
    # 这个函数包含原始函数及要执行的附加代码，并且可以被使用
    return the_wrapper_around_the_original_function

# 创建一个函数
def a_stand_alone_function():
    print "I am a stand alone function, don't you dare modify me"

a_stand_alone_function()
#outputs: I am a stand alone function, don't you dare modify me

# 好了，在这里你可以装饰这个函数，扩展其行为
# 将函数传递给装饰器，装饰器将动态地将其包装在任何你想执行的代码中，然后返回一个新的函数
a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)

# 调用新函数，可以看到装饰器的效果
a_stand_alone_function_decorated()
#outputs:
#Before the function runs
#I am a stand alone function, don't you dare modify me
#After the function runs

```
### 装饰器阐述

之前的例子，是我们手动执行 `a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)`

如果使用pthon的语法，那应该像这样， 使用`@`
```python
@my_shiny_new_decorator
def another_stand_alone_function():
    print "Leave me alone"

another_stand_alone_function()
#outputs:
#Before the function runs
#Leave me alone
#After the function runs
```

所以， 以下两个效果是等价的：
`nother_stand_alone_function = my_shiny_new_decorator(another_stand_alone_function) = @my_shiny_new_decorator
`
如果有多个装饰器
```python
@bread
@ingredients
def sandwich(food="--ham--"):
    print food

# 等价于：
bread(ingredients(sandwich))

# 装饰器位置的顺序很重要，先执行bread函数，bread调用ingredients, ingredients又会调用sandwich
```
### 装饰"对象方法"的装饰器
Python中对象的方法和函数是一样的，**除了对象的方法首个参数是指向当前对象的引用(self)**。这意味着你可以用同样的方法构建一个装饰器，只是必须考虑self
```python
def method_friendly_decorator(method_to_decorate):
    # wrapper是被返回的函数变量，最终需要在class中执行，由于class的方法的第一个参数必须是self，所以wrapper的第一个参数必须也是self
    def wrapper(self, lie):
        lie = lie - 3 # very friendly, decrease age even more :-)
        # method_to_decorate的第一个参数也必须是self
        return method_to_decorate(self, lie)
    return wrapper

class Lucy(object):

    def __init__(self):
        self.age = 32

    @method_friendly_decorator
    def sayYourAge(self, lie):
        print "I am %s, what did you think?" % (self.age + lie)

l = Lucy()
l.sayYourAge(-3)
#outputs: I am 26, what did you think?

```


### 向装饰器函数传递参数
在上面的一个例子中，我们可以看到，给装饰器传递了两个参数，`self`, `lie`, 我们在给装饰器函数传递参数，实际上，是给**`wrapper`**传递参数，因为我们的最终的函数实际上变成了装饰器返回的**`wrapper`**

你可以构造一个更加通用的装饰器，可以作用在任何函数或对象方法上，而不必关系其参数使用， 使用：

`*args, **kwargs`

如果对着两个变量不熟悉，[猛击](http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/)

```python
def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    # 包装函数可以接受任何参数
       def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):

        # 通过 a_wrapper_accepting_arbitrary_arguments 传递过来的参数，因为闭包的关系，可以被function_to_decorate访问到
        function_to_decorate(*args, **kwargs)
    return a_wrapper_accepting_arbitrary_arguments

```

### 向装饰器传递参数
我们可以想装饰器函数传递任意的参数了，那我们是否可以像装饰器传递参数的，比如我们想根据不同的参数返回不同的`wrapper`函数

但是，装饰器必须使用函数作为参数，你不能直接传递参数给装饰器本身
那我们需要做的就是，在装饰器外面在包一层
```python
# 声明一个用于创建装饰器的函数
def decorator_maker():

    print "I make decorators! I am executed only once: "+\
          "when you make me create a decorator."

    def my_decorator(func):
        print "I am a decorator! I am executed only when you decorate a function."

        def wrapped():
            print ("I am the wrapper around the decorated function. "
                  "I am called when you call the decorated function. "
                  "As the wrapper, I return the RESULT of the decorated function.")
            return func()

        print "As the decorator, I return the wrapped function."
        return wrapped

    print "As a decorator maker, I return a decorator"
    return my_decorator

# Let's create a decorator. It's just a new function after all.
# 创建一个装饰器，本质上只是一个函数
new_decorator = decorator_maker()
#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator

# 使用装饰器装饰函数

def decorated_function():
    print "I am the decorated function."

decorated_function = new_decorator(decorated_function)
#outputs:
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function

# 调用被装饰函数
decorated_function()
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.

```

我们跳过中间变量，做同样的事情
```python
def decorated_function():
    print "I am the decorated function."
# 先执行一个docorator_maker()函数，返回一个docorator
decorated_function = decorator_maker()(decorated_function)

#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

# 最后:
decorated_function()
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
```
使用装饰器语法，更简短
```python
# 眼睛睁大点，这里‘@’调用的是decorator_maker()执行后返回的decorator,值得注意的是，在improt这个文件的时候，不管是否调用decorated_function，decorator_maker()都会执行
@decorator_maker()
def decorated_function():
    print "I am the decorated function."
#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

#最终:
decorated_function()
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
```

回到问题，向装饰器本身传递参数，如果我们可以通过函数去创建装饰器，那么我们可以传递参数给这个函数，对么？
```python
def decorator_maker_with_arguments(decorator_arg1, decorator_arg2):

    print "I make decorators! And I accept arguments:", decorator_arg1, decorator_arg2

    def my_decorator(func):
        # 这里能传递参数的能力，是闭包的特性
        # 更多闭包的内容，参考 http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
        print "I am the decorator. Somehow you passed me arguments:", decorator_arg1, decorator_arg2

        # 不要搞混了装饰器参数和函数参数
        def wrapped(function_arg1, function_arg2) :
            print ("I am the wrapper around the decorated function.\n"
                  "I can access all the variables\n"
                  "\t- from the decorator: {0} {1}\n"
                  "\t- from the function call: {2} {3}\n"
                  "Then I can pass them to the decorated function"
                  .format(decorator_arg1, decorator_arg2,
                          function_arg1, function_arg2))
            return func(function_arg1, function_arg2)

        return wrapped

    return my_decorator

@decorator_maker_with_arguments("Leonard", "Sheldon")
def decorated_function_with_arguments(function_arg1, function_arg2):
    print ("I am the decorated function and only knows about my arguments: {0}"
           " {1}".format(function_arg1, function_arg2))

decorated_function_with_arguments("Rajesh", "Howard")
#outputs:
#I make decorators! And I accept arguments: Leonard Sheldon
#I am the decorator. Somehow you passed me arguments: Leonard Sheldon
#I am the wrapper around the decorated function.
#I can access all the variables
#   - from the decorator: Leonard Sheldon
#   - from the function call: Rajesh Howard
#Then I can pass them to the decorated function
#I am the decorated function and only knows about my arguments: Rajesh Howard
```

到目前为止，我们可以给装饰器传递参数，装饰器函数传递参数，我希望把这两种函数都传递给最装饰的函数，怎么做
```python
# 支持任意参数的装饰器
def decorator_maker_with_var_args(*decorator_maker_agrs, **decorator_maker_kwagrs):
    print type(decorator_maker_agrs), type(decorator_maker_kwagrs)
    print 'i am decorator maker with agrs'
    for arg in decorator_maker_agrs:
        print 'arg from *agrs format ', arg
    for key in decorator_maker_kwagrs:
        print "anthor keyword agr is: %r, %r" % (key, decorator_maker_kwagrs[key])

    def decoratro(fun):
        def wrapper(*agrs, **kwagrs):
            new_kwargs = decorator_maker_kwagrs.copy()
            new_kwargs.update(kwagrs)

            # 可以同时获取装饰器maker， 装饰器的参数
            fun(*(decorator_maker_agrs + agrs), **new_kwargs)
        return wrapper
```

### 使用装饰器
```python
def benchmark(func):
    """
    装饰器打印一个函数的执行时间
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.__name__, time.clock()-t
        return res
    return wrapper

def logging(func):
    """
    装饰器记录函数日志
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs
        return res
    return wrapper

def counter(func):
    """
    记录并打印一个函数的执行次数
    """
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        # 执行了func，并返回执行后的值
        res = func(*args, **kwargs)
        print "{0} has been used: {1}x".format(func.__name__, wrapper.count)
        return res
    wrapper.count = 0
    return wrapper

@counter
@benchmark
@logging
def reverse_string(string):
    return str(reversed(string))

print reverse_string("Able was I ere I saw Elba")


#outputs:
#logging: reverse_string ('Able was I ere I saw Elba',) {}
#benchmark: wrapper 2.6e-05
#counter: wrapper has been used: 1x
#<reversed object at 0x1020edfd0>

# 把一个函数变成守护进程
def daemon_decorator_maker(name, wait):
    def mid_func(func):
        @functools.wraps(func)
        def wrapper(*args):
            while True:
                try:
                    func(*args)
                    time.sleep(wait)
                except Exception:
                    time.sleep(wait)
        return wrapper
    return mid_func


# 缓存class的property
def cached_property(func):
"""Memoize property for class
"""
@functools.wraps(func)
def wrapper(self):
    if not hasattr(self, "_cached_property"):
        self._cached_property = {}
    if func.__name__ not in self._cached_property:
        self._cached_property[func.__name__] = func(self)
        return self._cached_property[func.__name__]
    return property(wrapper)


# 生成key
def gen_keygenerator(namespace, func):
    args = inspect.getargspec(func)
    prefix = "{}:{}|{}".format(func.__module__, func.__name__, namespace)
    has_self = args[0] and args[0][0] in ("self", "cls")

    def generate_key(*args, **kw):
        if has_self:
            args = args[1:]
        tuples = sorted(kw.iteritems())
        return "{}|{}{}".format(prefix, args, tuples)

    return generate_key
```

### 在回到“函数是一个对象”
函数是一个对象，所以，函数会有自己的属性，使用`dir(func_name)`可以查看这个函数对象

```python
# 函数是一个对象
def func_obj(a, b):
    '''
    this id doc
    '''
    pass
print func_obj.__doc__
print func_obj.__module__
print func_obj.__name__
# 对象的属性是可以修改的
func_obj.__doc__ = "updated doc"
print func_obj.__doc__

# output:
# this id doc
# __main__
# func_obj
# updated doc
```

被装饰器装饰之后，因为装饰器返回的是`wrapper`, 而不是原来的`func`, 所以，返回的后的函数的属性变成了`wrapper`

```pythoon
def my_decorator(f):
    def wrapper(*args, **kwds):
        print 'Calling decorated function'
        return f(*args, **kwds)
    return wrapper


@my_decorator
def example():
    """这里是文档注释"""
    print 'Called example function'

example()

# outputs:
# Calling decorated function
# Called example function
# wrapper  函数名变成了wrapper,而非example
# None
```
如何避免这种情况，我们需要使用到functools模块
```python
from functools import wraps
def my_decorator(f):
     @wraps(f)
     def wrapper(*args, **kwds):
         print 'Calling decorated function'
         return f(*args, **kwds)
     return wrapper

@my_decorator
def example():
    """这里是文档注释"""
    print 'Called example function'

example()

# 下面是输出
"""
Calling decorated function
Called example function
"""
print example.__name__ # 'example'
print example.__doc__ # '这里是文档注释'
```


### functools 模块
functools 模块中有三个主要的函数 partial(), update_wrapper() 和 wraps(), 下面我们分别来看一下吧。
```python
partial(func[,args][, *keywords])

def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    # 给函数对象添加新的属性
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc
```


OK，可能一下子没看明白，那么继续往下看，看一下是怎么用的。我们知道 python 中有个 int([x[,base]]) 函数，作用是把字符串转换为一个普通的整型。如果要把所有输入的二进制数转为整型，那么就要这样写 int('11', base=2)。这样写起来貌似不太方便，那么我们就能用 partial 来实现值传递一个参数就能转换二进制数转为整型的方法。
```python
from functools import partial
int2 = partial(int, base=2)

print int2('11') # 3
print int2('101') # 5
update_wrapper(wrapper, wrapped[, assigned][, updated])
```
看这个函数的源代码发现，它就是把被封装的函数的 module, name, doc 和 dict 复制到封装的函数中去，源码如下，很简单的几句：
```python
WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    for attr in assigned:
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    return wrapper
```
具体如何用我们可以往下看一下。
wraps(wrapped[, assigned][, updated])
wraps() 函数把用 partial() 把 update_wrapper() 给封装了一下。
```python
def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):

    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)
```
