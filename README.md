# Signal Visualization Application

A real-time signal visualization application built with PyQt5 and VisPy, designed for monitoring and analyzing multi-channel data streams over TCP connections.

## Features

### Real-time Visualization
- Multi-channel signal plotting with smooth updates
- Auto-scaling Y-axis for optimal viewing
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

- Python 3.7+
- PyQt5
- VisPy
- NumPy
- Matplotlib (for offline analysis)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Starting the Application

1. Launch the application with `python main.py`
2. Enter the TCP server details (host and port)
3. Click "Connect" to establish connection

### Real-time Monitoring

- Use the channel selector to switch between different data channels
- The plot automatically updates with incoming data
- Y-axis scales automatically based on signal amplitude

### Connection Management

- **Connect**: Establish TCP connection and start data reception
- **Disconnect**: Close connection while preserving received data
- **Status**: Monitor connection state in real-time

### Offline Analysis

1. Collect data by connecting to a TCP server
2. Click "Offline Analysis" to open the analysis window
3. Select channel and analysis type:
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

The application expects a TCP server that sends binary data in the following format:

```python
# Example TCP server
import socket
import struct
import time
import math

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(1)
    
    print("Server listening on localhost:12345")
    
    while True:
        client, addr = server.accept()
        print(f"Client connected: {addr}")
        
        try:
            t = 0
            while True:
                # Generate sample data for 4 channels
                channel1 = math.sin(t) * 100
                channel2 = math.cos(t) * 50
                channel3 = math.sin(t * 2) * 75
                channel4 = math.cos(t * 0.5) * 25
                
                # Pack as binary data (4 floats)
                data = struct.pack('ffff', channel1, channel2, channel3, channel4)
                client.send(data)
                
                t += 0.1
                time.sleep(0.05)  # 20 Hz update rate
                
        except (ConnectionResetError, BrokenPipeError):
            print("Client disconnected")
        finally:
            client.close()

if __name__ == "__main__":
    start_server()
```

## Application Controls

### Main Window
- **Host**: TCP server hostname or IP address
- **Port**: TCP server port number
- **Channel**: Select active channel for real-time plotting
- **Connect/Disconnect**: Manage TCP connection
- **Offline Analysis**: Open offline analysis window
- **Clear Data**: Reset all stored data

### Offline Analysis Window
- **Channel Selector**: Choose channel for analysis
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

### Adding New Features

1. **New Analysis Types**: Extend `OfflineAnalysisWidget` with additional analysis methods
2. **Data Formats**: Modify `DataBuffer` to support different data structures
3. **Visualization**: Add new plot types to `ChannelPlotWidget`
4. **Communication**: Extend `TCPService` for different protocols

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **Connection Failed**: Verify TCP server is running and accessible
3. **No Data Display**: Check data format matches expected binary structure
4. **Performance Issues**: Reduce update rate or data history size

### Debug Mode

Enable debug logging by modifying the logging level in `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

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