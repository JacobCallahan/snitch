"""Provides decorators for the Snitch application."""

import functools


def check(weight):
    """Register a method as a system check."""

    def outer(func):
        func._weight = weight

        @functools.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return outer
