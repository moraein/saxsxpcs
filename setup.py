#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for the SAXS-XPCS Analysis Suite.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "SAXS and XPCS Analysis Suite"

# Read the requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="saxsxpcs",
    version="0.1.0",
    description="SAXS and XPCS Analysis Suite with GUI for multiple beamlines",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="SAXS-XPCS Team",
    author_email="support@saxsxpcs.org",
    url="https://github.com/saxsxpcs/analysis-suite",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.800',
        ],
        'docs': [
            'sphinx>=3.0',
            'sphinx-rtd-theme>=0.5',
        ],
    },
    entry_points={
        'console_scripts': [
            'saxsxpcs=saxsxpcs.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    keywords='SAXS XPCS analysis beamline DESY ESRF P10 ID02 ID10',
    python_requires='>=3.7',
    zip_safe=False,
)

