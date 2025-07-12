# Signal Visualization Application

A real-time signal visualization application built with PyQt5 and VisPy, designed for monitoring and analyzing multi-channel data streams over TCP connections.

## Features

### Real-time Visualization
- Multi-channel signal plotting with smooth updates
- Auto-scaling for optimal viewing
- Channel switching capabilities
- Performance-optimized rendering with VisPy

### TCP Communication
- Robust TCP client with error handling
- Automatic reconnection capabilities
- Thread-safe data reception
- Connection status monitoring

### Offline Analysis
- Complete signal visualization
- Statistical analysis (histogram, running average)
- Frequency domain analysis
- Signal envelope detection
- Channel-specific data retrieval

### Data Management
- Dual buffer system for real-time and offline data
- Configurable data history (1000 samples)
- Data clearing functionality
- Channel-specific data access

## Architecture

The application follows the MVVM (Model-View-ViewModel) pattern:

```
├── main.py                 # Application entry point
├── service/                # Data services layer
│   ├── tcp.py             # TCP communication service
│   └── data_buffer.py     # Data buffering and management
├── viewmodel/             # Business logic layer
│   └── main.py            # Main view model
└── view/                  # User interface layer
    ├── main_view.py       # Main application window
    ├── channel_plot_widget.py    # Real-time plotting widget
    └── offline_analysis_widget.py # Offline analysis widget
```

## Requirements

- Python 3.12+

## Quick Start

1. Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd project
pip install -r requirements.txt
```

2. Start the test server (in one terminal):
```bash
python tcp_test_server.py
```

3. Run the application (in another terminal):
```bash
python main.py
```

4. In the application:
   - Click "Connect" to start receiving data
   - Use channel selector to switch between channels
   - Click "Offline Analysis" to explore data analysis features

## Installation

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Step-by-step Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd project
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Verify installation:**
```bash
python main.py
```

## Usage

### Starting the Application

1. Launch the application with `python main.py`
2. Enter the TCP server details (host and port)
3. Click "Listen TCP" to wait for connections

- **Listen TCP**: Start listening for tcp connections
- **Stop listening TCP**: Stop listening for incoming connections
- **Status**: Monitor connection state in real-time

### Offline Analysis

1. Collect data by connecting to a TCP server (or use offline analysis anytime when data is available)
2. Click "Offline Analysis" to open the analysis window
3. Select channel and signal type:
   - **Unfiltered**: Raw signal data
   - **Filtered**: Bandpass filtered signal (1-100 Hz, 4th order Butterworth)
   - **RMS**: Root Mean Square values (50-sample window)
4. Choose analysis type:
   - **Complete Signal**: Full signal visualization
   - **Histogram**: Data distribution analysis
   - **Running Average**: Smoothed signal trends
   - **Frequency Domain**: FFT analysis
   - **Signal Envelope**: Signal envelope detection

### Data Management

- **Clear Data**: Remove all stored data and reset buffers
- Data is automatically stored for offline analysis
- Each channel maintains separate data history

## TCP Server Setup

### Using the Included Test Server

The project includes a test server (`tcp_test_server.py`) for development and testing:

```bash
# Run with default settings (localhost:12345, 4 channels, 20 Hz)
python tcp_test_server.py

# Run with custom settings
python tcp_test_server.py --host localhost --port 5000 --channels 32 --rate 20
```

The test server generates various signal types:
- **Channel 1**: Sine wave
- **Channel 2**: Cosine wave  
- **Channel 3**: Square wave
- **Channel 4**: Sawtooth wave
- **Additional channels**: Combinations of the above

## Application Controls

### Main Window
- **Channel**: Select active channel for real-time plotting
- **Listen/Stop listening TCP**: Manage TCP connection
- **Offline Analysis**: Open offline analysis window
- **Clear Data**: Reset all stored data
- **STOP**: Stop receiving new data from client without disconnection
- **RESUME**: Resume receiving data from client

### Offline Analysis Window
- **Channel Selector**: Choose channel for analysis
- **Signal Type**: Select signal processing (Unfiltered, Filtered, RMS)
- **View Mode**: Select analysis type
- **Refresh**: Update analysis with latest data
- **Statistics**: View numerical analysis results

## Error Handling

The application includes comprehensive error handling:

- **Connection Errors**: Automatic retry and user notification
- **Data Reception Errors**: Graceful handling of malformed data
- **Socket Timeouts**: Configurable timeout management
- **Thread Safety**: Safe data sharing between threads

## Development

### Code Structure

- **Service Layer**: Handles TCP communication and data buffering
- **ViewModel Layer**: Manages business logic and data flow
- **View Layer**: Implements user interface and visualization

### Key Components

1. **TCPService**: Manages TCP connections and data reception
2. **DataBuffer**: Handles data storage and retrieval
3. **MainViewModel**: Coordinates between services and views
4. **ChannelPlotWidget**: Real-time signal visualization
5. **OfflineAnalysisWidget**: Statistical analysis and visualization

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **Connection Failed**: Verify TCP server is running and accessible
3. **No Data Display**: Check data format matches expected binary structure
4. **Performance Issues**: Reduce update rate or data history size

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue in the repository