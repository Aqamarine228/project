#!/usr/bin/env python3
"""
TCP Test Server for Signal Visualization Application

This script creates a TCP server that sends simulated multi-channel signal data
to test the Signal Visualization Application.

Usage:
    python tcp_test_server.py [--host HOST] [--port PORT] [--channels CHANNELS] [--rate RATE]

Example:
    python tcp_test_server.py --host localhost --port 12345 --channels 4 --rate 20
"""

import socket
import struct
import time
import math
import threading
import argparse
import signal
import sys
from typing import List, Tuple

class TCPTestServer:
    def __init__(self, host: str = 'localhost', port: int = 12345, channels: int = 4, rate: float = 20.0):
        """
        Initialize TCP test server.
        
        Args:
            host: Server hostname
            port: Server port
            channels: Number of signal channels
            rate: Update rate in Hz
        """
        self.host = host
        self.port = port
        self.channels = channels
        self.rate = rate
        self.running = False
        self.server_socket = None
        self.client_threads = []
        
    def generate_signal_data(self, t: float) -> List[float]:
        """
        Generate sample signal data for all channels.
        
        Args:
            t: Time parameter
            
        Returns:
            List of signal values for each channel
        """
        signals = []
        
        for i in range(self.channels):
            if i == 0:
                # Sine wave with noise
                signal = math.sin(t) * 100 + math.sin(t * 10) * 10
            elif i == 1:
                # Cosine wave
                signal = math.cos(t * 0.5) * 75
            elif i == 2:
                # Square wave approximation
                signal = 50 * (1 if math.sin(t * 2) > 0 else -1)
            elif i == 3:
                # Sawtooth wave
                signal = (t % (2 * math.pi)) / math.pi * 60 - 30
            else:
                # Additional channels: combination waves
                signal = math.sin(t * (i + 1)) * (100 / (i + 1))
                
            signals.append(signal)
            
        return signals
    
    def handle_client(self, client_socket: socket.socket, client_address: Tuple[str, int]):
        """
        Handle individual client connection.
        
        Args:
            client_socket: Client socket
            client_address: Client address tuple
        """
        print(f"Client connected: {client_address}")
        
        try:
            t = 0.0
            dt = 1.0 / self.rate
            
            while self.running:
                # Generate signal data
                signals = self.generate_signal_data(t)
                
                # Pack as binary data (floats)
                format_string = 'f' * self.channels
                data = struct.pack(format_string, *signals)
                
                # Send data
                client_socket.send(data)
                
                # Update time
                t += dt
                
                # Sleep to maintain update rate
                time.sleep(dt)
                
        except (ConnectionResetError, BrokenPipeError, OSError):
            print(f"Client {client_address} disconnected")
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
            print(f"Client {client_address} connection closed")
    
    def start(self):
        """
        Start the TCP server.
        """
        try:
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            
            print(f"TCP Test Server started on {self.host}:{self.port}")
            print(f"Channels: {self.channels}, Update rate: {self.rate} Hz")
            print(f"Data format: {self.channels} floats per packet ({self.channels * 4} bytes)")
            print("Waiting for connections... (Press Ctrl+C to stop)")
            
            while self.running:
                try:
                    # Accept client connection
                    client_socket, client_address = self.server_socket.accept()
                    
                    # Create thread for client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    self.client_threads.append(client_thread)
                    
                except OSError:
                    if self.running:
                        print("Error accepting connection")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """
        Stop the TCP server.
        """
        print("\nStopping TCP Test Server...")
        self.running = False
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        # Wait for client threads to finish
        for thread in self.client_threads:
            if thread.is_alive():
                thread.join(timeout=1.0)
        
        print("TCP Test Server stopped")

def signal_handler(signum, frame):
    """
    Handle interrupt signal.
    """
    print("\nReceived interrupt signal")
    sys.exit(0)

def main():
    """
    Main function to run the TCP test server.
    """
    parser = argparse.ArgumentParser(description='TCP Test Server for Signal Visualization')
    parser.add_argument('--host', default='localhost', help='Server hostname (default: localhost)')
    parser.add_argument('--port', type=int, default=12345, help='Server port (default: 12345)')
    parser.add_argument('--channels', type=int, default=4, help='Number of channels (default: 4)')
    parser.add_argument('--rate', type=float, default=20.0, help='Update rate in Hz (default: 20.0)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.channels < 1:
        print("Error: Number of channels must be at least 1")
        sys.exit(1)
    
    if args.rate <= 0:
        print("Error: Update rate must be positive")
        sys.exit(1)
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and start server
    server = TCPTestServer(args.host, args.port, args.channels, args.rate)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt")
    finally:
        server.stop()

if __name__ == '__main__':
    main()