
# xndframes

[![Build Status](https://travis-ci.org/Quansight/xndframes.svg?branch=master)](https://travis-ci.org/Quansight/xndframes)

[![Documentation Status](https://readthedocs.org/projects/xndframes/badge/?version=latest)](https://xndframes.readthedocs.io/en/latest)

[![codecov](https://codecov.io/gh/Quansight/xndframes/branch/master/graph/badge.svg)](https://codecov.io/gh/Quansight/xndframes)

Xndframes is a Python package that provides a set of Pandas ExtensionDType/Array implementations backed by [xnd](https://github.com/plures/xnd).
Xnd implements a container type that maps most Python values relevant for scientific computing directly to typed memory.

Xndframes provides support for storing xnd containers data inside a pandas Series and/or Dataframe using pandas' [Extension Array Interface](http://pandas-docs.github.io/pandas-docs-travis/extending.html#extension-types).

```python
In [1]: import xndframes as xf

In [2]: import pandas as pd

In [3]: s = ["Hello", "World"]

In [4]: sa = xf.StringArray(s)

In [5]: sa.data
Out[5]: xnd(['Hello', 'World'], type='2 * string')

In [6]: sa
Out[6]: <xndframes.string_array.StringArray at 0x7fde41299128>

In [7]: ser = pd.Series(sa)

In [8]: ser
Out[8]:
0    Hello
1    World
dtype: string

In [9]: df = pd.DataFrame({'col1': sa})

In [10]: df
Out[10]:
    col1
0  Hello
1  World

In [11]: df.head()
Out[11]:
    col1
0  Hello
1  World

In [12]: df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2 entries, 0 to 1
Data columns (total 1 columns):
col1    2 non-null string
dtypes: string(1)
memory usage: 96.0 bytes

In [13]: df.isna()
Out[13]:
    col1
0  False
1  False
```

See the [documentation](https://xndframes.readthedocs.io) for more.

## Try xndframes in the cloud

To try out xndframes interactively in your web browser, just click on the binder link:

[![Binder](https://i.imgur.com/xzKbKkP.png)](https://mybinder.org/v2/gh/Quansight/xndframes/master)

## Contributing

Contributions are welcome! For bug reports or requests please submit an issue.
