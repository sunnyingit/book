# -*- conding: utf-8 -*-

import functools


def thread_cache_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*agrs, **kwagrs):
        fn(*agrs, **kwagrs)
    return wrapper
