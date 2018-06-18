# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import numpy as np
# import pandas as pd
import xnd
# from pandas.api.types import is_array_like
from pandas.core.dtypes.dtypes import ExtensionDtype

from .base import XndframesArrayBase


class StringDtype(ExtensionDtype):
    name = "string"
    type = str
    kind = "O"

    @classmethod
    def construct_from_string(cls, string):
        if string == "string":
            return cls()
        else:
            raise TypeError(
                "Cannot construct a '{}' from "
                "'{}'".format(
                    cls, string))


class StringArray(XndframesArrayBase):
    dtype = StringDtype()

    def __init__(self, array):
        if isinstance(array, list):
            self.data = xnd.xnd(array)

        elif isinstance(array, np.ndarray):
            self.data = xnd.xnd.from_buffer(array)

        elif isinstance(array, xnd.xnd):
            self.data = array 
        else:
            raise ValueError(
                "Unsupported type passed for StringArray: {}".format(
                    type(array)))
