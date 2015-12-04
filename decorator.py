# -*- coding: utf8 -*-

import functools
import time


# 函数是一个对象， 可以把函数名赋值，传递
# def fun_var():
#     print 'i am a function var'
# fun_var_1 = fun_var
# # fun_var_1()


# def decorator_boby(fun):
#     print 'i am a decorator boby'
#     fun()


# def decorator(fun):
#     print 'i am a decorator'

#     def wrapper():
#         fun()
#     return wrapper


# @decorator  # 等价于 decorator_boby(func)
# def fun_decratored():
#     print 'function has been decorator'


# # 参数传递给被装饰的函数,
# def decorator(fun):
#     print 'i am a decorator'

#     def wrapper(arg1, arg2):
#         print 'i got args', arg1, arg2
#         fun(arg1, arg2)
#     return wrapper


# @decorator
# def print_x_y(x, y):
#     print 'x is {}, y is {}'.format(x, y)


# 调用print_x_y函数的时候，会先执行decorator(func)函数，返回wrapper, 然后执行wrapper, 执行
# print_x_y 等价于执行wrapper(x,y), 这样x, y就被传入了被装饰的函数


# 带有参数的装饰器
def decorator_maker_with_args(agr1, agr2):
    print 'i am a decorator maker with args:', agr1, agr2

    # 装饰器的参数永远只有一个
    def decorator(fun):
        # fun 又被装饰了
        @functools.wraps(fun)
        def wrapper(arg3, arg4):
            print 'i am a decorator function with args', arg3, arg4
            # 因为闭包的关系，wrapper里面也可以访问到arg1, arg2
            print 'get params from decorator maker:', agr1, agr2
            fun(arg3, arg4)
        return wrapper
    return decorator


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

# decorator_maker_with_var_args(key='value', test='test')


# @decorator_maker_with_args('maker_arg1', 'maker_arg2')  # 导入这个模块的时候，这个函数已经被执行，不管是否调用print_a_b函数
# def print_a_b(x, y):
#     'function doc'
#     print x, y

# print print_a_b.__name__
# print_a_b(1, 2)
# print print_a_b.__doc__


#
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

