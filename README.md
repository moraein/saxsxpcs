# SAXS and XPCS Analysis Suite

A comprehensive tool for analyzing Small Angle X-ray Scattering (SAXS) and X-ray Photon Correlation Spectroscopy (XPCS) data from various synchrotron beamlines.

## Features

- **Multi-Beamline Support**: Native support for DESY P10, ESRF ID02, and ESRF ID10 beamlines
- **File Format Support**: HDF5 and NeXus file formats
- **GUI Interface**: User-friendly graphical interface with PyQt5
- **Data Visualization**: Interactive plots for SAXS and XPCS data
- **Mask Editor**: Built-in mask creation and editing tools
- **Batch Processing**: Process multiple files simultaneously
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Supported Beamlines

### DESY P10
- Coherence Applications Beamline
- SAXS and XPCS measurements
- Pilatus detectors

### ESRF ID02
- Troika II: Time-resolved and Ultra Small-Angle X-ray Scattering
- SAXS and XPCS measurements
- Eiger detectors

### ESRF ID10
- Surface Diffraction Beamline
- XPCS measurements
- Maxipix detectors

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install from Source

1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install the package:
   ```bash
   pip install -e .
   ```

### Quick Installation

For a quick installation with all dependencies:

```bash
# Create a virtual environment (recommended)
python -m venv saxsxpcs_env
source saxsxpcs_env/bin/activate  # On Windows: saxsxpcs_env\Scripts\activate

# Install the package
pip install -e .
```

## Usage

### GUI Application

Launch the graphical interface:

```bash
saxsxpcs
```

Or run directly with Python:

```bash
python -m saxsxpcs.main
```

### Command Line Options

```bash
saxsxpcs --help
saxsxpcs --debug          # Enable debug logging
saxsxpcs --log-file path  # Specify log file location
```

### Alternative Runner

If the main command doesn't work, use the direct runner:

```bash
python run_saxsxpcs.py
```

## GUI Components

### File Browser
- Navigate and select data files
- Support for batch file selection
- File format detection and validation

### Data Preview
- Visualize SAXS 2D patterns and 1D curves
- Display XPCS correlation functions
- Interactive plotting with zoom and pan
- Multiple plot types: 2D Pattern, 1D Curve, Kratky Plot, Guinier Plot, g2, Intensity vs Time, Two-Time Correlation

### Mask Editor
- Create and edit masks for data processing
- Drawing tools for mask creation
- Load and save mask files
- Real-time mask preview

### Beam Parameters
- Input beam center, detector distance, wavelength
- Load and save parameter sets
- Automatic parameter extraction from files
- Parameter validation

## File Formats

### Supported Input Formats
- HDF5 (.h5, .hdf5)
- NeXus (.nxs, .nx)

### Supported Mask Formats
- HDF5 (.h5, .hdf5)
- NumPy (.npy)
- Images (.png, .jpg, .tiff)
- Text files (.txt, .dat)

## Data Processing

### SAXS Analysis
- Azimuthal averaging
- Background subtraction
- Kratky plots
- Guinier analysis
- Porod analysis

### XPCS Analysis
- G2 correlation function calculation
- Multi-tau algorithm
- Two-time correlation functions
- Intensity time traces
- Fitting capabilities

## Development

### Project Structure

```
saxsxpcs/
├── __init__.py
├── main.py                 # Main entry point
├── config.py              # Configuration settings
├── file_io/               # File I/O modules
│   ├── base_reader.py     # Base reader class
│   ├── hdf5_reader.py     # HDF5 file reader
│   ├── nexus_reader.py    # NeXus file reader
│   ├── mask_io.py         # Mask I/O functionality
│   ├── file_importer.py   # File import factory
│   └── beamlines/         # Beamline-specific readers
│       ├── desy_p10.py    # DESY P10 reader
│       ├── esrf_id02.py   # ESRF ID02 reader
│       └── esrf_id10.py   # ESRF ID10 reader
├── gui/                   # GUI components
│   ├── main_window.py     # Main application window
│   └── widgets/           # GUI widgets
│       ├── file_browser_widget.py
│       ├── data_preview_widget.py
│       ├── mask_editor_widget.py
│       └── beam_parameter_widget.py
└── utils/                 # Utility modules
    └── logging_config.py  # Logging configuration
```

### Adding New Beamlines

To add support for a new beamline:

1. Create a new reader class in `saxsxpcs/file_io/beamlines/`
2. Inherit from `HDF5Reader` or `NeXusReader`
3. Implement beamline-specific data paths and metadata extraction
4. Add the reader to the `READERS` list in `file_importer.py`

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **GUI Not Starting**: Check PyQt5 installation
   ```bash
   pip install PyQt5
   ```

3. **File Not Loading**: Check file format and beamline compatibility

4. **Performance Issues**: For large files, consider using smaller data subsets for testing

### Getting Help

- Check the documentation in the `docs/` directory
- Look at example scripts in the `examples/` directory
- Enable debug logging with `--debug` flag
- Check log files for detailed error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- DESY P10 beamline team
- ESRF ID02 and ID10 beamline teams
- PyQt5 and matplotlib communities
- HDF5 and NeXus format developers

## Citation

If you use this software in your research, please cite:

```
SAXS-XPCS Analysis Suite, Version 0.1.0
https://github.com/saxsxpcs/analysis-suite
```

