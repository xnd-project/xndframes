# -*- coding: utf-8 -*-

# import pytest
import pandas as pd
import pandas.testing as tm
import xndframes as xf
import xnd

TEST_ARRAY = xnd.xnd(["Test", "string", None])


def test_concatenate_blocks():
    v1 = xf.StringArray(TEST_ARRAY)
    sa = pd.Series(v1)
    result = pd.concat([sa, sa], ignore_index=True)
    EXPECTED_ARRAY = xnd.xnd(["Test", "string", None, "Test", "string", None])
    expected = pd.Series(xf.StringArray(EXPECTED_ARRAY))
    tm.assert_series_equal(result, expected)


def test_dataframe_constructor():
    v = xf.StringArray(TEST_ARRAY)
    df = pd.DataFrame({"A": v})
    assert isinstance(df.dtypes["A"], xf.StringDtype)
    assert df.shape == (3, 1)
    str(df)
