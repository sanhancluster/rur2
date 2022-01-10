import numpy as np

import core, config

class HaloData(core.Table):
    """
    A tabulated halo finder result data
    """
    def __init__(self, data: np.array):
        super().__init__(data)
        self.alias = config.alias_common
        self.type = 'None'

    def extra_fields(self, item):
        if(item in config.extra_fields_common.keys):
            return config.extra_fields_common[item](self.data)
        else:
            return super().extra_fields(item)