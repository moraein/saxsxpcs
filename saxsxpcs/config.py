#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration settings for the SAXS-XPCS Analysis Suite.
"""

import os
from pathlib import Path

# Application information
APP_NAME = "SAXS-XPCS Analysis Suite"
APP_VERSION = "0.1.0"
APP_AUTHOR = "SAXS-XPCS Team"

# Paths
HOME_DIR = Path.home()
APP_DATA_DIR = HOME_DIR / ".saxsxpcs"
CONFIG_DIR = APP_DATA_DIR / "config"
LOG_DIR = APP_DATA_DIR / "logs"
CACHE_DIR = APP_DATA_DIR / "cache"

# Create directories if they don't exist
for directory in [APP_DATA_DIR, CONFIG_DIR, LOG_DIR, CACHE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File formats
SUPPORTED_EXTENSIONS = ['.h5', '.hdf5', '.nxs', '.nx']
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.tiff', '.tif']

# Default settings
DEFAULT_SETTINGS = {
    'file_browser': {
        'default_directory': str(HOME_DIR),
        'show_hidden_files': False,
        'auto_refresh': True,
    },
    'data_preview': {
        'default_colormap': 'viridis',
        'log_scale_default': True,
        'auto_update': True,
    },
    'mask_editor': {
        'default_brush_size': 10,
        'show_mask_overlay': True,
        'mask_alpha': 0.5,
    },
    'beam_parameters': {
        'auto_load_from_file': True,
        'validate_parameters': True,
    },
    'processing': {
        'use_multiprocessing': True,
        'max_workers': None,  # Use all available cores
        'chunk_size': 1000,
    },
    'gui': {
        'theme': 'default',
        'window_size': (1200, 800),
        'remember_window_state': True,
    }
}

# Beamline configurations
BEAMLINE_CONFIGS = {
    'DESY_P10': {
        'name': 'DESY P10',
        'facility': 'DESY',
        'default_wavelength': 1.24,  # Angstrom
        'default_detector_distance': 5000,  # mm
        'default_pixel_size': 75,  # microns
    },
    'ESRF_ID02': {
        'name': 'ESRF ID02',
        'facility': 'ESRF',
        'default_wavelength': 1.0,  # Angstrom
        'default_detector_distance': 3000,  # mm
        'default_pixel_size': 55,  # microns
    },
    'ESRF_ID10': {
        'name': 'ESRF ID10',
        'facility': 'ESRF',
        'default_wavelength': 1.24,  # Angstrom
        'default_detector_distance': 2000,  # mm
        'default_pixel_size': 55,  # microns
    }
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(LOG_DIR / 'saxsxpcs.log'),
            'formatter': 'detailed',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

