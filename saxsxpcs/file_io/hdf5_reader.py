#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HDF5 file reader for SAXS and XPCS data.
"""

import logging
import numpy as np
from typing import Dict, Any, Optional, Union
import h5py

from .base_reader import BaseReader

logger = logging.getLogger(__name__)

class HDF5Reader(BaseReader):
    """Reader for HDF5 files."""
    
    def __init__(self, file_path: str):
        """Initialize the HDF5 reader.
        
        Parameters
        ----------
        file_path : str
            Path to the HDF5 file to read.
        """
        super().__init__(file_path)
        self.file = None
    
    def open(self):
        """Open the HDF5 file for reading."""
        try:
            self.file = h5py.File(self.file_path, 'r')
            self.is_open = True
            self.logger.debug(f"Opened HDF5 file: {self.file_path}")
        except Exception as e:
            self.logger.error(f"Error opening HDF5 file {self.file_path}: {e}")
            raise
    
    def close(self):
        """Close the HDF5 file."""
        if self.file is not None:
            try:
                self.file.close()
                self.is_open = False
                self.logger.debug(f"Closed HDF5 file: {self.file_path}")
            except Exception as e:
                self.logger.error(f"Error closing HDF5 file {self.file_path}: {e}")
            finally:
                self.file = None
    
    def read(self) -> bool:
        """Read data from the HDF5 file.
        
        Returns
        -------
        bool
            True if the file was read successfully, False otherwise.
        """
        try:
            if not self.is_open:
                self.open()
            
            # Read all datasets and attributes
            self.read_all_datasets()
            self.read_metadata_to_dict()
            
            return True
        except Exception as e:
            self.logger.error(f"Error reading HDF5 file {self.file_path}: {e}")
            return False
    
    def read_dataset(self, path: str) -> Optional[np.ndarray]:
        """Read a dataset from the HDF5 file.
        
        Parameters
        ----------
        path : str
            Path to the dataset in the HDF5 file.
        
        Returns
        -------
        Optional[np.ndarray]
            Dataset as numpy array, or None if not found.
        """
        try:
            if path in self.file:
                dataset = self.file[path]
                if isinstance(dataset, h5py.Dataset):
                    data = dataset[...]
                    self.logger.debug(f"Read dataset {path} with shape {data.shape}")
                    return data
                else:
                    self.logger.warning(f"Path {path} is not a dataset")
                    return None
            else:
                self.logger.debug(f"Dataset {path} not found in file")
                return None
        except Exception as e:
            self.logger.error(f"Error reading dataset {path}: {e}")
            return None
    
    def read_attribute(self, path: str, attr_name: str) -> Optional[Any]:
        """Read an attribute from the HDF5 file.
        
        Parameters
        ----------
        path : str
            Path to the object in the HDF5 file.
        attr_name : str
            Name of the attribute.
        
        Returns
        -------
        Optional[Any]
            Attribute value, or None if not found.
        """
        try:
            if path in self.file:
                obj = self.file[path]
                if attr_name in obj.attrs:
                    attr_value = obj.attrs[attr_name]
                    # Handle string attributes
                    if isinstance(attr_value, bytes):
                        attr_value = attr_value.decode('utf-8')
                    elif isinstance(attr_value, np.ndarray) and attr_value.dtype.kind in ['S', 'U']:
                        attr_value = str(attr_value)
                    self.logger.debug(f"Read attribute {attr_name} from {path}: {attr_value}")
                    return attr_value
                else:
                    self.logger.debug(f"Attribute {attr_name} not found in {path}")
                    return None
            else:
                self.logger.debug(f"Path {path} not found in file")
                return None
        except Exception as e:
            self.logger.error(f"Error reading attribute {attr_name} from {path}: {e}")
            return None
    
    def read_all_datasets(self):
        """Read all datasets from the HDF5 file."""
        def visit_func(name, obj):
            if isinstance(obj, h5py.Dataset):
                try:
                    # Use the full path as the key
                    key = name.replace('/', '_').strip('_')
                    if not key:
                        key = 'root_dataset'
                    
                    # Read the dataset
                    data = obj[...]
                    self.data[key] = data
                    self.logger.debug(f"Read dataset /{name} as key '{key}' with shape {data.shape}")
                except Exception as e:
                    self.logger.error(f"Error reading dataset /{name}: {e}")
        
        if self.file is not None:
            self.file.visititems(visit_func)
    
    def read_metadata_to_dict(self):
        """Read metadata (attributes) to the metadata dictionary."""
        def visit_func(name, obj):
            # Read attributes from groups and datasets
            for attr_name, attr_value in obj.attrs.items():
                try:
                    # Handle string attributes
                    if isinstance(attr_value, bytes):
                        attr_value = attr_value.decode('utf-8')
                    elif isinstance(attr_value, np.ndarray) and attr_value.dtype.kind in ['S', 'U']:
                        attr_value = str(attr_value)
                    
                    # Create a hierarchical key
                    if name:
                        key = f"{name.replace('/', '_')}_{attr_name}".strip('_')
                    else:
                        key = attr_name
                    
                    self.metadata[key] = attr_value
                    self.logger.debug(f"Read attribute {attr_name} from /{name} as key '{key}': {attr_value}")
                except Exception as e:
                    self.logger.error(f"Error reading attribute {attr_name} from /{name}: {e}")
        
        if self.file is not None:
            # Read root attributes
            visit_func('', self.file)
            # Read attributes from all objects
            self.file.visititems(visit_func)
    
    def list_datasets(self) -> list:
        """List all datasets in the HDF5 file.
        
        Returns
        -------
        list
            List of dataset paths.
        """
        datasets = []
        
        def visit_func(name, obj):
            if isinstance(obj, h5py.Dataset):
                datasets.append(f"/{name}")
        
        if self.file is not None:
            self.file.visititems(visit_func)
        
        return datasets
    
    def list_groups(self) -> list:
        """List all groups in the HDF5 file.
        
        Returns
        -------
        list
            List of group paths.
        """
        groups = []
        
        def visit_func(name, obj):
            if isinstance(obj, h5py.Group):
                groups.append(f"/{name}")
        
        if self.file is not None:
            groups.append("/")  # Root group
            self.file.visititems(visit_func)
        
        return groups
    
    def get_file_structure(self) -> Dict[str, Any]:
        """Get the structure of the HDF5 file.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary representing the file structure.
        """
        structure = {
            'groups': self.list_groups(),
            'datasets': self.list_datasets(),
        }
        
        return structure
    
    @classmethod
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
        try:
            # Check file extension
            if not file_path.lower().endswith(('.h5', '.hdf5', '.nxs', '.nx')):
                return False
            
            # Try to open the file
            with h5py.File(file_path, 'r') as f:
                return True
        except Exception:
            return False

