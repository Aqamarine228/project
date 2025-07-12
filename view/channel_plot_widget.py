import logging

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from vispy import scene
from vispy.scene import Line
import numpy as np
from scipy import signal

from config import SAMPLING_FREQUENCY, LOW_CUTOFF_FREQUENCY, HIGH_CUTOFF_FREQUENCY, RMS_WINDOW, FILTER_ORDER


class ChannelPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)  # Create canvas
        self.view = self.canvas.central_widget.add_view()

        self.data = np.zeros(1)
        initial_pos = np.column_stack((np.arange(1), self.data))
        self.line = Line(pos=initial_pos, parent=self.view.scene, color='blue', width=2)

        self.view.camera = 'panzoom'
        self.view.camera.set_range(x=(0, 1000), y=(-1, 1))

        layout = QVBoxLayout()
        layout.addWidget(self.canvas.native)
        self.setLayout(layout)

        self.channel_index = 0
        self.sample_count = 0
        self.signal_type = "unfiltered"

        self.fs = SAMPLING_FREQUENCY
        self.lowcut = LOW_CUTOFF_FREQUENCY
        self.highcut = HIGH_CUTOFF_FREQUENCY
        self.filter_order = FILTER_ORDER

        self.rms_window = RMS_WINDOW

    def clear_plot_data(self):
        self.update_plot(np.zeros(1))

    def set_signal_type(self, signal_type):
        self.signal_type = signal_type
        self.update_plot(self.data)

    def update_plot(self, data):

        self.data = data

        if self.signal_type == "filtered":
            data = self._apply_bandpass_filter()
        elif self.signal_type == "rms":
            data = self._calculate_rms()

        x_data = np.arange(len(data))

        self.line.set_data(pos=np.column_stack((x_data, data)))

        self._update_camera_range(data)

    def _apply_bandpass_filter(self):
        if len(self.data) < 2 * self.filter_order:
            return self.data  # Not enough self.data for filtering

        try:
            nyquist = 0.5 * self.fs
            low = self.lowcut / nyquist
            high = self.highcut / nyquist
            b, a = signal.butter(self.filter_order, [low, high], btype='band')
            return signal.filtfilt(b, a, self.data)
        except Exception as e:
            logging.error(e)
            return self.data  # Return original data if filtering fails

    def _calculate_rms(self):
        if len(self.data) < self.rms_window:
            return np.sqrt(np.mean(self.data ** 2)) * np.ones_like(self.data)

        rms_values = np.zeros_like(self.data)
        for i in range(len(self.data)):
            start_idx = max(0, i - self.rms_window // 2)
            end_idx = min(len(self.data), i + self.rms_window // 2 + 1)
            rms_values[i] = np.sqrt(np.mean(self.data[start_idx:end_idx] ** 2))
        return rms_values

    def _update_camera_range(self, data):
        y_min, y_max = np.min(data), np.max(data)
        y_range = y_max - y_min
        x_range = len(data)
        if y_range > 0:
            margin = y_range * 0.1
            self.view.camera.set_range(x=(0, x_range), y=(y_min - margin, y_max + margin))
