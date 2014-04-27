# -*- coding: utf-8 -*-
import os
import re
import sys
import contextlib
import keyword
import functools


@contextlib.contextmanager
def chdir(path):
    curr_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(curr_dir)


def is_valid_identifier(string):
    if not re.match("[_A-Za-z][_a-zA-Z0-9]*$", string):
        return False
    if keyword.iskeyword(string):
        return False
    return True


def make_valid_identifier(string):
    string = string.strip()
    string = string.replace("-", "_")
    string = string.replace(" ", "_")
    string = re.sub('[^_a-zA-Z0-9]', '', string)
    string = string.lower()
    if is_valid_identifier(string):
        return string
    else:
        raise RuntimeError("String cannot be converted to a valid identifier.")


def safe_set(args, attr, value):
    if not hasattr(args, attr) or getattr(args, attr) is None:
        setattr(args, attr, value)


def list2str(lst, indent=0):
    lst_str = str(lst)
    lb = ',\n' + indent*' '
    return lst_str.replace(', ', lb)


def exceptions2exit(exception_list):
    def exceptions2exit_decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except tuple(exception_list) as e:
                print(e.message)
                sys.exit(1)
        return func_wrapper
    return exceptions2exit_decorator
