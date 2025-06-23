#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File browser widget for the SAXS-XPCS Analysis Suite.
"""

import os
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, 
    QListWidgetItem, QFileDialog, QLabel, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

from ...utils.logging_config import LoggerMixin

logger = logging.getLogger(__name__)

class FileBrowserWidget(QWidget, LoggerMixin):
    """Widget for browsing and selecting files."""
    
    # Signals
    files_selected = pyqtSignal(list)
    files_imported = pyqtSignal(list)
    
    def __init__(self, parent=None):
        """Initialize the file browser widget.
        
        Parameters
        ----------
        parent : QWidget, optional
            Parent widget, by default None
        """
        super().__init__(parent)
        
        self.current_directory = os.path.expanduser("~")
        self.file_importer = None
        
        self.init_ui()
        self.logger.debug("File browser widget initialized")
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout()
        
        # Directory selection
        dir_layout = QHBoxLayout()
        
        self.dir_label = QLabel("Directory:")
        dir_layout.addWidget(self.dir_label)
        
        self.dir_edit = QLineEdit(self.current_directory)
        self.dir_edit.setReadOnly(True)
        dir_layout.addWidget(self.dir_edit)
        
        self.browse_dir_btn = QPushButton("Browse...")
        self.browse_dir_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_dir_btn)
        
        layout.addLayout(dir_layout)
        
        # File list
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.file_list.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.file_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_file_list)
        button_layout.addWidget(self.refresh_btn)
        
        self.import_btn = QPushButton("Import Selected")
        self.import_btn.clicked.connect(self.import_selected_files)
        self.import_btn.setEnabled(False)
        button_layout.addWidget(self.import_btn)
        
        self.import_all_btn = QPushButton("Import All")
        self.import_all_btn.clicked.connect(self.import_all_files)
        button_layout.addWidget(self.import_all_btn)
        
        layout.addLayout(button_layout)
        
        # Info label
        self.info_label = QLabel("No files selected")
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
        
        # Load initial file list
        self.refresh_file_list()
    
    def set_file_importer(self, file_importer):
        """Set the file importer.
        
        Parameters
        ----------
        file_importer : FileImporter
            File importer instance.
        """
        self.file_importer = file_importer
        self.update_info_label()
    
    def set_directory(self, directory):
        """Set the current directory.
        
        Parameters
        ----------
        directory : str
            Directory path.
        """
        if os.path.exists(directory):
            self.current_directory = directory
            self.dir_edit.setText(directory)
            self.refresh_file_list()
    
    def get_current_directory(self):
        """Get the current directory.
        
        Returns
        -------
        str
            Current directory path.
        """
        return self.current_directory
    
    def browse_directory(self):
        """Browse for a directory."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", self.current_directory
        )
        
        if directory:
            self.set_directory(directory)
    
    def refresh_file_list(self):
        """Refresh the file list."""
        self.file_list.clear()
        
        if not os.path.exists(self.current_directory):
            return
        
        # Supported file extensions
        supported_extensions = ['.h5', '.hdf5', '.nxs', '.nx']
        
        try:
            files = os.listdir(self.current_directory)
            data_files = []
            
            for file in files:
                if any(file.lower().endswith(ext) for ext in supported_extensions):
                    data_files.append(file)
            
            # Sort files
            data_files.sort()
            
            # Add files to list
            for file in data_files:
                item = QListWidgetItem(file)
                item.setData(Qt.UserRole, os.path.join(self.current_directory, file))
                self.file_list.addItem(item)
            
            self.update_info_label()
            self.logger.debug(f"Found {len(data_files)} data files in {self.current_directory}")
            
        except Exception as e:
            self.logger.error(f"Error reading directory {self.current_directory}: {e}")
            QMessageBox.warning(
                self, "Directory Error", 
                f"Error reading directory:\n{str(e)}"
            )
    
    def get_selected_files(self):
        """Get selected file paths.
        
        Returns
        -------
        list
            List of selected file paths.
        """
        selected_items = self.file_list.selectedItems()
        return [item.data(Qt.UserRole) for item in selected_items]
    
    def get_all_files(self):
        """Get all file paths in the list.
        
        Returns
        -------
        list
            List of all file paths.
        """
        all_files = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            all_files.append(item.data(Qt.UserRole))
        return all_files
    
    def import_selected_files(self):
        """Import selected files."""
        selected_files = self.get_selected_files()
        if selected_files:
            self.files_imported.emit(selected_files)
    
    def import_all_files(self):
        """Import all files."""
        all_files = self.get_all_files()
        if all_files:
            self.files_imported.emit(all_files)
    
    def on_selection_changed(self):
        """Handle selection change."""
        selected_files = self.get_selected_files()
        self.import_btn.setEnabled(len(selected_files) > 0)
        self.files_selected.emit(selected_files)
        self.update_info_label()
    
    def update_info_label(self):
        """Update the info label."""
        total_files = self.file_list.count()
        selected_files = len(self.get_selected_files())
        
        info_text = f"Total files: {total_files}"
        if selected_files > 0:
            info_text += f", Selected: {selected_files}"
        
        if self.file_importer:
            imported_files = len(self.file_importer)
            info_text += f", Imported: {imported_files}"
        
        self.info_label.setText(info_text)

