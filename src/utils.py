"""
utils.py
Daniel Goldbach
2013 November

All-purpose utilities for Python coding.
"""

import os
import pickle

import config


def cached(func):
    """
    Decorator to cache function's return values to a file on disk.

    Although it will cache functions that take arguments (e.g. cache f(2) and
    f(3) separately), this is an experimental feature. It will cache the
    function under the function name and the hash of the repr() of the arguments
    tuple. We hash the repr() and not the tuple itself to avoid the problem of
    unhashable arguments.

    If you modify a function, it will still load the old cached version.
    """

    def write_to_cache(fpath, data):
        with open(fpath, 'wb') as fout:
            pickle.dump(data, fout)
        return data

    def wrapper(*func_args):
        fname = '{}-{}-cache.pkl'.format(func.__name__, hash(repr(func_args)))
        fpath = os.path.join(config.CACHE_DIR, fname)

        try:
            return pickle.load(open(fpath, 'rb'))
        except (IOError, EOFError):
            # Cache is corrupt or doesn't exist. Call the func and cache it.
            return write_to_cache(fpath, func(*func_args))

    return wrapper
