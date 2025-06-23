#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GUI modules for the SAXS and XPCS Analysis Suite.
"""

from .main_window import MainWindow
from .widgets import (
    FileBrowserWidget, DataPreviewWidget, MaskEditorWidget, BeamParameterWidget
)

__all__ = [
    'MainWindow',
    'FileBrowserWidget',
    'DataPreviewWidget',
    'MaskEditorWidget',
    'BeamParameterWidget',
]

