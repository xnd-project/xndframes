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

So far, xndframes implements ``XndframesArray``. ``XndframesArray`` satisfies pandas extension array interface, which means that it can safely be stored inside pandas's 
Series and DataFrame. 

.. ipython:: python 

    s = ["Pandas", "NumPy", "xnd", "SciPy", None, "CuPy", None, "Keras", "Numba"]
    packages = xf.XndframesArray(s)
    type(packages)
    print(packages.data) 

    ser = pd.Series(packages)
    ser 

    vals = list(range(9))
    values = xf.XndframesArray(vals) 
    ser2 = pd.Series(values)
    ser2 

    df = pd.DataFrame({"packages": packages, "id": values})
    df.head()
    df 
    df.describe()

Most pandas methods that make sense should work. The following section will call 
out points of interest. 

.. ipython:: python 

    packages.shape
    packages.unique()
    packages.unique().data 
    packages.isna()

    df.info()




Indexing
""""""""

If your selection returns a scalar, you get back a string.

.. ipython:: python

    ser[0]
    df.loc[2, "packages"]


Missing Data 
""""""""""""

xnd uses `None` to represent missing values. Xndframes does the same. 

.. ipython:: python 

    df.isna()
    
    df.dropna()
