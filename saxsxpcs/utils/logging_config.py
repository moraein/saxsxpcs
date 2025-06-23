#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Logging configuration for the SAXS-XPCS Analysis Suite.
"""

import logging
import logging.config
import sys
from pathlib import Path

from ..config import LOG_DIR, LOGGING_CONFIG

def setup_logging(debug=False, log_file=None):
    """Setup logging configuration.
    
    Parameters
    ----------
    debug : bool, optional
        Enable debug logging, by default False
    log_file : str, optional
        Custom log file path, by default None
    """
    # Create a copy of the logging config
    config = LOGGING_CONFIG.copy()
    
    # Update log level if debug is enabled
    if debug:
        config['handlers']['console']['level'] = 'DEBUG'
    
    # Update log file if specified
    if log_file:
        config['handlers']['file']['filename'] = log_file
    
    # Apply the configuration
    logging.config.dictConfig(config)
    
    # Log the startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Debug: {debug}, Log file: {config['handlers']['file']['filename']}")

def get_logger(name):
    """Get a logger with the specified name.
    
    Parameters
    ----------
    name : str
        Logger name
    
    Returns
    -------
    logging.Logger
        Logger instance
    """
    return logging.getLogger(name)

class LoggerMixin:
    """Mixin class to add logging functionality to other classes."""
    
    @property
    def logger(self):
        """Get the logger for this class."""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__module__ + '.' + self.__class__.__name__)
        return self._logger

