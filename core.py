import numpy as np
import config

class Alias(dict):
    def __missing__(self, key):
        return key

class Table:
    """
    A wrapper class to store tabulated data.
    Basically acts like structured numpy.array, but some functions may not work.
    """
    def __init__(self, data: np.array):
        self.data = data
        self.alias = Alias({})

    def __getitem__(self, item):
        if(isinstance(item, str)):
            item = self.alias[item]
            if(item not in self.data.keys):
                return self.extra_fields(item)
            else:
                return self.__getitem__(item)
        if(isinstance(item, tuple)):
            item, unit = item
            return self.__getitem__(item) / self.unit_scale(unit)
        else:
            return self.data[item]

    def __str__(self):
        return self.data.__str__()
    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)
    def __getattr__(self, attr):
        return self.data.__getattribute__(attr)
    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)

    def set_alias(self, alias, key):
        self.alias[alias] = key

    def extra_fields(self, item):
        raise ValueError("Unknown field : %s" % item)

    def unit_scale(self, item):
        pass
