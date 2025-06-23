#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mask I/O functionality for SAXS and XPCS data.
"""

import os
import logging
import numpy as np
from typing import Optional, Union
import h5py
from skimage import io as skimage_io

from ..utils.logging_config import LoggerMixin

logger = logging.getLogger(__name__)

class MaskIO(LoggerMixin):
    """Class for loading and saving masks."""
    
    @staticmethod
    def load_mask(file_path: str) -> Optional[np.ndarray]:
        """Load a mask from file.
        
        Parameters
        ----------
        file_path : str
            Path to the mask file.
        
        Returns
        -------
        Optional[np.ndarray]
            Mask array, or None if loading failed.
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"Mask file not found: {file_path}")
                return None
            
            # Determine file format and load accordingly
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.h5', '.hdf5']:
                return MaskIO._load_mask_hdf5(file_path)
            elif file_ext in ['.npy']:
                return MaskIO._load_mask_npy(file_path)
            elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.tif']:
                return MaskIO._load_mask_image(file_path)
            elif file_ext in ['.txt', '.dat']:
                return MaskIO._load_mask_text(file_path)
            else:
                logger.error(f"Unsupported mask file format: {file_ext}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading mask from {file_path}: {e}")
            return None
    
    @staticmethod
    def save_mask(mask: np.ndarray, file_path: str, format: str = 'auto') -> bool:
        """Save a mask to file.
        
        Parameters
        ----------
        mask : np.ndarray
            Mask array to save.
        file_path : str
            Path to save the mask file.
        format : str, optional
            File format ('auto', 'hdf5', 'npy', 'png', 'txt'), by default 'auto'
        
        Returns
        -------
        bool
            True if saving was successful, False otherwise.
        """
        try:
            # Determine format
            if format == 'auto':
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext in ['.h5', '.hdf5']:
                    format = 'hdf5'
                elif file_ext in ['.npy']:
                    format = 'npy'
                elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.tif']:
                    format = 'png'
                elif file_ext in ['.txt', '.dat']:
                    format = 'txt'
                else:
                    format = 'npy'  # Default format
            
            # Save according to format
            if format == 'hdf5':
                return MaskIO._save_mask_hdf5(mask, file_path)
            elif format == 'npy':
                return MaskIO._save_mask_npy(mask, file_path)
            elif format == 'png':
                return MaskIO._save_mask_image(mask, file_path)
            elif format == 'txt':
                return MaskIO._save_mask_text(mask, file_path)
            else:
                logger.error(f"Unsupported mask save format: {format}")
                return False
                
        except Exception as e:
            logger.error(f"Error saving mask to {file_path}: {e}")
            return False
    
    @staticmethod
    def _load_mask_hdf5(file_path: str) -> Optional[np.ndarray]:
        """Load mask from HDF5 file."""
        try:
            with h5py.File(file_path, 'r') as f:
                # Look for common mask dataset names
                mask_names = ['mask', 'data', 'array']
                for name in mask_names:
                    if name in f:
                        mask = f[name][...]
                        logger.debug(f"Loaded mask from HDF5 dataset '{name}' with shape {mask.shape}")
                        return mask.astype(bool)
                
                # If no common names found, use the first dataset
                datasets = []
                f.visit(lambda name: datasets.append(name) if isinstance(f[name], h5py.Dataset) else None)
                if datasets:
                    mask = f[datasets[0]][...]
                    logger.debug(f"Loaded mask from HDF5 dataset '{datasets[0]}' with shape {mask.shape}")
                    return mask.astype(bool)
                
                logger.error("No datasets found in HDF5 mask file")
                return None
                
        except Exception as e:
            logger.error(f"Error loading HDF5 mask: {e}")
            return None
    
    @staticmethod
    def _save_mask_hdf5(mask: np.ndarray, file_path: str) -> bool:
        """Save mask to HDF5 file."""
        try:
            with h5py.File(file_path, 'w') as f:
                f.create_dataset('mask', data=mask.astype(np.uint8))
                f.attrs['description'] = 'SAXS/XPCS mask file'
                f.attrs['format'] = 'boolean mask (0=masked, 1=valid)'
            logger.debug(f"Saved mask to HDF5 file with shape {mask.shape}")
            return True
        except Exception as e:
            logger.error(f"Error saving HDF5 mask: {e}")
            return False
    
    @staticmethod
    def _load_mask_npy(file_path: str) -> Optional[np.ndarray]:
        """Load mask from NumPy file."""
        try:
            mask = np.load(file_path)
            logger.debug(f"Loaded mask from NumPy file with shape {mask.shape}")
            return mask.astype(bool)
        except Exception as e:
            logger.error(f"Error loading NumPy mask: {e}")
            return None
    
    @staticmethod
    def _save_mask_npy(mask: np.ndarray, file_path: str) -> bool:
        """Save mask to NumPy file."""
        try:
            np.save(file_path, mask.astype(np.uint8))
            logger.debug(f"Saved mask to NumPy file with shape {mask.shape}")
            return True
        except Exception as e:
            logger.error(f"Error saving NumPy mask: {e}")
            return False
    
    @staticmethod
    def _load_mask_image(file_path: str) -> Optional[np.ndarray]:
        """Load mask from image file."""
        try:
            mask = skimage_io.imread(file_path)
            # Convert to boolean (assuming non-zero values are valid pixels)
            if mask.ndim == 3:
                # Convert RGB to grayscale
                mask = np.mean(mask, axis=2)
            mask = mask > 0
            logger.debug(f"Loaded mask from image file with shape {mask.shape}")
            return mask
        except Exception as e:
            logger.error(f"Error loading image mask: {e}")
            return None
    
    @staticmethod
    def _save_mask_image(mask: np.ndarray, file_path: str) -> bool:
        """Save mask to image file."""
        try:
            # Convert boolean mask to 0-255 range
            mask_image = (mask.astype(np.uint8) * 255)
            skimage_io.imsave(file_path, mask_image)
            logger.debug(f"Saved mask to image file with shape {mask.shape}")
            return True
        except Exception as e:
            logger.error(f"Error saving image mask: {e}")
            return False
    
    @staticmethod
    def _load_mask_text(file_path: str) -> Optional[np.ndarray]:
        """Load mask from text file."""
        try:
            mask = np.loadtxt(file_path)
            logger.debug(f"Loaded mask from text file with shape {mask.shape}")
            return mask.astype(bool)
        except Exception as e:
            logger.error(f"Error loading text mask: {e}")
            return None
    
    @staticmethod
    def _save_mask_text(mask: np.ndarray, file_path: str) -> bool:
        """Save mask to text file."""
        try:
            np.savetxt(file_path, mask.astype(np.uint8), fmt='%d')
            logger.debug(f"Saved mask to text file with shape {mask.shape}")
            return True
        except Exception as e:
            logger.error(f"Error saving text mask: {e}")
            return False
    
    @staticmethod
    def create_circular_mask(shape: tuple, center: tuple, radius: float) -> np.ndarray:
        """Create a circular mask.
        
        Parameters
        ----------
        shape : tuple
            Shape of the mask (height, width).
        center : tuple
            Center of the circle (y, x).
        radius : float
            Radius of the circle.
        
        Returns
        -------
        np.ndarray
            Boolean mask array.
        """
        y, x = np.ogrid[:shape[0], :shape[1]]
        mask = (x - center[1])**2 + (y - center[0])**2 <= radius**2
        return mask
    
    @staticmethod
    def create_rectangular_mask(shape: tuple, top_left: tuple, bottom_right: tuple) -> np.ndarray:
        """Create a rectangular mask.
        
        Parameters
        ----------
        shape : tuple
            Shape of the mask (height, width).
        top_left : tuple
            Top-left corner (y, x).
        bottom_right : tuple
            Bottom-right corner (y, x).
        
        Returns
        -------
        np.ndarray
            Boolean mask array.
        """
        mask = np.zeros(shape, dtype=bool)
        y1, x1 = top_left
        y2, x2 = bottom_right
        mask[y1:y2, x1:x2] = True
        return mask

