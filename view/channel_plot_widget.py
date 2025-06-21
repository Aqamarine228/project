from PyQt5.QtWidgets import QWidget, QVBoxLayout
from vispy import scene
from vispy.scene import Line
import numpy as np
from scipy import signal

class ChannelPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)  # Create canvas
        self.view = self.canvas.central_widget.add_view()
        
        # Initialize with empty data
        self.data_history = np.zeros(1000)  # Store last 1000 samples
        self.raw_data_history = np.zeros(1000)  # Store raw unfiltered data
        # Create initial line data with proper 2D format for VisPy
        initial_pos = np.column_stack((np.arange(1000), self.data_history))
        self.line = Line(pos=initial_pos, parent=self.view.scene, color='blue', width=2)
        
        # Set up the view
        self.view.camera = 'panzoom'
        self.view.camera.set_range(x=(0, 1000), y=(-1, 1))
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas.native)
        self.setLayout(layout)

        self.channel_index = 0  # Default to channel 0
        self.sample_count = 0
        self.signal_type = "unfiltered"  # Default signal type
        
        # Filter parameters
        self.fs = 1000  # Sampling frequency (Hz)
        self.lowcut = 1.0  # Low cutoff frequency
        self.highcut = 100.0  # High cutoff frequency
        self.filter_order = 4
        
        # RMS window size
        self.rms_window = 50

    def set_channel(self, index):
        self.channel_index = index  # Set active channel
        # Reset data history when changing channels
        self.data_history = np.zeros(1000)
        self.raw_data_history = np.zeros(1000)
        self.sample_count = 0
        
        # Update the plot immediately to clear old channel data
        x_data = np.arange(len(self.data_history))
        self.line.set_data(pos=np.column_stack((x_data, self.data_history)))
        self.view.camera.set_range(x=(0, 1000), y=(-1, 1))
        self.canvas.update()
    
    def clear_plot_data(self):
        """Clear all plot data and reset the display"""
        self.data_history = np.zeros(1000)
        self.raw_data_history = np.zeros(1000)
        self.sample_count = 0
        
        # Update the plot to show cleared data
        x_data = np.arange(len(self.data_history))
        self.line.set_data(pos=np.column_stack((x_data, self.data_history)))
        self.view.camera.set_range(x=(0, 1000), y=(-1, 1))
        self.canvas.update()
    
    def set_signal_type(self, signal_type):
        """Set the signal processing type: 'unfiltered', 'filtered', or 'rms'"""
        self.signal_type = signal_type
        # Reprocess existing data with new signal type
        self._reprocess_data()
    
    def _apply_bandpass_filter(self, data):
        """Apply bandpass filter to the data"""
        if len(data) < 2 * self.filter_order:
            return data  # Not enough data for filtering
        
        try:
            nyquist = 0.5 * self.fs
            low = self.lowcut / nyquist
            high = self.highcut / nyquist
            b, a = signal.butter(self.filter_order, [low, high], btype='band')
            return signal.filtfilt(b, a, data)
        except:
            return data  # Return original data if filtering fails
    
    def _calculate_rms(self, data):
        """Calculate RMS values using a sliding window"""
        if len(data) < self.rms_window:
            return np.sqrt(np.mean(data**2)) * np.ones_like(data)
        
        rms_values = np.zeros_like(data)
        for i in range(len(data)):
            start_idx = max(0, i - self.rms_window // 2)
            end_idx = min(len(data), i + self.rms_window // 2 + 1)
            rms_values[i] = np.sqrt(np.mean(data[start_idx:end_idx]**2))
        return rms_values
    
    def _reprocess_data(self):
        """Reprocess existing raw data with current signal type"""
        if self.signal_type == "unfiltered":
            self.data_history = self.raw_data_history.copy()
        elif self.signal_type == "filtered":
            self.data_history = self._apply_bandpass_filter(self.raw_data_history)
        elif self.signal_type == "rms":
            self.data_history = self._calculate_rms(self.raw_data_history)
        
        # Update the plot
        x_data = np.arange(len(self.data_history))
        self.line.set_data(pos=np.column_stack((x_data, self.data_history)))
        self._update_camera_range()

    def update_plot(self, data):
        if data.shape[0] > self.channel_index:
            # Get new samples for the selected channel
            new_samples = data[self.channel_index]  # 18 new samples
            
            # Shift existing raw data and add new samples
            self.raw_data_history[:-len(new_samples)] = self.raw_data_history[len(new_samples):]
            self.raw_data_history[-len(new_samples):] = new_samples
            
            # Process data based on signal type
            if self.signal_type == "unfiltered":
                processed_samples = new_samples
                # Shift existing data and add new samples
                self.data_history[:-len(new_samples)] = self.data_history[len(new_samples):]
                self.data_history[-len(new_samples):] = processed_samples
            elif self.signal_type == "filtered":
                # Apply filter to entire history for better results
                self.data_history = self._apply_bandpass_filter(self.raw_data_history)
            elif self.signal_type == "rms":
                # Calculate RMS for entire history
                self.data_history = self._calculate_rms(self.raw_data_history)
            
            # Update the line
            x_data = np.arange(len(self.data_history))
            self.line.set_data(pos=np.column_stack((x_data, self.data_history)))
            
            # Auto-scale Y axis
            self._update_camera_range()
            
            self.sample_count += len(new_samples)
    
    def _update_camera_range(self):
        """Update camera range based on current data"""
        if np.any(self.data_history != 0):
            y_min, y_max = np.min(self.data_history), np.max(self.data_history)
            y_range = y_max - y_min
            if y_range > 0:
                margin = y_range * 0.1
                self.view.camera.set_range(y=(y_min - margin, y_max + margin))