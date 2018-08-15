# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Decorators"""


from threading import Thread


def async(f):
    """Async decorator"""
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
