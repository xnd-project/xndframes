# -*- coding: utf-8 -*-

# import pytest
import pandas as pd
import pandas.testing as tm
import xnd
from pandas.core.internals import ExtensionBlock
import numpy as np
import xndframes as xf

TEST_ARRAY = ["Test", "string", None]


def test_constructors():
    v1 = xf.Array(TEST_ARRAY)
    assert isinstance(v1.dtype, xf.Dtype)
    v2 = xf.Array(np.array(TEST_ARRAY))
    assert isinstance(v2.dtype, xf.Dtype)
    v3 = xf.Array(xnd.xnd(TEST_ARRAY))
    assert isinstance(v3.dtype, xf.Dtype)


def test_concatenate_blocks():
    v1 = xf.Array(TEST_ARRAY)
    sa = pd.Series(v1)
    result = pd.concat([sa, sa], ignore_index=True)
    EXPECTED_ARRAY = xnd.xnd(["Test", "string", None, "Test", "string", None])
    expected = pd.Series(xf.Array(EXPECTED_ARRAY))
    tm.assert_series_equal(result, expected)


def test_series_constructor():
    v = xf.Array(TEST_ARRAY)
    result = pd.Series(v)
    assert result.dtype == v.dtype
    assert isinstance(result._data.blocks[0], ExtensionBlock)


def test_dataframe_constructor():
    v = xf.Array(TEST_ARRAY)
    df = pd.DataFrame({"A": v})
    assert isinstance(df.dtypes["A"], xf.Dtype)
    assert df.shape == (3, 1)
    str(df)


def test_dataframe_from_series_no_dict():
    s = pd.Series(xf.Array(TEST_ARRAY))
    result = pd.DataFrame(s)
    expected = pd.DataFrame({0: s})
    tm.assert_frame_equal(result, expected)

    s = pd.Series(xf.Array(TEST_ARRAY), name="A")
    result = pd.DataFrame(s)
    expected = pd.DataFrame({"A": s})
    tm.assert_frame_equal(result, expected)


def test_dataframe_from_series():
    s = pd.Series(xf.Array(TEST_ARRAY))
    c = pd.Series(pd.Categorical(["a", "b"]))
    result = pd.DataFrame({"A": s, "B": c})
    assert isinstance(result.dtypes["A"], xf.Dtype)


def test_getitem_scalar():
    sa = xf.Array(TEST_ARRAY)
    ser = pd.Series(sa)
    result = ser[1]
    assert result == sa.data[1]

    result = ser[5]
    assert result is None

    result = ser[-3]
    assert result == "Test"


def test_getitem_slice():
    ser = pd.Series(xf.Array(TEST_ARRAY))
    result = ser[1:]
    expected = pd.Series(xf.Array(TEST_ARRAY[1:]), index=range(1, 3))
    tm.assert_series_equal(result, expected)


def test_getitem_iterable():
    ser = pd.Series(xf.Array(TEST_ARRAY))
    result = ser[[0, 1]]
    expected = pd.Series(xf.Array(TEST_ARRAY[0:2]), index=range(0, 2))
    tm.assert_series_equal(result, expected)


def test_isna():
    ser = pd.Series(xf.Array(TEST_ARRAY))
    result = ser.isna().values
    expected = np.array([False, False, True])
    np.testing.assert_array_equal(result, expected)


def test_copy():
    ser = pd.Series(xf.Array(TEST_ARRAY))
    copy = ser.copy()
    tm.assert_series_equal(ser, copy)


def test_nbytes():
    sa = xf.Array(TEST_ARRAY)
    result = sa.nbytes
    expected = len(TEST_ARRAY) * 8
    assert result == expected


def test_factorize():
    ser = pd.Series(xf.Array(TEST_ARRAY))
    labels, uniques = ser.factorize()
    expected_labels = np.array([0, 1, -1])
    np.testing.assert_array_equal(labels, expected_labels)


def test_astype():
    ser = pd.Series(xf.Array(TEST_ARRAY))
    as_ser = ser.astype("object")
    result = as_ser.dtype
    result is np.dtype("object")


def test_size():
    ser = pd.Series(xf.Array(TEST_ARRAY))
    assert ser.size == len(TEST_ARRAY)


def test_take():
    ser = pd.Series(xf.Array(TEST_ARRAY))
    result = ser.take([0, 2, 1])
    assert isinstance(result, pd.Series)
