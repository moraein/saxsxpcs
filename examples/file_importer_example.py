#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example script demonstrating the SAXS-XPCS file importer usage.
"""

import os
import sys
import numpy as np

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from saxsxpcs.file_io import FileImporter

def main():
    """Main example function."""
    print("SAXS-XPCS File Importer Example")
    print("=" * 40)
    
    # Create file importer
    importer = FileImporter()
    
    # Example file paths (replace with actual file paths)
    example_files = [
        # Add your actual file paths here
        # "/path/to/desy_p10_file.h5",
        # "/path/to/esrf_id02_file.nxs",
        # "/path/to/esrf_id10_file.h5",
    ]
    
    if not example_files:
        print("No example files specified.")
        print("Please edit this script and add actual file paths to the example_files list.")
        return
    
    # Check if files exist
    existing_files = [f for f in example_files if os.path.exists(f)]
    
    if not existing_files:
        print("No existing files found.")
        print("Please check the file paths in the example_files list.")
        return
    
    print(f"Found {len(existing_files)} files to import:")
    for file_path in existing_files:
        print(f"  - {file_path}")
    
    # Import files
    print("\nImporting files...")
    readers = importer.import_files(existing_files)
    
    if not readers:
        print("Failed to import any files.")
        return
    
    print(f"Successfully imported {len(readers)} files.")
    
    # Analyze each file
    for file_path, reader in readers.items():
        print(f"\nAnalyzing: {os.path.basename(file_path)}")
        print("-" * 40)
        
        # Get file info
        file_info = reader.get_file_info()
        print(f"File size: {file_info.get('size', 'Unknown')} bytes")
        
        # Get metadata
        metadata = reader.get_metadata()
        print(f"Beamline: {metadata.get('beamline', 'Unknown')}")
        print(f"Facility: {metadata.get('facility', 'Unknown')}")
        
        if 'beam_center_x' in metadata:
            print(f"Beam center: ({metadata['beam_center_x']}, {metadata['beam_center_y']})")
        
        if 'detector_distance' in metadata:
            print(f"Detector distance: {metadata['detector_distance']} m")
        
        if 'wavelength' in metadata:
            print(f"Wavelength: {metadata['wavelength']} Å")
        
        # Get data
        data = reader.get_data()
        print(f"Available data types: {list(data.keys())}")
        
        for data_type, data_array in data.items():
            if hasattr(data_array, 'shape'):
                print(f"  {data_type}: shape {data_array.shape}, dtype {data_array.dtype}")
        
        # Try to get SAXS data
        saxs_data = reader.get_saxs_data()
        if saxs_data is not None:
            print(f"SAXS data: shape {saxs_data.shape}")
        
        # Try to get XPCS data
        xpcs_data = reader.get_xpcs_data()
        if xpcs_data:
            print(f"XPCS data types: {list(xpcs_data.keys())}")
            for xpcs_type, xpcs_array in xpcs_data.items():
                if hasattr(xpcs_array, 'shape'):
                    print(f"  {xpcs_type}: shape {xpcs_array.shape}")
        
        # Try to get Q-map
        q_map = reader.get_q_map()
        if q_map is not None:
            print(f"Q-map: shape {q_map.shape}")
        
        # Try to get mask
        mask = reader.get_mask()
        if mask is not None:
            print(f"Mask: shape {mask.shape}")
    
    # Get summary
    print("\nSummary:")
    print("-" * 40)
    summary = importer.get_data_summary()
    print(f"Total files imported: {summary['total_files']}")
    
    for file_path, file_summary in summary['files'].items():
        print(f"\n{os.path.basename(file_path)}:")
        print(f"  Beamline: {file_summary['beamline']}")
        print(f"  Data types: {file_summary['data_types']}")
    
    # Clean up
    importer.clear()
    print("\nExample completed.")

if __name__ == "__main__":
    main()

