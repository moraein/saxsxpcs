#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeXus file reader for the SAXS-XPCS Analysis Suite.
"""

import logging
import numpy as np
from .hdf5_reader import HDF5Reader

logger = logging.getLogger(__name__)

class NeXusReader(HDF5Reader):
    """Reader for NeXus format files."""
    
    def __init__(self, file_path):
        """Initialize the NeXus reader.
        
        Parameters
        ----------
        file_path : str
            Path to the NeXus file.
        """
        super().__init__(file_path)
        self.logger.debug(f"NeXus reader initialized for {file_path}")
    
    def get_metadata(self):
        """Get metadata from the NeXus file.
        
        Returns
        -------
        dict
            Dictionary containing metadata.
        """
        metadata = super().get_metadata()
        
        # Add NeXus-specific metadata
        metadata['file_format'] = 'NeXus'
        
        try:
            with self.open_file() as f:
                # Try to get NeXus-specific metadata
                if 'entry' in f:
                    entry = f['entry']
                    
                    # Get instrument information
                    if 'instrument' in entry:
                        instrument = entry['instrument']
                        if 'name' in instrument:
                            metadata['instrument'] = self.safe_read_dataset(instrument['name'])
                    
                    # Get sample information
                    if 'sample' in entry:
                        sample = entry['sample']
                        if 'name' in sample:
                            metadata['sample_name'] = self.safe_read_dataset(sample['name'])
                
        except Exception as e:
            self.logger.warning(f"Could not read NeXus metadata: {e}")
        
        return metadata
    
    def get_saxs_data(self):
        """Get SAXS data from the NeXus file.
        
        Returns
        -------
        numpy.ndarray or None
            SAXS data array, or None if not found.
        """
        try:
            with self.open_file() as f:
                # Try common NeXus paths for SAXS data
                saxs_paths = [
                    'entry/data/data',
                    'entry/instrument/detector/data',
                    'entry_0000/instrument/detector/data',
                    'entry_0000/ESRF-ID02/eiger500k/data',
                    'entry/ESRF-ID02/eiger500k/data',
                    'data/data',
                    'detector/data'
                ]
                
                for path in saxs_paths:
                    try:
                        if path in f:
                            data = f[path]
                            if hasattr(data, 'shape') and len(data.shape) >= 2:
                                # Read the data
                                saxs_data = data[:]
                                self.logger.info(f"Found SAXS data at {path} with shape {saxs_data.shape}")
                                return saxs_data
                    except Exception as e:
                        self.logger.debug(f"Could not read SAXS data from {path}: {e}")
                        continue
                
                # If no specific SAXS data found, try to get any 2D/3D data
                data_dict = self.get_data()
                for key, value in data_dict.items():
                    if hasattr(value, 'shape') and len(value.shape) >= 2:
                        self.logger.info(f"Using {key} as SAXS data with shape {value.shape}")
                        return value
                
                self.logger.warning("No suitable SAXS data found in NeXus file")
                return None
                
        except Exception as e:
            self.logger.error(f"Error reading SAXS data from NeXus file: {e}")
            return None
    
    def get_xpcs_data(self):
        """Get XPCS data from the NeXus file.
        
        Returns
        -------
        dict
            Dictionary containing XPCS data.
        """
        xpcs_data = {}
        
        try:
            with self.open_file() as f:
                # Try common NeXus paths for XPCS data
                xpcs_paths = {
                    'g2': [
                        'entry/analysis/g2',
                        'entry_0000/analysis/g2',
                        'analysis/g2',
                        'g2'
                    ],
                    'tau': [
                        'entry/analysis/tau',
                        'entry_0000/analysis/tau',
                        'analysis/tau',
                        'tau'
                    ],
                    'intensity': [
                        'entry/analysis/intensity',
                        'entry_0000/analysis/intensity',
                        'analysis/intensity',
                        'intensity'
                    ],
                    'twotime': [
                        'entry/analysis/twotime',
                        'entry_0000/analysis/twotime',
                        'analysis/twotime',
                        'twotime'
                    ]
                }
                
                for data_type, paths in xpcs_paths.items():
                    for path in paths:
                        try:
                            if path in f:
                                data = f[path]
                                xpcs_data[data_type] = data[:]
                                self.logger.debug(f"Found {data_type} data at {path}")
                                break
                        except Exception as e:
                            self.logger.debug(f"Could not read {data_type} from {path}: {e}")
                            continue
                
        except Exception as e:
            self.logger.error(f"Error reading XPCS data from NeXus file: {e}")
        
        return xpcs_data
    
    def get_q_map(self):
        """Get Q-map from the NeXus file.
        
        Returns
        -------
        numpy.ndarray or None
            Q-map array, or None if not found.
        """
        try:
            with self.open_file() as f:
                # Try common NeXus paths for Q-map
                q_paths = [
                    'entry/analysis/q_map',
                    'entry_0000/analysis/q_map',
                    'analysis/q_map',
                    'q_map'
                ]
                
                for path in q_paths:
                    try:
                        if path in f:
                            q_map = f[path][:]
                            self.logger.debug(f"Found Q-map at {path}")
                            return q_map
                    except Exception as e:
                        self.logger.debug(f"Could not read Q-map from {path}: {e}")
                        continue
                
                return None
                
        except Exception as e:
            self.logger.error(f"Error reading Q-map from NeXus file: {e}")
            return None
    
    def get_mask(self):
        """Get mask from the NeXus file.
        
        Returns
        -------
        numpy.ndarray or None
            Mask array, or None if not found.
        """
        try:
            with self.open_file() as f:
                # Try common NeXus paths for mask
                mask_paths = [
                    'entry/analysis/mask',
                    'entry_0000/analysis/mask',
                    'analysis/mask',
                    'mask'
                ]
                
                for path in mask_paths:
                    try:
                        if path in f:
                            mask = f[path][:]
                            self.logger.debug(f"Found mask at {path}")
                            return mask
                    except Exception as e:
                        self.logger.debug(f"Could not read mask from {path}: {e}")
                        continue
                
                return None
                
        except Exception as e:
            self.logger.error(f"Error reading mask from NeXus file: {e}")
            return None
    
    def list_datasets(self):
        """List all datasets in the NeXus file.
        
        Returns
        -------
        list
            List of dataset paths.
        """
        datasets = []
        
        try:
            with self.open_file() as f:
                def visit_func(name, obj):
                    if hasattr(obj, 'shape'):  # It's a dataset
                        datasets.append(name)
                
                f.visititems(visit_func)
                
        except Exception as e:
            self.logger.error(f"Error listing datasets: {e}")
        
        return datasets
