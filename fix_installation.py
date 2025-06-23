#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Installation fix script for the SAXS-XPCS Analysis Suite.
This script helps resolve common installation issues.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error during {description}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor}.{version.micro} is not compatible")
        print("  Please use Python 3.7 or higher")
        return False

def check_pip():
    """Check if pip is available."""
    try:
        import pip
        print("✓ pip is available")
        return True
    except ImportError:
        print("✗ pip is not available")
        return False

def install_dependencies():
    """Install required dependencies."""
    dependencies = [
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "h5py>=3.0.0",
        "matplotlib>=3.3.0",
        "PyQt5>=5.15.0",
        "pyqtgraph>=0.12.0",
        "scikit-image>=0.18.0",
        "lmfit>=1.0.0",
        "pandas>=1.3.0",
    ]
    
    print("\nInstalling dependencies...")
    for dep in dependencies:
        success = run_command(f"pip install {dep}", f"Installing {dep}")
        if not success:
            print(f"Warning: Failed to install {dep}")
    
    return True

def install_package():
    """Install the SAXS-XPCS package."""
    if os.path.exists("setup.py"):
        return run_command("pip install -e .", "Installing SAXS-XPCS package")
    else:
        print("✗ setup.py not found. Please run this script from the project directory.")
        return False

def test_installation():
    """Test if the installation works."""
    try:
        import saxsxpcs
        print("✓ SAXS-XPCS package can be imported")
        return True
    except ImportError as e:
        print(f"✗ Failed to import SAXS-XPCS package: {e}")
        return False

def create_runner_script():
    """Create a runner script as fallback."""
    runner_content = '''#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from saxsxpcs.main import main
if __name__ == "__main__":
    sys.exit(main())
'''
    
    try:
        with open("run_saxsxpcs_fixed.py", "w") as f:
            f.write(runner_content)
        print("✓ Created fallback runner script: run_saxsxpcs_fixed.py")
        return True
    except Exception as e:
        print(f"✗ Failed to create runner script: {e}")
        return False

def main():
    """Main installation fix function."""
    print("SAXS-XPCS Analysis Suite - Installation Fix")
    print("=" * 50)
    
    # Check system requirements
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Install dependencies
    install_dependencies()
    
    # Install package
    install_success = install_package()
    
    # Test installation
    test_success = test_installation()
    
    if not test_success:
        print("\nPackage installation failed. Creating fallback runner...")
        create_runner_script()
    
    print("\n" + "=" * 50)
    print("Installation Fix Summary:")
    print(f"  Package installation: {'✓' if install_success else '✗'}")
    print(f"  Import test: {'✓' if test_success else '✗'}")
    
    if test_success:
        print("\n✓ Installation successful! You can now run:")
        print("  saxsxpcs")
        print("  or")
        print("  python -m saxsxpcs.main")
    else:
        print("\n⚠ Installation had issues. Try running:")
        print("  python run_saxsxpcs.py")
        print("  or")
        print("  python run_saxsxpcs_fixed.py")
    
    return test_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

