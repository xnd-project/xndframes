from __future__ import absolute_import, division, print_function

from collections import Iterable

import ndtypes
import numpy as np
import pandas as pd
from pandas.api.types import (is_array_like, is_bool_dtype, is_integer,
                              is_integer_dtype)
from pandas.core.arrays import ExtensionArray
import xnd


class XndframesArrayBase(ExtensionArray):
    def __array__(self):
        """
        Construct numpy arrays when passed to `np.asarray()`.
        """
        return np.asarray(self.data)

    def __len__(self):
        """
        Length of this array
        """
        return len(self.data)

    def __getitem__(self, item):
        """Select subset of self.

        Parameters
        ----------
        item: int, slice
            * int: The position in 'self' to get.
            * slice: A slice object, where 'start', 'stop', and 'step' are
            integers or None
            * ndarray: A 1-d boolean NumPy ndarray the same length as 'self'

        Returns
        --------
        item: scalar or ExtensionArray

         Notes
        -----
        For scalar ``item``, return a scalar value suitable for the array's
        type. This should be an instance of ``self.dtype.type``.
        For slice ``key``, return an instance of ``ExtensionArray``, even
        if the slice is length 0 or 1.
        For a boolean mask, return an instance of ``ExtensionArray``, filtered
        to the values where ``item`` is True.
        """
        if isinstance(item, slice):
            start = item.start or 0
            stop = item.stop if item.stop is not None else len(self.data)
            stop = min(stop, len(self.data))
            if stop - start == 0:
                return type(self)(xnd.xnd([], type=self.data.type))

        elif isinstance(item, Iterable):
            if not is_array_like(item):
                item = np.array(item)
            if is_integer_dtype(item):
                return self.take(item)
            elif is_bool_dtype(item):
                indices = np.array(item)
                indices = np.argwhere(indices).flatten()
                return self.take(indices)
            else:
                raise IndexError(
                    "Only integers, slices and integer or boolean \
                    arrays are valid indices."
                )

        elif is_integer(item):
            if item < 0:
                item += len(self)
            if item >= len(self):
                return None

    def copy(self, deep=False):
        """
        Return a copy of the array.

        Parameters
        -----------
        deep : bool, default False
              Also copy the underlying data backing this array.

        Returns
        --------
        ExtensionArray
        """
        if deep:
            raise NotImplementedError("Deep Copy is not supported")

        return type(self)(self.data)

    @property
    def nbytes(self):
        """
        Return total bytes consumed by the elements of the array..
        Does not include memory consumed by non-element attributes
        of the array object.
        """

        return self.data.type.datasize

    @property
    def size(self):
        """
        Return the number of elements in the underlying data.
        """
        return len(self.data)

    @property
    def base(self):
        """
        The base object of the underlying data.
        """
        return self.data

    def factorize(self, na_sentinel=-1):
        np_array = np.asarray(xnd.xnd(self.data))
        return pd.factorize(np_array, na_sentinel=na_sentinel)

    def astype(self, dtype, copy=True):
        """
        Cast to a NumPy array with 'dtype'

        Parameters
        -----------
        dtype {str or dtype} --
                Typecode or data-type to which the array is cast

        copy {bool} -- (default: {True})
                Whether to copy the data, even if not necessary.
                If False, a copy is made only if the old dtye does
                not match the new dtype.

        Returns
        --------
        array: ndarray
            NumPy ndarray with 'dtype' for its dtype.
        """
        if isinstance(dtype, ndtypes.ndt):
            raise NotImplementedError(
                "cast propagation in \
            astype not yet implemented"
            )

        else:
            dtype = np.dtype(dtype)
            return np.asarray(self).astype(dtype)

    @classmethod
    def _from_sequence(cls, scalars):
        """
        Construct a new ExtensionArray from a sequence of scalars.

        Parameters
        ----------
        scalars: Sequence
             Each element will be an instance of the scalar type for this array
             ,``cls.dtype.type``.

        Returns
        -------
        ExtensionArray
        """
        return cls(xnd.xnd(scalars))

    def take(self, indices, allow_fill=False, fill_value=None):
        from pandas.core.algorithms import take

        data = self.astype(object)
        if allow_fill and fill_value is None:
            fill_value = self.dtype.na_value

        result = take(
            data,
            indices,
            fill_value=fill_value,
            allow_fill=allow_fill)
        return self._from_sequence(result)
