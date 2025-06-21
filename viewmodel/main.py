from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np

from service.data_buffer import DataBuffer
from service.tcp import TCPService


class MainViewModel(QObject):
    status_changed = pyqtSignal(str)  # Signal to show status
    new_data = pyqtSignal(np.ndarray)  # Signal for new data
    offline_data_ready = pyqtSignal(np.ndarray)  # Signal for offline analysis

    def __init__(self):
        super().__init__()
        self.buffer = DataBuffer()  # Data storage
        # TCP service handles network I/O
        self.tcp_service = None
        self.is_connected = False
        self.visualization_paused = False  # Flag to control visualization updates

    def connect_tcp(self):
        if not self.is_connected:
            self.tcp_service = TCPService(self.buffer, self.on_new_data, self.on_status_change)
            self.tcp_service.start()  # Start TCP thread
            self.is_connected = True
    
    def disconnect_tcp(self):
        if self.is_connected and self.tcp_service:
            self.tcp_service.stop()
            self.is_connected = False
            # Emit offline data for analysis
            all_data = self.buffer.get_all_data()
            if len(all_data) > 0:
                self.offline_data_ready.emit(all_data)

    def on_status_change(self, status):
        if status == "Disconnected":
            self.is_connected = False
        self.status_changed.emit(status)  # Update status label

    def on_new_data(self):
        data = self.buffer.get_latest_chunk()  # Get newest data
        # Only emit new data signal if visualization is not paused
        if not self.visualization_paused:
            self.new_data.emit(data)  # Update plot
    
    def stop_visualization(self):
        """Stop updating the visualization while keeping data collection"""
        self.visualization_paused = True
    
    def resume_visualization(self):
        """Resume updating the visualization"""
        self.visualization_paused = False
        # Emit the latest data to update the plot
        if self.buffer.get_latest_chunk().size > 0:
            self.new_data.emit(self.buffer.get_latest_chunk())
    
    def get_channel_data(self, channel_index):
        """Get all data for a specific channel for offline analysis"""
        return self.buffer.get_channel_data(channel_index)
    
    def clear_data(self):
        """Clear all stored data"""
        self.buffer.clear()
