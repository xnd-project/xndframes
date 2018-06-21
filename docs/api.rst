API
===

.. currentmodule:: xndframes

Xndframes provides one extension type, :class: `StringArray`

:class: `String Array`
---------------------
.. autoclass:: StringArray

Methods
"""""""

Various methods that are useful for pandas. When a Series contains a StringArray,
calling the Series method will dispatch to these methods.

.. automethod:: StringArray.take 
.. automethod:: StringArray.unique
.. automethod:: StringArray.isin
.. automethod:: StringArray.isna 
