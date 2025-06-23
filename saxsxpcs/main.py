#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the SAXS-XPCS Analysis Suite.
"""

import os
import sys
import logging
import argparse
from PyQt5.QtWidgets import QApplication

from .gui import MainWindow
from .utils.logging_config import setup_logging

def main():
    """Main entry point for the SAXS-XPCS Analysis Suite."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='SAXS-XPCS Analysis Suite')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--log-file', type=str, help='Log file path')
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(debug=args.debug, log_file=args.log_file)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting SAXS-XPCS Analysis Suite")
    
    try:
        # Create the application
        app = QApplication(sys.argv)
        app.setApplicationName("SAXS-XPCS Analysis Suite")
        app.setOrganizationName("SAXS-XPCS")
        app.setApplicationVersion("0.1.0")
        
        # Create the main window
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

