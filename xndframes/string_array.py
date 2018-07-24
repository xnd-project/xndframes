# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function


import pandas as pd

from .base import XndframesArray


@pd.api.extensions.register_series_accessor("text")
class TextAccessor:
    def __init__(self, obj):
        if not isinstance(obj.values, XndframesArray):
            raise AttributeError(
                "only XndframesArray[string] has text accessor")
        self.obj = obj
        self.data = self.obj.values.data

    def startswith(self, needle, na=None):
        pass

    def endswith(self, needle, na=None):
        pass

    def _call_x_with(self, impl, needle, na=None):
        pass
