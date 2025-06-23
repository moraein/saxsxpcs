#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base reader class for SAXS and XPCS data files.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from ..utils.logging_config import LoggerMixin

logger = logging.getLogger(__name__)

class BaseReader(ABC, LoggerMixin):
    """Abstract base class for file readers."""
    
    def __init__(self, file_path: str):
        """Initialize the base reader.
        
        Parameters
        ----------
        file_path : str
            Path to the file to read.
        """
        self.file_path = file_path
        self.data = {}
        self.metadata = {}
        self.is_open = False
        
        # Validate file path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
    
    @abstractmethod
    def open(self):
        """Open the file for reading."""
        pass
    
    @abstractmethod
    def close(self):
        """Close the file."""
        pass
    
    @abstractmethod
    def read(self) -> bool:
        """Read data from the file.
        
        Returns
        -------
        bool
            True if the file was read successfully, False otherwise.
        """
        pass
    
    @classmethod
    @abstractmethod
    def can_read(cls, file_path: str) -> bool:
        """Check if the file can be read by this reader.
        
        Parameters
        ----------
        file_path : str
            Path to the file to check.
        
        Returns
        -------
        bool
            True if the file can be read by this reader, False otherwise.
        """
        pass
    
    def get_data(self) -> Dict[str, Any]:
        """Get the data dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary containing the data.
        """
        return self.data
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get the metadata dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary containing the metadata.
        """
        return self.metadata
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get file information.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary containing file information.
        """
        stat = os.stat(self.file_path)
        return {
            'file_path': self.file_path,
            'file_name': os.path.basename(self.file_path),
            'file_size': stat.st_size,
            'modification_time': stat.st_mtime,
            'creation_time': stat.st_ctime,
        }
    
    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def __repr__(self):
        """String representation."""
        return f"{self.__class__.__name__}('{self.file_path}')"

