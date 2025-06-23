#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Direct runner script for the SAXS-XPCS Analysis Suite.
This script can be used to run the application without installing it.
"""

import sys
import os

# Add the package directory to the Python path
package_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, package_dir)

try:
    from saxsxpcs.main import main
    
    if __name__ == "__main__":
        print("Starting SAXS-XPCS Analysis Suite...")
        sys.exit(main())
        
except ImportError as e:
    print(f"Error importing saxsxpcs package: {e}")
    print("\nThis is likely due to missing dependencies.")
    print("Please install the required packages:")
    print("  pip install -r requirements.txt")
    print("\nOr install the package:")
    print("  pip install -e .")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)

