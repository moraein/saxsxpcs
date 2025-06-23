#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File importer factory and format detector for SAXS and XPCS data.
"""

import os
import logging
from typing import Dict, List, Optional, Type, Any

from .base_reader import BaseReader
from .hdf5_reader import HDF5Reader
from .nexus_reader import NeXusReader
from .beamlines.desy_p10 import DESYP10Reader
from .beamlines.esrf_id02 import ESRFID02Reader
from .beamlines.esrf_id10 import ESRFID10Reader
from ..utils.logging_config import LoggerMixin

logger = logging.getLogger(__name__)

class FileFormatDetector(LoggerMixin):
    """Detector for file formats and appropriate readers."""
    
    # Registry of available readers
    READERS = [
        DESYP10Reader,
        ESRFID02Reader,
        ESRFID10Reader,
        NeXusReader,
        HDF5Reader,  # Keep as fallback
    ]
    
    @classmethod
    def detect_format(cls, file_path: str) -> Optional[Type[BaseReader]]:
        """Detect the file format and return the appropriate reader class.
        
        Parameters
        ----------
        file_path : str
            Path to the file to analyze.
        
        Returns
        -------
        Optional[Type[BaseReader]]
            Reader class that can handle the file, or None if no suitable reader found.
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        # Try each reader in order of specificity
        for reader_class in cls.READERS:
            try:
                if reader_class.can_read(file_path):
                    logger.debug(f"File {file_path} can be read by {reader_class.__name__}")
                    return reader_class
            except Exception as e:
                logger.debug(f"Error checking {reader_class.__name__} for {file_path}: {e}")
                continue
        
        logger.warning(f"No suitable reader found for file: {file_path}")
        return None
    
    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """Get list of supported file extensions.
        
        Returns
        -------
        List[str]
            List of supported file extensions.
        """
        return ['.h5', '.hdf5', '.nxs', '.nx']

class FileImporterFactory(LoggerMixin):
    """Factory for creating file readers."""
    
    @staticmethod
    def create_reader(file_path: str) -> Optional[BaseReader]:
        """Create a reader for the specified file.
        
        Parameters
        ----------
        file_path : str
            Path to the file to read.
        
        Returns
        -------
        Optional[BaseReader]
            Reader instance, or None if no suitable reader found.
        """
        reader_class = FileFormatDetector.detect_format(file_path)
        if reader_class is None:
            return None
        
        try:
            reader = reader_class(file_path)
            logger.debug(f"Created {reader_class.__name__} for {file_path}")
            return reader
        except Exception as e:
            logger.error(f"Error creating reader for {file_path}: {e}")
            return None

class FileImporter(LoggerMixin):
    """Main file importer class for SAXS and XPCS data."""
    
    def __init__(self):
        """Initialize the file importer."""
        self.readers: Dict[str, BaseReader] = {}
        self.factory = FileImporterFactory()
    
    def import_file(self, file_path: str) -> Optional[BaseReader]:
        """Import a single file.
        
        Parameters
        ----------
        file_path : str
            Path to the file to import.
        
        Returns
        -------
        Optional[BaseReader]
            Reader instance, or None if import failed.
        """
        try:
            # Create reader
            reader = self.factory.create_reader(file_path)
            if reader is None:
                self.logger.error(f"Failed to create reader for {file_path}")
                return None
            
            # Read the file
            success = reader.read()
            if not success:
                self.logger.error(f"Failed to read file {file_path}")
                reader.close()
                return None
            
            # Store the reader
            self.readers[file_path] = reader
            self.logger.info(f"Successfully imported {file_path}")
            return reader
            
        except Exception as e:
            self.logger.error(f"Error importing file {file_path}: {e}")
            return None
    
    def import_files(self, file_paths: List[str]) -> Dict[str, BaseReader]:
        """Import multiple files.
        
        Parameters
        ----------
        file_paths : List[str]
            List of file paths to import.
        
        Returns
        -------
        Dict[str, BaseReader]
            Dictionary mapping file paths to reader instances.
        """
        imported_readers = {}
        
        for file_path in file_paths:
            reader = self.import_file(file_path)
            if reader is not None:
                imported_readers[file_path] = reader
        
        self.logger.info(f"Successfully imported {len(imported_readers)} out of {len(file_paths)} files")
        return imported_readers
    
    def get_reader(self, file_path: str) -> Optional[BaseReader]:
        """Get the reader for a specific file.
        
        Parameters
        ----------
        file_path : str
            Path to the file.
        
        Returns
        -------
        Optional[BaseReader]
            Reader instance, or None if not found.
        """
        return self.readers.get(file_path)
    
    def get_all_readers(self) -> Dict[str, BaseReader]:
        """Get all imported readers.
        
        Returns
        -------
        Dict[str, BaseReader]
            Dictionary mapping file paths to reader instances.
        """
        return self.readers.copy()
    
    def get_file_list(self) -> List[str]:
        """Get list of imported file paths.
        
        Returns
        -------
        List[str]
            List of imported file paths.
        """
        return list(self.readers.keys())
    
    def remove_file(self, file_path: str) -> bool:
        """Remove a file from the importer.
        
        Parameters
        ----------
        file_path : str
            Path to the file to remove.
        
        Returns
        -------
        bool
            True if the file was removed, False otherwise.
        """
        if file_path in self.readers:
            reader = self.readers[file_path]
            reader.close()
            del self.readers[file_path]
            self.logger.info(f"Removed file {file_path}")
            return True
        else:
            self.logger.warning(f"File not found in importer: {file_path}")
            return False
    
    def clear(self):
        """Clear all imported files."""
        for reader in self.readers.values():
            reader.close()
        self.readers.clear()
        self.logger.info("Cleared all imported files")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get a summary of all imported data.
        
        Returns
        -------
        Dict[str, Any]
            Summary of imported data.
        """
        summary = {
            'total_files': len(self.readers),
            'files': {},
        }
        
        for file_path, reader in self.readers.items():
            file_info = reader.get_file_info()
            metadata = reader.get_metadata()
            data = reader.get_data()
            
            file_summary = {
                'file_info': file_info,
                'beamline': metadata.get('beamline', 'Unknown'),
                'facility': metadata.get('facility', 'Unknown'),
                'data_types': list(data.keys()),
                'data_shapes': {key: getattr(value, 'shape', 'N/A') for key, value in data.items()},
            }
            
            summary['files'][file_path] = file_summary
        
        return summary
    
    def __len__(self):
        """Get the number of imported files."""
        return len(self.readers)
    
    def __contains__(self, file_path: str):
        """Check if a file is imported."""
        return file_path in self.readers
    
    def __iter__(self):
        """Iterate over imported file paths."""
        return iter(self.readers.keys())
    
    def __getitem__(self, file_path: str):
        """Get reader by file path."""
        return self.readers[file_path]

