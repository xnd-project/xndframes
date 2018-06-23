=====
Usage
=====

This document describes how to use the methods and classes provided by ``xndframes``.

We will assume that the following packages have been imported.

.. ipython:: python
    import xndframes as xf 
    import pandas as pd 
    
Pandas Integration
------------------

``StringArray`` satisfies pandas extension array interface, which means that it can safely be stored inside pandas's 
Series and DataFrame. 

.. ipython:: python 

    values = ["Hello", "World", None, "This is a test"]
    sa = xf.StringArray(values)
    type(sa)
    print(sa.data) 

    ser = pd.Series(sa)
    ser 
    df = pd.DataFrame({"strings": values})
    df

Most pandas methods that make sense should work. The following section will call 
out points of interest. 

