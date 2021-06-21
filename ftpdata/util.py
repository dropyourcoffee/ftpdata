from functools import reduce

# Not Used
# def _override_with(**methods):
#
#     class Wrapper(object):
#         def __init__(self, instance):
#             object.__setattr__(self, 'instance',instance)
#
#         def __setattr__(self, name, value):
#             object.__setattr__(object.__getattribute__(self,'instance'), name, value)
#
#         def __getattribute__(self, name):
#             instance = object.__getattribute__(self, 'instance')
#
#             # If this is a wrapped method, return a bound method
#             if name in methods: return (lambda *args, **kargs: methods[name](self,*args,**kargs))
#
#             # Otherwise, just return attribute of instance
#             return instance.__getattribute__(name)
#
#     return Wrapper


def unzip(dict):

    def _inner(acc, curr):
        keys, vals = acc
        new_key, new_val = curr
        return (*keys, new_key), (*vals, new_val)

    return reduce(_inner , [item for item in dict.items()], ((), ()))
