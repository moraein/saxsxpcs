"""
SAXS and XPCS Analysis Suite

A comprehensive tool for analyzing SAXS and XPCS data from various beamlines.
"""

__version__ = "0.1.0"
__author__ = "SAXS-XPCS Team"
__email__ = "support@saxsxpcs.org"

from .file_io import FileImporter
from .gui import MainWindow

__all__ = [
    'FileImporter',
    'MainWindow',
]

