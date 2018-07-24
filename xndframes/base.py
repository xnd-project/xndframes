from __future__ import absolute_import, division, print_function

import itertools
from collections import Iterable
import numpy as np
import pandas as pd
import six
from pandas.api.types import is_array_like, is_bool_dtype, is_integer, is_integer_dtype
from pandas.core.arrays import ExtensionArray
from pandas.core.dtypes.dtypes import ExtensionDtype

import ndtypes
import xnd
from ndtypes import ndt

_python_type_map = {
    str(ndt("int64").hidden_dtype): int,
    str(ndt("?int64").hidden_dtype): int,
    str(ndt("float64").hidden_dtype): float,
    str(ndt("?float64").hidden_dtype): float,
    str(ndt("string").hidden_dtype): six.text_type,
    str(ndt("?string").hidden_dtype): six.text_type,
}


class XndframesDtype(ExtensionDtype):
    def __init__(self, xnd_dtype):
        self.xnd_dtype = xnd_dtype

    def __str__(self):
        return "xndframes[{}]".format(self.xnd_dtype)

    def __repr__(self):
        return "XndframesDType({})".format(str(self.xnd_dtype))

    def __eq__(self, other):
        """Check whether 'other' is equal to self.
        By default, 'other' is considered equal if
        * it is a string matching 'self.name'.
        * it is an instance of this type.

        Parameters
        ----------
        other: Any

        Returns
        -------
        bool
        """
        if isinstance(other, six.string_types):
            return other == self.name

        elif isinstance(other, type(self)):
            return self.xnd_dtype == other.xnd_dtype

        else:
            return False

    @property
    def type(self):
        # type: () -> type
        """The scalar type for the array, e.g. ``int``
        It's expected ``ExtensionArray[item]`` returns an instance
        of ``ExtensionDtype.type`` for scalar ``item``.
        """
        return _python_type_map[str(self.xnd_dtype.hidden_dtype)]

    @property
    def kind(self):
        # type () -> str
        """A character code (one of 'biufcmMOSUV'), default 'O'
        This should match the NumPy dtype used when the array is
        converted to an ndarray, which is probably 'O' for object if
        the extension type cannot be represented as a built-in NumPy
        type.
        See Also
        --------
        numpy.dtype.kind
        """
        return np.dtype(self.type).kind

    @property
    def name(self):
        # type: () -> str
        """A string identifying the data type.
        Will be used for display in, e.g. ``Series.dtype``
        """
        return str(self)

    @classmethod
    def construct_array_type(cls, *args):
        """
        Return the array type associated with this dtype
        Returns
        -------
        type
        """
        if len(args) > 0:
            raise NotImplementedError(
                "construct_array_type does not support arguments")
        return XndframesArray


class XndframesArray(ExtensionArray):
    _can_hold_na = True

    def __init__(self, array):
        if isinstance(array, list):
            self.data = xnd.xnd(array)

        elif isinstance(array, np.ndarray):
            self.data = xnd.xnd(array.tolist())
        elif isinstance(array, xnd.xnd):
            self.data = array
        else:
            raise ValueError(
                "Unsupported type passed for {}: {}".format(
                    self.__name__, type(array)))

        self._dtype = XndframesDtype(self.data.type)

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

    @property
    def dtype(self):
        # type: () -> ExtensionDtype
        return self._dtype

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

    @classmethod
    def _concat_same_type(cls, to_concat):
        """
        Concatenate multiple arrays

        Parameters
        ----------
        to_concat : sequence of this type

        Returns
        ----------
        ExtensionArray
        """
        interim_array = [array.data for array in to_concat]

        return cls(xnd.xnd(list(itertools.chain(*interim_array))))

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
            else:

                return self.data[item]

        value = self.data[item]
        return type(self)(value)

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

    def isna(self):
        """
        Boolean NumPy array indicating if each value is missing.
        This should return a 1-D array the same length as 'self'.
        """
        size = len(self.data)
        isnull_byte_map = np.zeros(size, dtype=bool)
        for i in range(size):
            if self.data[i] is None:
                isnull_byte_map[i] = 1

        return isnull_byte_map

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
        return cls(xnd.xnd(list(scalars)))

    def take(self, indices, allow_fill=False, fill_value=None):
        """
        Take elements from an array.

        Parameters
        ----------
        indices : sequence of integers
             Indices to be taken.
        allow_fill : bool, default False
              How to handle negative values in `indices`.
              * False: negative values in `indices` indicate position indices
                from the right (the default). This is similar to
                :func:`numpy.take`.
              * True: negative values in `indices` indicate missing values.
                These values are set to `fill_value`. Any other negative values
                raise a ``ValueError``.
        fill_value : any, optional
              Fill value to use for NA-indices when `allow_fill` is True.
              This may be ``None``, in which case the default NA value for the
              type, ``self.dtype.na_value``, is used.
              For many ExtensionArrays, there will be two representations of
              `fill_value`: a user-facing "boxed" scalar, and
              a low-level physical NA value. `fill_value` should be the
              user-facing version, and the implementation should
              handle translating that to the physical version for
              processing the take if necessary.

        Returns
        -------
        ExtensionArray

        Raises
        ------
        IndexError
            When the indices are out of bounds for the array.
        ValueError
            When `indices` contain negative values other than ``-1``
            and `allow_fill` is True.

        Notes
        -----
        ExtensionArray.take is called by ``Series.__getitem__``, ``.loc``,
        ``iloc``, when `indices` is a sequence of values. Additionally,
        it's called by :meth:`Series.reindex`, or any other method
        that causes realignemnt, with a `fill_value`.
        See Also
        --------
        numpy.take
        pandas.api.extensions.take

        """
        from pandas.core.algorithms import take

        data = self.astype(object)
        if allow_fill and fill_value is None:
            fill_value = self.dtype.na_value
        # fill value should always be translated from the scalar
        # type for the array, to the physical storage type for
        # the data, before passing to take.
        result = take(
            data,
            indices,
            fill_value=fill_value,
            allow_fill=allow_fill)
        return self._from_sequence(result)

    def factorize(self, na_sentinel=-1):
        np_array = self.__array__()
        return pd.factorize(np_array, na_sentinel=na_sentinel)
