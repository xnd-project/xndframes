# -*- coding: utf-8 -*-

# import pytest
import pandas as pd
import pandas.testing as tm
import xnd
from pandas.core.internals import ExtensionBlock

import xndframes as xf

TEST_ARRAY = xnd.xnd(["Test", "string", None])


def test_concatenate_blocks():
    v1 = xf.StringArray(TEST_ARRAY)
    sa = pd.Series(v1)
    result = pd.concat([sa, sa], ignore_index=True)
    EXPECTED_ARRAY = xnd.xnd(["Test", "string", None, "Test", "string", None])
    expected = pd.Series(xf.StringArray(EXPECTED_ARRAY))
    tm.assert_series_equal(result, expected)


def test_series_constructor():
    v = xf.StringArray(TEST_ARRAY)
    result = pd.Series(v)
    assert result.dtype == v.dtype
    assert isinstance(result._data.blocks[0], ExtensionBlock)


def test_dataframe_constructor():
    v = xf.StringArray(TEST_ARRAY)
    df = pd.DataFrame({"A": v})
    assert isinstance(df.dtypes["A"], xf.StringDtype)
    assert df.shape == (3, 1)
    str(df)


def test_dataframe_from_series_no_dict():
    s = pd.Series(xf.StringArray(TEST_ARRAY))
    result = pd.DataFrame(s)
    expected = pd.DataFrame({0: s})
    tm.assert_frame_equal(result, expected)

    s = pd.Series(xf.StringArray(TEST_ARRAY), name='A')
    result = pd.DataFrame(s)
    expected = pd.DataFrame({'A': s})
    tm.assert_frame_equal(result, expected)


def test_dataframe_from_series():
    s = pd.Series(xf.StringArray(TEST_ARRAY))
    c = pd.Series(pd.Categorical(['a', 'b']))
    result = pd.DataFrame({"A": s, "B": c})
    assert isinstance(result.dtypes["A"], xf.StringDtype)


def test_getitem_scalar():
    ser = pd.Series(xf.StringArray(TEST_ARRAY))
    result = ser[1]
    assert result == "string"


def test_getitem_slice():
    ser = pd.Series(xf.StringArray(TEST_ARRAY))
    result = ser[1:]
    expected = pd.Series(xf.StringArray(TEST_ARRAY[1:]), index=range(1, 3))
    tm.assert_series_equal(result, expected)
