# -*- coding: utf-8 -*-

"""Top-level package for xndframes."""
from .base import XndframesArray, XndframesDtype
from ._version import get_versions
from .string_array import TextAccessor

__version__ = get_versions()["version"]
del get_versions

__all__ = ["XndframesArray", "XndframesDtype", "TextAccessor"]
