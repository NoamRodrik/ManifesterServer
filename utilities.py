from functools import lru_cache, wraps
from frozendict import *
from flask import request

def make_args_hashable(func):
    def _make_hashable(obj):
        # If we're a list or a tuple, make each object hashable.
        if isinstance(obj, list) or isinstance(obj, tuple):
            return tuple(_make_hashable(x) for x in obj)

        # If we're not a dictionary, no need to make hashable.
        if not isinstance(obj, dict):
            return obj

        # Dictionaries need to recursively freeze inner dictionaries.
        new_dict = dict()
        for (key, val) in obj.items():
            if isinstance(val, dict):
                val = _make_hashable(val)
            new_dict[key] = val
        return frozendict(new_dict)

    @wraps(func)
    def _wrapper(*args, **kwargs):
        frozen_args = _make_hashable(args)
        frozen_kwargs = _make_hashable(kwargs)
        return func(*frozen_args, **frozen_kwargs)

    return _wrapper

def filter_by_arglist(arg, filter_func, db):
    arg_val = request.args.getlist(arg)
    if arg_val:
        return filter_func(arg_val, db)
    return db
