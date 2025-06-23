#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DESY P10 beamline reader for SAXS and XPCS data.
"""

import logging
import numpy as np
from typing import Dict, Any, Optional

from ..hdf5_reader import HDF5Reader

logger = logging.getLogger(__name__)

class DESYP10Reader(HDF5Reader):
    """Reader for DESY P10 beamline files."""
    
    def __init__(self, file_path: str):
        """Initialize the DESY P10 reader.
        
        Parameters
        ----------
        file_path : str
            Path to the DESY P10 file to read.
        """
        super().__init__(file_path)
        self.beamline = "DESY P10"
    
    def read(self) -> bool:
        """Read data from the DESY P10 file.
        
        Returns
        -------
        bool
            True if the file was read successfully, False otherwise.
        """
        try:
            if not self.is_open:
                self.open()
            
            # Read DESY P10-specific structure
            self.read_p10_structure()
            
            # Also read all datasets and metadata
            self.read_all_datasets()
            self.read_metadata_to_dict()
            
            # Extract and organize P10-specific metadata
            self.extract_p10_metadata()
            
            return True
        except Exception as e:
            self.logger.error(f"Error reading DESY P10 file {self.file_path}: {e}")
            return False
    
    def read_p10_structure(self):
        """Read DESY P10-specific data structure."""
        # Common P10 data paths
        p10_paths = {
            'detector_data': [
                '/entry/data/data',
                '/entry/instrument/detector/data',
                '/entry/data/pilatus_data',
                '/data/data',
            ],
            'saxs_data': [
                '/entry/data/saxs',
                '/entry/result/saxs',
                '/saxs/data',
            ],
            'xpcs_data': [
                '/entry/data/xpcs',
                '/entry/result/xpcs',
                '/xpcs/data',
            ],
            'g2_data': [
                '/entry/result/g2',
                '/entry/data/g2',
                '/g2/data',
                '/g2',
            ],
            'tau_data': [
                '/entry/result/tau',
                '/entry/data/tau',
                '/tau/data',
                '/tau',
            ],
            'twotime_data': [
                '/entry/result/twotime',
                '/entry/data/twotime',
                '/twotime/data',
                '/twotime',
            ],
            'q_map': [
                '/entry/result/q_map',
                '/entry/data/q_map',
                '/q_map/data',
                '/q_map',
            ],
            'mask': [
                '/entry/data/mask',
                '/entry/instrument/detector/mask',
                '/mask/data',
                '/mask',
            ],
        }
        
        for data_type, paths in p10_paths.items():
            for path in paths:
                data = self.read_dataset(path)
                if data is not None:
                    self.data[data_type] = data
                    self.logger.debug(f"Read P10 {data_type} from {path} with shape {data.shape}")
                    break  # Use the first found path
    
    def extract_p10_metadata(self):
        """Extract DESY P10-specific metadata."""
        # Common P10 metadata paths
        metadata_paths = {
            'beam_center_x': [
                '/entry/instrument/detector/beam_center_x',
                '/entry/data/beam_center_x',
                '/beam_center_x',
            ],
            'beam_center_y': [
                '/entry/instrument/detector/beam_center_y',
                '/entry/data/beam_center_y',
                '/beam_center_y',
            ],
            'detector_distance': [
                '/entry/instrument/detector/distance',
                '/entry/data/detector_distance',
                '/detector_distance',
            ],
            'wavelength': [
                '/entry/instrument/source/wavelength',
                '/entry/data/wavelength',
                '/wavelength',
            ],
            'energy': [
                '/entry/instrument/source/energy',
                '/entry/data/energy',
                '/energy',
            ],
            'pixel_size_x': [
                '/entry/instrument/detector/x_pixel_size',
                '/entry/data/pixel_size_x',
                '/pixel_size_x',
            ],
            'pixel_size_y': [
                '/entry/instrument/detector/y_pixel_size',
                '/entry/data/pixel_size_y',
                '/pixel_size_y',
            ],
            'exposure_time': [
                '/entry/instrument/detector/count_time',
                '/entry/data/exposure_time',
                '/exposure_time',
            ],
            'sample_name': [
                '/entry/sample/name',
                '/entry/data/sample_name',
                '/sample_name',
            ],
            'sample_temperature': [
                '/entry/sample/temperature',
                '/entry/data/sample_temperature',
                '/sample_temperature',
            ],
            'start_time': [
                '/entry/start_time',
                '/entry/data/start_time',
                '/start_time',
            ],
            'end_time': [
                '/entry/end_time',
                '/entry/data/end_time',
                '/end_time',
            ],
        }
        
        for key, paths in metadata_paths.items():
            for path in paths:
                data = self.read_dataset(path)
                if data is not None:
                    # Handle scalar values
                    if isinstance(data, np.ndarray) and data.size == 1:
                        data = data.item()
                    self.metadata[key] = data
                    self.logger.debug(f"Read P10 metadata {key}: {data}")
                    break  # Use the first found path
        
        # Add beamline information
        self.metadata['beamline'] = self.beamline
        self.metadata['facility'] = 'DESY'
    
    def get_saxs_data(self) -> Optional[np.ndarray]:
        """Get SAXS data.
        
        Returns
        -------
        Optional[np.ndarray]
            SAXS data array, or None if not found.
        """
        # Try different keys for SAXS data
        saxs_keys = ['saxs_data', 'detector_data', 'data']
        for key in saxs_keys:
            if key in self.data:
                return self.data[key]
        return None
    
    def get_xpcs_data(self) -> Dict[str, Optional[np.ndarray]]:
        """Get XPCS data.
        
        Returns
        -------
        Dict[str, Optional[np.ndarray]]
            Dictionary containing XPCS data arrays.
        """
        xpcs_data = {}
        
        # Get g2 data
        if 'g2_data' in self.data:
            xpcs_data['g2'] = self.data['g2_data']
        
        # Get tau data
        if 'tau_data' in self.data:
            xpcs_data['tau'] = self.data['tau_data']
        
        # Get two-time correlation data
        if 'twotime_data' in self.data:
            xpcs_data['twotime'] = self.data['twotime_data']
        
        # Get XPCS data (if available as a single dataset)
        if 'xpcs_data' in self.data:
            xpcs_data['xpcs'] = self.data['xpcs_data']
        
        return xpcs_data
    
    def get_q_map(self) -> Optional[np.ndarray]:
        """Get Q-map data.
        
        Returns
        -------
        Optional[np.ndarray]
            Q-map array, or None if not found.
        """
        return self.data.get('q_map')
    
    def get_mask(self) -> Optional[np.ndarray]:
        """Get mask data.
        
        Returns
        -------
        Optional[np.ndarray]
            Mask array, or None if not found.
        """
        return self.data.get('mask')
    
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
            # First check if it's a valid HDF5 file
            if not super().can_read(file_path):
                return False
            
            # Check for P10-specific structure
            import h5py
            with h5py.File(file_path, 'r') as f:
                # Look for P10-specific paths or attributes
                p10_indicators = [
                    '/entry/data/pilatus_data',
                    '/entry/instrument/detector/pilatus',
                    '/data/data',
                ]
                
                for indicator in p10_indicators:
                    if indicator in f:
                        return True
                
                # Check for P10-specific attributes
                if 'beamline' in f.attrs:
                    beamline = f.attrs['beamline']
                    if isinstance(beamline, bytes):
                        beamline = beamline.decode('utf-8')
                    if 'P10' in str(beamline).upper():
                        return True
                
                return False
        except Exception:
            return False

    @classmethod
    def can_read_file(cls, file_path):
        """Check if this reader can read the given file.
        
        Parameters
        ----------
        file_path : str
            Path to the file to check.
            
        Returns
        -------
        bool
            True if this reader can read the file, False otherwise.
        """
        try:
            import h5py
            with h5py.File(file_path, 'r') as f:
                # Check for P10-specific indicators
                p10_indicators = [
                    'entry/instrument/pilatus',
                    'entry/instrument/detector',
                    'pilatus',
                    'detector'
                ]
                
                for indicator in p10_indicators:
                    if indicator in f:
                        return True
                
                # Check for P10 in file attributes or metadata
                if hasattr(f, 'attrs'):
                    for key, value in f.attrs.items():
                        if isinstance(value, (str, bytes)):
                            value_str = value.decode() if isinstance(value, bytes) else value
                            if 'p10' in value_str.lower() or 'desy' in value_str.lower():
                                return True
                
                return False
                
        except Exception:
            return False

