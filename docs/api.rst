API
===

.. currentmodule:: xndframes

Xndframes provides one extension type, :class: `XndframesArray`

:class: `String Array`
---------------------
.. autoclass:: XndframesArray

Methods
"""""""

Various methods that are useful for pandas. When a Series contains a XndframesArray,
calling the Series method will dispatch to these methods.

.. automethod:: XndframesArray.take 
.. automethod:: XndframesArray.unique
.. automethod:: XndframesArray.isna 
