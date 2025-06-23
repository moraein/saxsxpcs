#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main window for the SAXS-XPCS Analysis Suite.
"""

import os
import sys
import logging
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QAction,
    QMenu, QToolBar, QStatusBar, QFileDialog, QMessageBox, QDockWidget,
    QApplication, QSplitter
)
from PyQt5.QtCore import Qt, QSettings, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence

from .widgets import (
    FileBrowserWidget, DataPreviewWidget, MaskEditorWidget, BeamParameterWidget
)
from ..file_io import FileImporter
from ..utils.logging_config import LoggerMixin

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow, LoggerMixin):
    """Main window for the SAXS-XPCS Analysis Suite."""
    
    # Signals
    file_imported = pyqtSignal(str)
    files_imported = pyqtSignal(list)
    
    def __init__(self, parent=None):
        """Initialize the main window.
        
        Parameters
        ----------
        parent : QWidget, optional
            Parent widget, by default None
        """
        super().__init__(parent)
        
        # Initialize the file importer
        self.file_importer = FileImporter()
        
        # Initialize the UI
        self.init_ui()
        
        # Connect signals
        self.connect_signals()
        
        # Load settings
        self.load_settings()
        
        self.logger.info("Main window initialized")
    
    def init_ui(self):
        """Initialize the UI."""
        # Set the window title and icon
        self.setWindowTitle("SAXS-XPCS Analysis Suite")
        self.setMinimumSize(800, 600)
        self.resize(1200, 800)
        
        # Create the central widget with tabs
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create the data preview widget
        self.data_preview_widget = DataPreviewWidget(self.file_importer)
        self.central_widget.addTab(self.data_preview_widget, "Data Preview")
        
        # Create the mask editor widget
        self.mask_editor_widget = MaskEditorWidget(self.file_importer)
        self.central_widget.addTab(self.mask_editor_widget, "Mask Editor")
        
        # Create dock widgets
        self.create_dock_widgets()
        
        # Create the menu bar
        self.create_menu_bar()
        
        # Create the tool bar
        self.create_tool_bar()
        
        # Create the status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        self.logger.debug("UI initialized")
    
    def create_dock_widgets(self):
        """Create dock widgets."""
        # File browser dock widget
        self.file_browser_dock = QDockWidget("File Browser", self)
        self.file_browser_dock.setObjectName("FileBrowserDock")
        self.file_browser_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.file_browser_dock.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable
        )
        
        self.file_browser_widget = FileBrowserWidget()
        self.file_browser_dock.setWidget(self.file_browser_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.file_browser_dock)
        
        # Beam parameter dock widget
        self.beam_parameter_dock = QDockWidget("Beam Parameters", self)
        self.beam_parameter_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.beam_parameter_dock.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable
        )
        
        self.beam_parameter_widget = BeamParameterWidget(self.file_importer)
        self.beam_parameter_dock.setWidget(self.beam_parameter_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.beam_parameter_dock)
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Open action
        self.open_action = QAction("&Open Files...", self)
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.setStatusTip("Open data files")
        self.open_action.triggered.connect(self.open_files)
        file_menu.addAction(self.open_action)
        
        # Open directory action
        self.open_dir_action = QAction("Open &Directory...", self)
        self.open_dir_action.setShortcut("Ctrl+Shift+O")
        self.open_dir_action.setStatusTip("Open all files in a directory")
        self.open_dir_action.triggered.connect(self.open_directory)
        file_menu.addAction(self.open_dir_action)
        
        file_menu.addSeparator()
        
        # Save action
        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.setStatusTip("Save current data")
        self.save_action.triggered.connect(self.save_data)
        self.save_action.setEnabled(False)  # Enable when data is loaded
        file_menu.addAction(self.save_action)
        
        # Export action
        self.export_action = QAction("&Export...", self)
        self.export_action.setShortcut("Ctrl+E")
        self.export_action.setStatusTip("Export data or plots")
        self.export_action.triggered.connect(self.export_data)
        self.export_action.setEnabled(False)  # Enable when data is loaded
        file_menu.addAction(self.export_action)
        
        file_menu.addSeparator()
        
        # Exit action
        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut(QKeySequence.Quit)
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)
        file_menu.addAction(self.exit_action)
        
        # View menu
        view_menu = menu_bar.addMenu("&View")
        
        # Dock widget toggles
        view_menu.addAction(self.file_browser_dock.toggleViewAction())
        view_menu.addAction(self.beam_parameter_dock.toggleViewAction())
        
        view_menu.addSeparator()
        
        # Zoom actions
        self.zoom_in_action = QAction("Zoom &In", self)
        self.zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        self.zoom_in_action.setStatusTip("Zoom in")
        self.zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(self.zoom_in_action)
        
        self.zoom_out_action = QAction("Zoom &Out", self)
        self.zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        self.zoom_out_action.setStatusTip("Zoom out")
        self.zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(self.zoom_out_action)
        
        self.zoom_reset_action = QAction("&Reset Zoom", self)
        self.zoom_reset_action.setShortcut("Ctrl+0")
        self.zoom_reset_action.setStatusTip("Reset zoom to fit")
        self.zoom_reset_action.triggered.connect(self.zoom_reset)
        view_menu.addAction(self.zoom_reset_action)
        
        # Tools menu
        tools_menu = menu_bar.addMenu("&Tools")
        
        # Mask editor action
        self.mask_editor_action = QAction("&Mask Editor", self)
        self.mask_editor_action.setShortcut("Ctrl+M")
        self.mask_editor_action.setStatusTip("Open the mask editor")
        self.mask_editor_action.triggered.connect(self.show_mask_editor)
        tools_menu.addAction(self.mask_editor_action)
        
        # Data processing action
        self.process_action = QAction("&Process Data", self)
        self.process_action.setShortcut("Ctrl+P")
        self.process_action.setStatusTip("Process loaded data")
        self.process_action.triggered.connect(self.process_data)
        self.process_action.setEnabled(False)  # Enable when data is loaded
        tools_menu.addAction(self.process_action)
        
        # Settings action
        self.settings_action = QAction("&Settings...", self)
        self.settings_action.setStatusTip("Open application settings")
        self.settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(self.settings_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        
        # About action
        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip("About this application")
        self.about_action.triggered.connect(self.show_about)
        help_menu.addAction(self.about_action)
        
        # Documentation action
        self.docs_action = QAction("&Documentation", self)
        self.docs_action.setShortcut("F1")
        self.docs_action.setStatusTip("Open documentation")
        self.docs_action.triggered.connect(self.show_documentation)
        help_menu.addAction(self.docs_action)
    
    def create_tool_bar(self):
        """Create the tool bar."""
        self.tool_bar = QToolBar("Main Toolbar")
        self.addToolBar(self.tool_bar)
        
        # Add actions to toolbar
        self.tool_bar.addAction(self.open_action)
        self.tool_bar.addAction(self.save_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.mask_editor_action)
        self.tool_bar.addAction(self.process_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.zoom_in_action)
        self.tool_bar.addAction(self.zoom_out_action)
        self.tool_bar.addAction(self.zoom_reset_action)
    
    def connect_signals(self):
        """Connect signals and slots."""
        # File browser signals
        self.file_browser_widget.files_selected.connect(self.on_files_selected)
        self.file_browser_widget.files_imported.connect(self.on_files_imported)
        
        # Data preview signals
        self.data_preview_widget.data_changed.connect(self.on_data_changed)
        
        # Mask editor signals
        self.mask_editor_widget.mask_updated.connect(self.on_mask_updated)
        
        # Beam parameter signals
        self.beam_parameter_widget.parameters_updated.connect(self.on_parameters_updated)
        
        # Tab change signal
        self.central_widget.currentChanged.connect(self.on_tab_changed)
    
    def open_files(self):
        """Open files dialog."""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Data Files (*.h5 *.hdf5 *.nxs *.nx);;All Files (*)")
        file_dialog.setDirectory(os.path.expanduser("~"))
        
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.import_files(file_paths)
    
    def open_directory(self):
        """Open directory dialog."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", os.path.expanduser("~")
        )
        
        if directory:
            # Find all supported files in the directory
            supported_extensions = ['.h5', '.hdf5', '.nxs', '.nx']
            file_paths = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in supported_extensions):
                        file_paths.append(os.path.join(root, file))
            
            if file_paths:
                self.import_files(file_paths)
            else:
                QMessageBox.information(
                    self, "No Files Found", 
                    f"No supported data files found in {directory}"
                )
    
    def import_files(self, file_paths):
        """Import files using the file importer.
        
        Parameters
        ----------
        file_paths : list
            List of file paths to import.
        """
        if not file_paths:
            return
        
        self.status_bar.showMessage("Importing files...")
        
        try:
            # Import files
            readers = self.file_importer.import_files(file_paths)
            
            if readers:
                # Update widgets
                self.update_widgets()
                
                # Enable actions
                self.save_action.setEnabled(True)
                self.export_action.setEnabled(True)
                self.process_action.setEnabled(True)
                
                # Emit signal
                self.files_imported.emit(list(readers.keys()))
                
                # Update status
                self.status_bar.showMessage(
                    f"Successfully imported {len(readers)} files", 5000
                )
                
                self.logger.info(f"Imported {len(readers)} files")
            else:
                QMessageBox.warning(
                    self, "Import Failed", 
                    "Failed to import any files. Please check the file formats."
                )
                self.status_bar.showMessage("Import failed", 5000)
        
        except Exception as e:
            self.logger.error(f"Error importing files: {e}")
            QMessageBox.critical(
                self, "Import Error", 
                f"An error occurred while importing files:\n{str(e)}"
            )
            self.status_bar.showMessage("Import error", 5000)
    
    def save_data(self):
        """Save current data."""
        # TODO: Implement data saving
        QMessageBox.information(
            self, "Save Data", 
            "Data saving functionality will be implemented in a future version."
        )
    
    def export_data(self):
        """Export data or plots."""
        # TODO: Implement data export
        QMessageBox.information(
            self, "Export Data", 
            "Data export functionality will be implemented in a future version."
        )
    
    def zoom_in(self):
        """Zoom in current view."""
        current_widget = self.central_widget.currentWidget()
        if hasattr(current_widget, 'zoom_in'):
            current_widget.zoom_in()
    
    def zoom_out(self):
        """Zoom out current view."""
        current_widget = self.central_widget.currentWidget()
        if hasattr(current_widget, 'zoom_out'):
            current_widget.zoom_out()
    
    def zoom_reset(self):
        """Reset zoom to fit."""
        current_widget = self.central_widget.currentWidget()
        if hasattr(current_widget, 'zoom_reset'):
            current_widget.zoom_reset()
    
    def show_mask_editor(self):
        """Show the mask editor tab."""
        self.central_widget.setCurrentWidget(self.mask_editor_widget)
    
    def process_data(self):
        """Process loaded data."""
        # TODO: Implement data processing
        QMessageBox.information(
            self, "Process Data", 
            "Data processing functionality will be implemented in a future version."
        )
    
    def show_settings(self):
        """Show application settings."""
        # TODO: Implement settings dialog
        QMessageBox.information(
            self, "Settings", 
            "Settings dialog will be implemented in a future version."
        )
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About SAXS-XPCS Analysis Suite",
            "<h3>SAXS-XPCS Analysis Suite</h3>"
            "<p>Version 0.1.0</p>"
            "<p>A comprehensive tool for analyzing SAXS and XPCS data from various beamlines.</p>"
            "<p><b>Supported Beamlines:</b></p>"
            "<ul>"
            "<li>DESY P10</li>"
            "<li>ESRF ID02</li>"
            "<li>ESRF ID10</li>"
            "</ul>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>HDF5 and NeXus file support</li>"
            "<li>Interactive data visualization</li>"
            "<li>Mask editor</li>"
            "<li>Beam parameter management</li>"
            "</ul>"
            "<p>© 2024 SAXS-XPCS Team</p>"
        )
    
    def show_documentation(self):
        """Show documentation."""
        # TODO: Implement documentation viewer
        QMessageBox.information(
            self, "Documentation", 
            "Documentation will be available in a future version.\n\n"
            "For now, please refer to the README.md file in the project directory."
        )
    
    def update_widgets(self):
        """Update all widgets with current data."""
        # Update file browser
        self.file_browser_widget.set_file_importer(self.file_importer)
        
        # Update data preview
        self.data_preview_widget.set_file_importer(self.file_importer)
        
        # Update mask editor
        self.mask_editor_widget.set_file_importer(self.file_importer)
        
        # Update beam parameter widget
        self.beam_parameter_widget.set_file_importer(self.file_importer)
    
    def on_files_selected(self, file_paths):
        """Handle file selection from file browser.
        
        Parameters
        ----------
        file_paths : list
            List of selected file paths.
        """
        self.logger.debug(f"Files selected: {file_paths}")
    
    def on_files_imported(self, file_paths):
        """Handle files imported from file browser.
        
        Parameters
        ----------
        file_paths : list
            List of imported file paths.
        """
        self.import_files(file_paths)
    
    def on_data_changed(self):
        """Handle data change in preview widget."""
        self.logger.debug("Data changed in preview widget")
    
    def on_mask_updated(self, mask):
        """Handle mask update from mask editor.
        
        Parameters
        ----------
        mask : np.ndarray
            Updated mask array.
        """
        self.logger.debug("Mask updated")
        # TODO: Apply mask to data processing
    
    def on_parameters_updated(self, parameters):
        """Handle parameter update from beam parameter widget.
        
        Parameters
        ----------
        parameters : dict
            Updated parameters.
        """
        self.logger.debug(f"Parameters updated: {parameters}")
        # TODO: Apply parameters to data processing
    
    def on_tab_changed(self, index):
        """Handle tab change.
        
        Parameters
        ----------
        index : int
            Index of the current tab.
        """
        tab_names = ["Data Preview", "Mask Editor"]
        if 0 <= index < len(tab_names):
            self.logger.debug(f"Switched to tab: {tab_names[index]}")
    
    def load_settings(self):
        """Load application settings."""
        settings = QSettings("SAXS-XPCS", "Analysis Suite")
        
        # Load window geometry
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Load window state (dock positions, etc.)
        state = settings.value("windowState")
        if state:
            self.restoreState(state)
        
        # Load last directory
        last_dir = settings.value("lastDirectory", os.path.expanduser("~"))
        if os.path.exists(last_dir):
            self.file_browser_widget.set_directory(last_dir)
    
    def save_settings(self):
        """Save application settings."""
        settings = QSettings("SAXS-XPCS", "Analysis Suite")
        
        # Save window geometry
        settings.setValue("geometry", self.saveGeometry())
        
        # Save window state
        settings.setValue("windowState", self.saveState())
        
        # Save current directory
        current_dir = self.file_browser_widget.get_current_directory()
        if current_dir:
            settings.setValue("lastDirectory", current_dir)
    
    def closeEvent(self, event):
        """Handle close event.
        
        Parameters
        ----------
        event : QCloseEvent
            Close event.
        """
        # Save settings
        self.save_settings()
        
        # Close file readers
        self.file_importer.clear()
        
        # Accept the event
        event.accept()
        
        self.logger.info("Application closed")

