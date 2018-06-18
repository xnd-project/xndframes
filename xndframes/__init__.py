# -*- coding: utf-8 -*-

"""Top-level package for xndframes."""
from .string_array import StringArray, StringDtype
from ._version import get_versions

__version__ = '0.1.0'

__version__ = get_versions()['version']
del get_versions

__all__ = ["StringArray", "StringDtype"]
