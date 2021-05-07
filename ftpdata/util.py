
def _override_with(**methods):

    class Wrapper(object):
        def __init__(self, instance):
            object.__setattr__(self, 'instance',instance)

        def __setattr__(self, name, value):
            object.__setattr__(object.__getattribute__(self,'instance'), name, value)

        def __getattribute__(self, name):
            instance = object.__getattribute__(self, 'instance')

            # If this is a wrapped method, return a bound method
            if name in methods: return (lambda *args, **kargs: methods[name](self,*args,**kargs))

            # Otherwise, just return attribute of instance
            return instance.__getattribute__(name)

    return Wrapper
