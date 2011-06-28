from operator import isCallable

def compose(g, f):
    def h(*args, **kwargs):
        return g(f(*args, **kwargs))
    return h

class Either(tuple):
    def __new__(klass, *args):
        return tuple.__new__(klass, *args)

class Success(Either):
    def __new__(klass, value):
        return Either.__new__(klass, (value, None))

class Failure(Either):
    def __new__(klass, value):
        return tuple.__new__(klass, (None, value))

def unpack(e):
    (s, f) = e
    return s if isinstance(e, Success) else f

def raise_it(value):
    raise value

def raise_as(klass):
    return compose(raise_it, klass)

def on(e, branches):
    if type(e) in branches:
        b = branches[type(e)]
        if isCallable(b):
            return b(unpack(e))
        else:
            return b
    else:
        raise KeyError("The type of the value passed was not found in the branching map.")

def when(value, test, branches):
    for (key, branch) in branches.iteritems():
        if test(value, key):
            if isCallable(branch):
                return branch(value)
            else:
                return branch
    raise KeyError("The result of the {test}({value}) was not found in the branching map.".format(test=test.__name__, value=repr(value)))

