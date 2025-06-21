from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from view.channel_plot_widget import ChannelPlotWidget
from viewmodel.main import MainViewModel


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Visualization")
        self.setGeometry(100, 100, 1000, 600)

        self.viewModel = MainViewModel()  # Link to business logic

        self.plot_widget = ChannelPlotWidget()  # Plot area

        # Dropdown to choose channel
        self.channel_selector = QComboBox()
        self.channel_selector.addItems([f"Channel {i}" for i in range(32)])
        self.channel_selector.currentIndexChanged.connect(self.change_channel)

        # Signal type selector
        self.signal_type_selector = QComboBox()
        self.signal_type_selector.addItems(["Unfiltered", "Filtered", "RMS"])
        self.signal_type_selector.currentIndexChanged.connect(self.change_signal_type)

        # Buttons for TCP connection
        self.connect_button = QPushButton("Connect TCP")
        self.connect_button.clicked.connect(self.connect_tcp)
        
        self.disconnect_button = QPushButton("Disconnect TCP")
        self.disconnect_button.clicked.connect(self.disconnect_tcp)
        self.disconnect_button.setEnabled(False)
        
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
        self.status_label = QLabel("Disconnected")
        self.viewModel.status_changed.connect(self.update_status)
        self.viewModel.new_data.connect(self.plot_widget.update_plot)
        self.viewModel.new_data.connect(lambda: self.check_offline_data_availability())
        self.viewModel.offline_data_ready.connect(self.enable_offline_analysis)

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
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)
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

    def change_channel(self, index):
        self.plot_widget.set_channel(index)  # Update channel shown
        # Force a plot update with current data if available
        if hasattr(self.viewModel, 'buffer') and self.viewModel.buffer.get_latest_chunk().size > 0:
            self.plot_widget.update_plot(self.viewModel.buffer.get_latest_chunk())
    
    def change_signal_type(self, index):
        signal_types = ["unfiltered", "filtered", "rms"]
        self.plot_widget.set_signal_type(signal_types[index])
    
    def connect_tcp(self):
        self.viewModel.connect_tcp()
        self.connect_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        self.stop_button.setEnabled(True)
    
    def disconnect_tcp(self):
        self.viewModel.disconnect_tcp()
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
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
        if status == "Disconnected":
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
    
    def enable_offline_analysis(self, data):
        self.offline_button.setEnabled(True)
    
    def check_offline_data_availability(self):
        """Check if offline data is available and enable button accordingly"""
        if hasattr(self.viewModel, 'buffer'):
            all_data = self.viewModel.buffer.get_all_data()
            if len(all_data) > 0:
                self.offline_button.setEnabled(True)
            else:
                self.offline_button.setEnabled(False)
    
    def show_offline_analysis(self):
        # Create offline analysis window
        from view.offline_analysis_widget import OfflineAnalysisWidget
        self.offline_window = OfflineAnalysisWidget(self.viewModel)
        self.offline_window.show()
    
    def clear_data(self):
        self.viewModel.clear_data()
        # Clear the plot widget's internal data and update display
        self.plot_widget.clear_plot_data()
        # Check data availability to update offline button state
        self.check_offline_data_availability()
