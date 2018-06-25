# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import abc
import numpy as np
import six

# import pandas as pd
import xnd

# from pandas.api.types import is_array_like
from pandas.core.dtypes.dtypes import ExtensionDtype

from .base import XndframesArrayBase


@six.add_metaclass(abc.ABCMeta)
class StringArrayBase(object):
    """
    Metaclass providing a common base class for xnd String type.
    """
    pass


StringArrayBase.register(xnd.xnd)


class StringDtype(ExtensionDtype):
    name = "string"
    type = StringArrayBase
    kind = "O"
    na_value = None

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
    """
    Holder for xnd's strings which are pointers to
    NUL-terminated UTF-8 strings.

    StringArray is a container for xnd's Strings. It satisfies pandas'
    extension array interface, and so can be stored inside
    :class:`pandas.Series` and :class:`pandas.DataFrame`.

    see :ref:`usage` for more.

    """

    dtype = StringDtype()
    can_hold_na = True

    def __init__(self, array):
        if isinstance(array, list):
            self.data = xnd.xnd(array)

        elif isinstance(array, np.ndarray):
            self.data = self._from_ndarray(array)

        elif isinstance(array, xnd.xnd):
            self.data = array
        else:
            raise ValueError(
                "Unsupported type passed for StringArray: {}".format(
                    type(array)))

    def _from_ndarray(self, data, copy=False):
        """ construction of a StringArray from an ndarray.

        Parameters
        ----------
        data: ndarray
             This should be a NumPy array with string data type or
             object data type

        copy: bool, default False
              Whether to copy the data.

        Returns
        --------
        ExtensionArray
        """
        if isinstance(data, np.ndarray):
            if data.dtype.kind in {'U', 'S', 'O'}:
                if copy:
                    data = data.copy()

                return xnd.xnd(data.tolist())
    # -----------------------------------------------------------
    #                   Properties
    # -----------------------------------------------------------

    @property
    def na_value(self):
        """
        The missing value sentinal for String.
        """
        return self.dtype.na_value
