import socket
import struct
import time
import math
import threading
import argparse
import signal
import sys
from typing import List, Tuple

class TCPTestClient:
    def __init__(self, host: str = 'localhost', port: int = 5000, channels: int = 4, rate: float = 20.0):
        self.host = host
        self.port = port
        self.channels = channels
        self.rate = rate
        self.running = False
        self.socket = None

    def generate_signal_data(self, t: float) -> List[float]:
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

    def start(self):
        try:
            print("Connecting to server...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(None)
            print("Connected")


            self.running = True

            print(f"Channels: {self.channels}, Update rate: {self.rate} Hz")
            print(f"Data format: {self.channels} floats per packet ({self.channels * 4} bytes)")
            print("Started sending data... (Press Ctrl+C to stop)")

            while self.running:
                try:
                    t = 0.0
                    dt = 1.0 / self.rate

                    while self.running:
                        signals = self.generate_signal_data(t)

                        format_string = 'f' * self.channels
                        data = struct.pack(format_string, *signals)

                        self.socket.send(data)

                        t += dt

                        time.sleep(dt)

                except OSError:
                    if self.running:
                        print("Error accepting connection")
                    break

        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()

def main():
    parser = argparse.ArgumentParser(description='TCP Client for Signal Visualization')
    parser.add_argument('--host', default='localhost', help='Server hostname (default: localhost)')
    parser.add_argument('--port', type=int, default=5000, help='Server port (default: 12345)')
    parser.add_argument('--channels', type=int, default=32, help='Number of channels (default: 4)')
    parser.add_argument('--rate', type=float, default=20.0, help='Update rate in Hz (default: 20.0)')

    args = parser.parse_args()

    if args.channels < 1:
        print("Error: Number of channels must be at least 1")
        sys.exit(1)

    if args.rate <= 0:
        print("Error: Update rate must be positive")
        sys.exit(1)

    server = TCPTestClient(args.host, args.port, args.channels, args.rate)

    try:
        server.start()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt")
    finally:
        server.stop()

if __name__ == '__main__':
    main()