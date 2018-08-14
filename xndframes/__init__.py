# -*- coding: utf-8 -*-

"""Top-level package for xndframes."""
from .base import Array, Dtype
from ._version import get_versions
from .string_array import TextAccessor

__version__ = get_versions()["version"]
del get_versions

__all__ = ["Array", "Dtype", "TextAccessor"]
