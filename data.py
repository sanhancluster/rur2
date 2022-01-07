import numpy as np

import core, config

class HaloData(core.Table):
    """
    A tabulated halo finder result data
    """
    def __init__(self, data: np.array):
        super().__init__(data)
        self.alias = config.alias_common

    def extra_fields(self, item):

