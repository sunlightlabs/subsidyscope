def no_self_wrapper(f):
    return lambda self, *args, **kwargs: f(*args, **kwargs)
