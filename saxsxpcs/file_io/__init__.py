#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File I/O modules for SAXS and XPCS data.
"""

from .base_reader import BaseReader
from .hdf5_reader import HDF5Reader
from .nexus_reader import NeXusReader
from .mask_io import MaskIO
from .file_importer import FileImporter, FileImporterFactory, FileFormatDetector
from .beamlines.desy_p10 import DESYP10Reader
from .beamlines.esrf_id02 import ESRFID02Reader
from .beamlines.esrf_id10 import ESRFID10Reader

__all__ = [
    'BaseReader',
    'HDF5Reader',
    'NeXusReader',
    'MaskIO',
    'FileImporter',
    'FileImporterFactory',
    'FileFormatDetector',
    'DESYP10Reader',
    'ESRFID02Reader',
    'ESRFID10Reader',
]

