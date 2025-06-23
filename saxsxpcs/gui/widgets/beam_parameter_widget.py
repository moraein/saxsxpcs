#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Beam parameter widget for the SAXS-XPCS Analysis Suite.
"""

import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QLineEdit, QPushButton, QDoubleSpinBox, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal

from ...utils.logging_config import LoggerMixin

logger = logging.getLogger(__name__)

class BeamParameterWidget(QWidget, LoggerMixin):
    """Widget for managing beam parameters."""
    
    # Signals
    parameters_updated = pyqtSignal(dict)
    
    def __init__(self, file_importer=None, parent=None):
        """Initialize the beam parameter widget.
        
        Parameters
        ----------
        file_importer : FileImporter, optional
            File importer instance, by default None
        parent : QWidget, optional
            Parent widget, by default None
        """
        super().__init__(parent)
        
        self.file_importer = file_importer
        self.parameters = {}
        
        self.init_ui()
        self.logger.debug("Beam parameter widget initialized")
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()
        
        # Beam parameters group
        beam_group = QGroupBox("Beam Parameters")
        beam_layout = QFormLayout()
        
        # Beam center
        self.beam_center_x_spin = QDoubleSpinBox()
        self.beam_center_x_spin.setRange(0, 10000)
        self.beam_center_x_spin.setValue(500)
        self.beam_center_x_spin.valueChanged.connect(self.on_parameter_changed)
        beam_layout.addRow("Beam Center X:", self.beam_center_x_spin)
        
        self.beam_center_y_spin = QDoubleSpinBox()
        self.beam_center_y_spin.setRange(0, 10000)
        self.beam_center_y_spin.setValue(500)
        self.beam_center_y_spin.valueChanged.connect(self.on_parameter_changed)
        beam_layout.addRow("Beam Center Y:", self.beam_center_y_spin)
        
        # Detector distance
        self.detector_distance_spin = QDoubleSpinBox()
        self.detector_distance_spin.setRange(0.1, 100.0)
        self.detector_distance_spin.setValue(1.0)
        self.detector_distance_spin.setSuffix(" m")
        self.detector_distance_spin.valueChanged.connect(self.on_parameter_changed)
        beam_layout.addRow("Detector Distance:", self.detector_distance_spin)
        
        # Wavelength
        self.wavelength_spin = QDoubleSpinBox()
        self.wavelength_spin.setRange(0.1, 10.0)
        self.wavelength_spin.setValue(1.0)
        self.wavelength_spin.setSuffix(" Å")
        self.wavelength_spin.setDecimals(4)
        self.wavelength_spin.valueChanged.connect(self.on_parameter_changed)
        beam_layout.addRow("Wavelength:", self.wavelength_spin)
        
        # Pixel size
        self.pixel_size_x_spin = QDoubleSpinBox()
        self.pixel_size_x_spin.setRange(1e-6, 1e-3)
        self.pixel_size_x_spin.setValue(75e-6)
        self.pixel_size_x_spin.setSuffix(" m")
        self.pixel_size_x_spin.setDecimals(6)
        self.pixel_size_x_spin.valueChanged.connect(self.on_parameter_changed)
        beam_layout.addRow("Pixel Size X:", self.pixel_size_x_spin)
        
        self.pixel_size_y_spin = QDoubleSpinBox()
        self.pixel_size_y_spin.setRange(1e-6, 1e-3)
        self.pixel_size_y_spin.setValue(75e-6)
        self.pixel_size_y_spin.setSuffix(" m")
        self.pixel_size_y_spin.setDecimals(6)
        self.pixel_size_y_spin.valueChanged.connect(self.on_parameter_changed)
        beam_layout.addRow("Pixel Size Y:", self.pixel_size_y_spin)
        
        beam_group.setLayout(beam_layout)
        layout.addWidget(beam_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("Load from File")
        self.load_btn.clicked.connect(self.load_from_file)
        button_layout.addWidget(self.load_btn)
        
        self.save_btn = QPushButton("Save Parameters")
        self.save_btn.clicked.connect(self.save_parameters)
        button_layout.addWidget(self.save_btn)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_parameters)
        button_layout.addWidget(self.reset_btn)
        
        layout.addLayout(button_layout)
        
        # Info label
        self.info_label = QLabel("Parameters will be applied to data processing.")
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Initialize parameters
        self.update_parameters()
    
    def set_file_importer(self, file_importer):
        """Set the file importer.
        
        Parameters
        ----------
        file_importer : FileImporter
            File importer instance.
        """
        self.file_importer = file_importer
        self.load_from_file()
    
    def on_parameter_changed(self):
        """Handle parameter change."""
        self.update_parameters()
        self.parameters_updated.emit(self.parameters)
    
    def update_parameters(self):
        """Update the parameters dictionary."""
        self.parameters = {
            'beam_center_x': self.beam_center_x_spin.value(),
            'beam_center_y': self.beam_center_y_spin.value(),
            'detector_distance': self.detector_distance_spin.value(),
            'wavelength': self.wavelength_spin.value(),
            'pixel_size_x': self.pixel_size_x_spin.value(),
            'pixel_size_y': self.pixel_size_y_spin.value(),
        }
    
    def load_from_file(self):
        """Load parameters from the current file."""
        if not self.file_importer or len(self.file_importer) == 0:
            return
        
        # Get the first reader
        readers = self.file_importer.get_all_readers()
        if not readers:
            return
        
        reader = list(readers.values())[0]
        metadata = reader.get_metadata()
        
        # Update parameters from metadata
        if 'beam_center_x' in metadata:
            self.beam_center_x_spin.setValue(float(metadata['beam_center_x']))
        
        if 'beam_center_y' in metadata:
            self.beam_center_y_spin.setValue(float(metadata['beam_center_y']))
        
        if 'detector_distance' in metadata:
            self.detector_distance_spin.setValue(float(metadata['detector_distance']))
        
        if 'wavelength' in metadata:
            self.wavelength_spin.setValue(float(metadata['wavelength']))
        
        if 'pixel_size_x' in metadata:
            self.pixel_size_x_spin.setValue(float(metadata['pixel_size_x']))
        
        if 'pixel_size_y' in metadata:
            self.pixel_size_y_spin.setValue(float(metadata['pixel_size_y']))
        
        self.update_parameters()
        self.info_label.setText("Parameters loaded from file metadata.")
        self.logger.info("Parameters loaded from file metadata")
    
    def save_parameters(self):
        """Save parameters to file."""
        # TODO: Implement parameter saving
        self.info_label.setText("Parameter saving not yet implemented.")
    
    def reset_parameters(self):
        """Reset parameters to defaults."""
        self.beam_center_x_spin.setValue(500)
        self.beam_center_y_spin.setValue(500)
        self.detector_distance_spin.setValue(1.0)
        self.wavelength_spin.setValue(1.0)
        self.pixel_size_x_spin.setValue(75e-6)
        self.pixel_size_y_spin.setValue(75e-6)
        
        self.update_parameters()
        self.info_label.setText("Parameters reset to defaults.")
        self.logger.info("Parameters reset to defaults")

