import logging

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from scipy import signal

from config import SAMPLING_FREQUENCY, LOW_CUTOFF_FREQUENCY, HIGH_CUTOFF_FREQUENCY, FILTER_ORDER, RMS_WINDOW


class OfflineAnalysisWidget(QWidget):
    def __init__(self, get_data_callback):
        super().__init__()
        self.setWindowTitle("Offline Signal Analysis")
        self.setGeometry(200, 200, 1200, 800)
        
        # Filter parameters (same as in channel_plot_widget)
        self.fs = SAMPLING_FREQUENCY  # Sampling frequency (Hz)
        self.lowcut = LOW_CUTOFF_FREQUENCY  # Low cutoff frequency
        self.highcut = HIGH_CUTOFF_FREQUENCY  # High cutoff frequency
        self.filter_order = FILTER_ORDER
        self.rms_window = RMS_WINDOW# RMS window size
        
        self.init_ui()

        self.get_data_callback = get_data_callback

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Control panel
        control_layout = QHBoxLayout()
        
        # Channel selector
        control_layout.addWidget(QLabel("Channel:"))
        self.channel_selector = QComboBox()
        self.channel_selector.addItems([f"Channel {i}" for i in range(32)])
        self.channel_selector.currentIndexChanged.connect(self.plot)
        control_layout.addWidget(self.channel_selector)
        
        # Signal type selector
        control_layout.addWidget(QLabel("Signal Type:"))
        self.signal_type_selector = QComboBox()
        self.signal_type_selector.addItems(["Unfiltered", "Filtered", "RMS"])
        self.signal_type_selector.currentIndexChanged.connect(self.plot)
        control_layout.addWidget(self.signal_type_selector)
        
        # View mode selector
        control_layout.addWidget(QLabel("View Mode:"))
        self.view_mode_selector = QComboBox()
        self.view_mode_selector.addItems(["Complete Signal", "Signal Statistics"])
        self.view_mode_selector.currentIndexChanged.connect(self.plot)
        control_layout.addWidget(self.view_mode_selector)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.plot)
        control_layout.addWidget(self.refresh_button)
        
        layout.addLayout(control_layout)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Statistics label
        self.stats_label = QLabel("Statistics will appear here")
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)

    def plot(self):
        channel_index = self.channel_selector.currentIndex()
        signal_type = self.signal_type_selector.currentIndex()
        view_mode = self.view_mode_selector.currentIndex()
        
        raw_data = self.get_data_callback(channel_index)

        # Process signal based on selected type
        channel_data = self._process_signal(raw_data, signal_type)
        
        # Get signal type name for display
        signal_type_names = ["Unfiltered", "Filtered", "RMS"]
        signal_type_name = signal_type_names[signal_type]
        
        if len(channel_data) == 0:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=16)
            ax.set_title(f'Channel {channel_index} ({signal_type_name}) - No Data')
            self.canvas.draw()
            self.stats_label.setText("No data available for statistics")
            return
        
        self.figure.clear()
        
        if view_mode == 0:  # Complete Signal
            ax = self.figure.add_subplot(111)
            time_axis = np.arange(len(channel_data))
            ax.plot(time_axis, channel_data, 'b-', linewidth=0.5)
            ax.set_title(f'Channel {channel_index} ({signal_type_name}) - Complete Signal')
            ax.set_xlabel('Sample Number')
            ax.set_ylabel('Amplitude')
            ax.grid(True, alpha=0.3)
            
        else:  # Signal Statistics
            # Create subplots for different statistics
            ax1 = self.figure.add_subplot(2, 2, 1)
            ax2 = self.figure.add_subplot(2, 2, 2)
            ax3 = self.figure.add_subplot(2, 2, 3)
            ax4 = self.figure.add_subplot(2, 2, 4)
            
            # Histogram
            ax1.hist(channel_data, bins=50, alpha=0.7, color='blue', edgecolor='black')
            ax1.set_title(f'{signal_type_name} Signal Histogram')
            ax1.set_xlabel('Amplitude')
            ax1.set_ylabel('Frequency')
            ax1.grid(True, alpha=0.3)
            
            # Running average
            window_size = max(1, len(channel_data) // 100)
            running_avg = np.convolve(channel_data, np.ones(window_size)/window_size, mode='valid')
            ax2.plot(running_avg, 'r-', linewidth=1)
            ax2.set_title(f'{signal_type_name} Running Average (window={window_size})')
            ax2.set_xlabel('Sample Number')
            ax2.set_ylabel('Amplitude')
            ax2.grid(True, alpha=0.3)
            
            # Frequency domain
            fft_data = np.fft.fft(channel_data)
            freqs = np.fft.fftfreq(len(channel_data))
            ax3.plot(freqs[:len(freqs)//2], np.abs(fft_data[:len(fft_data)//2]), 'g-', linewidth=1)
            ax3.set_title(f'{signal_type_name} Frequency Domain')
            ax3.set_xlabel('Frequency (normalized)')
            ax3.set_ylabel('Magnitude')
            ax3.grid(True, alpha=0.3)
            
            # Signal envelope
            envelope = np.abs(signal.hilbert(channel_data))
            time_axis = np.arange(len(channel_data))
            ax4.plot(time_axis, channel_data, 'b-', alpha=0.5, linewidth=0.5, label='Signal')
            ax4.plot(time_axis, envelope, 'r-', linewidth=1, label='Envelope')
            ax4.set_title(f'{signal_type_name} Signal Envelope')
            ax4.set_xlabel('Sample Number')
            ax4.set_ylabel('Amplitude')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            
            self.figure.tight_layout()
        
        self.canvas.draw()
        
        # Update statistics
        if len(channel_data) > 0:
            mean_val = np.mean(channel_data)
            std_val = np.std(channel_data)
            min_val = np.min(channel_data)
            max_val = np.max(channel_data)
            rms_val = np.sqrt(np.mean(channel_data**2))
            
            stats_text = f"""
        Channel {channel_index} ({signal_type_name}) Statistics:
        Mean: {mean_val:.4f}
        Std Dev: {std_val:.4f}
        Min: {min_val:.4f}
        Max: {max_val:.4f}
        RMS: {rms_val:.4f}
        Samples: {len(channel_data)}
        """
            self.stats_label.setText(stats_text)
        else:
            self.stats_label.setText("No data available for statistics")

    def _apply_bandpass_filter(self, data):
        if len(data) < 2 * self.filter_order:
            return data  # Not enough data for filtering

        try:
            nyquist = 0.5 * self.fs
            low = self.lowcut / nyquist
            high = self.highcut / nyquist
            b, a = signal.butter(self.filter_order, [low, high], btype='band')
            return signal.filtfilt(b, a, data)
        except Exception as e:
            logging.error(e)
            return data

    def _calculate_rms(self, data):
        if len(data) < self.rms_window:
            return np.sqrt(np.mean(data ** 2)) * np.ones_like(data)

        rms_values = np.zeros_like(data)
        for i in range(len(data)):
            start_idx = max(0, i - self.rms_window // 2)
            end_idx = min(len(data), i + self.rms_window // 2 + 1)
            rms_values[i] = np.sqrt(np.mean(data[start_idx:end_idx] ** 2))
        return rms_values

    def _process_signal(self, data, signal_type):
        if signal_type == 0:  # Unfiltered
            return data
        elif signal_type == 1:  # Filtered
            return self._apply_bandpass_filter(data)
        elif signal_type == 2:  # RMS
            return self._calculate_rms(data)
        return data