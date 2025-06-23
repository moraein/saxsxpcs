#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Widget modules for the SAXS and XPCS Analysis Suite GUI.
"""

from .file_browser_widget import FileBrowserWidget
from .data_preview_widget import DataPreviewWidget
from .mask_editor_widget import MaskEditorWidget
from .beam_parameter_widget import BeamParameterWidget

__all__ = [
    'FileBrowserWidget',
    'DataPreviewWidget',
    'MaskEditorWidget',
    'BeamParameterWidget',
]

