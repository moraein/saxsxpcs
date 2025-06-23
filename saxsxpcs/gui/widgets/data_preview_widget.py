#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data preview widget for the SAXS-XPCS Analysis Suite.
"""

import logging
import os
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, 
    QSplitter, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from ...utils.logging_config import LoggerMixin

logger = logging.getLogger(__name__)

class DataPreviewWidget(QWidget, LoggerMixin):
    """Widget for previewing SAXS and XPCS data."""
    
    # Signals
    data_changed = pyqtSignal()
    
    def __init__(self, file_importer=None, parent=None):
        """Initialize the data preview widget.
        
        Parameters
        ----------
        file_importer : FileImporter, optional
            File importer instance, by default None
        parent : QWidget, optional
            Parent widget, by default None
        """
        super().__init__(parent)
        
        self.file_importer = file_importer
        self.current_reader = None
        
        self.init_ui()
        self.logger.debug("Data preview widget initialized")
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QHBoxLayout()
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - file list and controls
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # File list
        self.file_list = QListWidget()
        self.file_list.itemSelectionChanged.connect(self.on_file_selected)
        left_layout.addWidget(QLabel("Imported Files:"))
        left_layout.addWidget(self.file_list)
        
        # Plot type selection
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems([
            "2D Pattern", "1D Curve", "Kratky Plot", "Guinier Plot",
            "g2", "Intensity vs Time", "Two-Time Correlation"
        ])
        self.plot_type_combo.currentTextChanged.connect(self.update_plot)
        left_layout.addWidget(QLabel("Plot Type:"))
        left_layout.addWidget(self.plot_type_combo)
        
        # Info label
        self.info_label = QLabel("No data loaded")
        left_layout.addWidget(self.info_label)
        
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(300)
        splitter.addWidget(left_panel)
        
        # Right panel - plot area
        if MATPLOTLIB_AVAILABLE:
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            splitter.addWidget(self.canvas)
        else:
            no_plot_label = QLabel("Matplotlib not available.\nPlease install matplotlib to view plots.")
            no_plot_label.setAlignment(Qt.AlignCenter)
            splitter.addWidget(no_plot_label)
        
        # Set splitter proportions
        splitter.setSizes([300, 800])
        
        layout.addWidget(splitter)
        self.setLayout(layout)
    
    def set_file_importer(self, file_importer):
        """Set the file importer.
        
        Parameters
        ----------
        file_importer : FileImporter
            File importer instance.
        """
        self.file_importer = file_importer
        self.update_file_list()
    
    def update_file_list(self):
        """Update the file list."""
        self.file_list.clear()
        
        if not self.file_importer:
            return
        
        for file_path in self.file_importer.get_file_list():
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)
            self.file_list.addItem(item)
        
        # Select first item if available
        if self.file_list.count() > 0:
            self.file_list.setCurrentRow(0)
    
    def on_file_selected(self):
        """Handle file selection."""
        current_item = self.file_list.currentItem()
        if current_item:
            file_path = current_item.data(Qt.UserRole)
            self.current_reader = self.file_importer.get_reader(file_path)
            self.update_info()
            self.update_plot()
    
    def update_info(self):
        """Update the info label."""
        if not self.current_reader:
            self.info_label.setText("No data loaded")
            return
        
        metadata = self.current_reader.get_metadata()
        beamline = metadata.get('beamline', 'Unknown')
        facility = metadata.get('facility', 'Unknown')
        
        info_text = f"Beamline: {beamline}\nFacility: {facility}"
        
        # Add data shape information
        data = self.current_reader.get_data()
        if data:
            info_text += f"\nData types: {len(data)}"
        
        self.info_label.setText(info_text)
    
    def update_plot(self):
        """Update the plot."""
        if not MATPLOTLIB_AVAILABLE or not self.current_reader:
            return
        
        plot_type = self.plot_type_combo.currentText()
        
        try:
            self.figure.clear()
            
            if plot_type == "2D Pattern":
                self.plot_2d_pattern()
            elif plot_type == "1D Curve":
                self.plot_1d_curve()
            elif plot_type == "Kratky Plot":
                self.plot_kratky()
            elif plot_type == "Guinier Plot":
                self.plot_guinier()
            elif plot_type == "g2":
                self.plot_g2()
            elif plot_type == "Intensity vs Time":
                self.plot_intensity_time()
            elif plot_type == "Two-Time Correlation":
                self.plot_twotime()
            
            self.canvas.draw()
            
        except Exception as e:
            self.logger.error(f"Error updating plot: {e}")
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, f"Error: {str(e)}", 
                   ha='center', va='center', transform=ax.transAxes)
            self.canvas.draw()
    
    def plot_2d_pattern(self):
        """Plot 2D SAXS pattern."""
        saxs_data = self.current_reader.get_saxs_data()
        if saxs_data is None:
            # Try to get detector data
            data = self.current_reader.get_data()
            saxs_data = data.get('detector_data') or data.get('data')
        
        if saxs_data is not None:
            # Take first frame if 3D
            if saxs_data.ndim == 3:
                saxs_data = saxs_data[0]
            
            ax = self.figure.add_subplot(111)
            im = ax.imshow(saxs_data, origin='lower', cmap='viridis')
            ax.set_title("2D SAXS Pattern")
            ax.set_xlabel("Pixel X")
            ax.set_ylabel("Pixel Y")
            self.figure.colorbar(im, ax=ax)
        else:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, "No 2D data available", 
                   ha='center', va='center', transform=ax.transAxes)
    
    def plot_1d_curve(self):
        """Plot 1D SAXS curve."""
        # This is a placeholder - would need actual 1D data or azimuthal averaging
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, "1D curve plotting\nnot yet implemented", 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title("1D SAXS Curve")
    
    def plot_kratky(self):
        """Plot Kratky plot."""
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, "Kratky plot\nnot yet implemented", 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Kratky Plot")
    
    def plot_guinier(self):
        """Plot Guinier plot."""
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, "Guinier plot\nnot yet implemented", 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Guinier Plot")
    
    def plot_g2(self):
        """Plot g2 correlation function."""
        xpcs_data = self.current_reader.get_xpcs_data()
        g2 = xpcs_data.get('g2')
        tau = xpcs_data.get('tau')
        
        if g2 is not None:
            ax = self.figure.add_subplot(111)
            
            if tau is not None and len(tau) == len(g2):
                ax.semilogx(tau, g2, 'o-')
                ax.set_xlabel("Delay Time (s)")
            else:
                ax.plot(g2, 'o-')
                ax.set_xlabel("Delay Index")
            
            ax.set_ylabel("g2")
            ax.set_title("g2 Correlation Function")
            ax.grid(True)
        else:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, "No g2 data available", 
                   ha='center', va='center', transform=ax.transAxes)
    
    def plot_intensity_time(self):
        """Plot intensity vs time."""
        xpcs_data = self.current_reader.get_xpcs_data()
        intensity = xpcs_data.get('intensity')
        
        if intensity is not None:
            ax = self.figure.add_subplot(111)
            ax.plot(intensity)
            ax.set_xlabel("Time Index")
            ax.set_ylabel("Intensity")
            ax.set_title("Intensity vs Time")
            ax.grid(True)
        else:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, "No intensity data available", 
                   ha='center', va='center', transform=ax.transAxes)
    
    def plot_twotime(self):
        """Plot two-time correlation."""
        xpcs_data = self.current_reader.get_xpcs_data()
        twotime = xpcs_data.get('twotime')
        
        if twotime is not None:
            ax = self.figure.add_subplot(111)
            im = ax.imshow(twotime, origin='lower', cmap='viridis')
            ax.set_title("Two-Time Correlation")
            ax.set_xlabel("Time 1")
            ax.set_ylabel("Time 2")
            self.figure.colorbar(im, ax=ax)
        else:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, "No two-time data available", 
                   ha='center', va='center', transform=ax.transAxes)
    
    def zoom_in(self):
        """Zoom in the plot."""
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'canvas'):
            # This is a simplified zoom - matplotlib has built-in zoom tools
            pass
    
    def zoom_out(self):
        """Zoom out the plot."""
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'canvas'):
            # This is a simplified zoom - matplotlib has built-in zoom tools
            pass
    
    def zoom_reset(self):
        """Reset zoom to fit."""
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'canvas'):
            for ax in self.figure.get_axes():
                ax.autoscale()
            self.canvas.draw()

