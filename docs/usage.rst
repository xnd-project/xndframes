=====
Usage
=====

Xndframes is meant to provide a set of Pandas ExtensionDType/Array implementations backed by xnd

This document describes how to use the methods and classes provided by ``xndframes``. 

We will assume that the following packages have been imported.

.. ipython:: python

    import xndframes as xf 
    import pandas as pd 
    

Pandas Integration
------------------

So far, xndframes implements ``StringArray``. ``StringArray`` satisfies pandas extension array interface, which means that it can safely be stored inside pandas's 
Series and DataFrame. 

.. ipython:: python 

    values = ["Pandas", "NumPy", "xnd", "SciPy", None, "CuPy", None]
    sa = xf.StringArray(values)
    type(sa)
    print(sa.data) 

    ser = pd.Series(sa)
    ser 
    df = pd.DataFrame({"packages": sa})
    df

Most pandas methods that make sense should work. The following section will call 
out points of interest. 

.. ipython:: python 

    sa.shape
    sa.unique()
    sa.unique().data 
    sa.isna()


Indexing
""""""""

If your selection returns a scalar, you get back a string.

.. ipython:: python

    ser[0]
    df.loc[2, "packages"]


Missing Data 
""""""""""""

xnd uses `None` to represent missing values. Xndframes does the same. 

..ipython:: python 

    df.isna()
    df.dropna()
