from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QPushButton, QLabel

from config import NUMBER_OF_CHANNELS
from view.channel_plot_widget import ChannelPlotWidget
from view.offline_analysis_widget import OfflineAnalysisWidget
from viewmodel.main import MainViewModel


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Visualization")
        self.setGeometry(100, 100, 1000, 600)

        self.viewModel = MainViewModel()  # Link to business logic

        self.plot_widget = ChannelPlotWidget()  # Plot area

        self.offline_window = OfflineAnalysisWidget(self.viewModel.get_channel_data)

        # Dropdown to choose channel
        self.channel_selector = QComboBox()
        self.channel_selector.addItems([f"Channel {i}" for i in range(NUMBER_OF_CHANNELS)])
        self.channel_selector.currentIndexChanged.connect(self.change_channel)

        # Signal type selector
        self.signal_type_selector = QComboBox()
        self.signal_type_selector.addItems(["Unfiltered", "Filtered", "RMS"])
        self.signal_type_selector.currentIndexChanged.connect(self.change_signal_type)

        # Buttons for TCP connection
        self.receive_button = QPushButton("Listen TCP")
        self.receive_button.clicked.connect(self.start_tcp)

        self.stop_receiving_button = QPushButton("Stop listening TCP")
        self.stop_receiving_button.clicked.connect(self.stop_tcp)
        self.stop_receiving_button.setEnabled(False)

        # STOP/RESUME buttons
        self.stop_button = QPushButton("STOP")
        self.stop_button.clicked.connect(self.stop_visualization)
        self.stop_button.setEnabled(False)

        self.resume_button = QPushButton("RESUME")
        self.resume_button.clicked.connect(self.resume_visualization)
        self.resume_button.setEnabled(False)

        # Button for offline analysis
        self.offline_button = QPushButton("Show Offline Analysis")
        self.offline_button.clicked.connect(self.show_offline_analysis)
        self.offline_button.setEnabled(False)

        # Button to clear data
        self.clear_button = QPushButton("Clear Data")
        self.clear_button.clicked.connect(self.clear_data)

        # Label to show connection status
        self.status_label = QLabel("Server not active")
        self.viewModel.status_changed.connect(self.update_status)
        self.viewModel.new_data.connect(self.apply_new_data)
        self.viewModel.new_data.connect(self.check_offline_data_availability)

        # Layout for the UI
        layout = QVBoxLayout()

        # Control panel layout
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Channel:"))
        control_layout.addWidget(self.channel_selector)
        control_layout.addWidget(QLabel("Signal Type:"))
        control_layout.addWidget(self.signal_type_selector)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.receive_button)
        button_layout.addWidget(self.stop_receiving_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.resume_button)

        # Action button layout
        action_layout = QHBoxLayout()
        action_layout.addWidget(self.offline_button)
        action_layout.addWidget(self.clear_button)

        layout.addLayout(control_layout)
        layout.addWidget(self.plot_widget)
        layout.addLayout(button_layout)
        layout.addLayout(action_layout)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Check initial offline data availability
        self.check_offline_data_availability()


    def apply_new_data(self):
        data = self.viewModel.get_channel_data(self.channel_selector.currentIndex())
        self.plot_widget.update_plot(data)

    def change_channel(self, index):
        data = self.viewModel.get_channel_data(index)
        self.plot_widget.update_plot(data)  # Update channel shown

    def change_signal_type(self, index):
        signal_types = ["unfiltered", "filtered", "rms"]
        self.plot_widget.set_signal_type(signal_types[index])

    def start_tcp(self):
        self.viewModel.start_tcp()
        self.receive_button.setEnabled(False)
        self.stop_receiving_button.setEnabled(True)
        self.stop_button.setEnabled(True)

    def stop_tcp(self):
        self.viewModel.stop_tcp()
        self.receive_button.setEnabled(True)
        self.stop_receiving_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.resume_button.setEnabled(False)

    def stop_visualization(self):
        self.viewModel.stop_visualization()
        self.stop_button.setEnabled(False)
        self.resume_button.setEnabled(True)

    def resume_visualization(self):
        self.viewModel.resume_visualization()
        self.stop_button.setEnabled(True)
        self.resume_button.setEnabled(False)

    def update_status(self, status):
        self.status_label.setText(status)

    def check_offline_data_availability(self):
        if self.viewModel.has_data():
            self.offline_button.setEnabled(True)
        else:
            self.offline_button.setEnabled(False)

    def show_offline_analysis(self):
        self.offline_window.plot()
        self.offline_window.show()

    def clear_data(self):
        self.viewModel.clear_data()
        self.plot_widget.clear_plot_data()
        self.offline_button.setEnabled(False)
