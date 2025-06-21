import socket
import threading
import struct

class TCPService(threading.Thread):
    def __init__(self, buffer, new_data_callback, status_callback):
        super().__init__()
        self.buffer = buffer
        self.new_data_callback = new_data_callback
        self.status_callback = status_callback
        self.running = True
        self.socket = None
        self.daemon = True  # Allow main thread to exit

    def run(self):
        self.status_callback("Connecting...")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)  # 5 second timeout
            self.socket.connect(('127.0.0.1', 12345))  # Connect to TCP server
            self.socket.settimeout(None)  # Remove timeout for data reception
            self.status_callback("Connected")

            while self.running:
                try:
                    # Expect 576 float32 values (2304 bytes)
                    data = b''
                    while len(data) < 2304 and self.running:
                        packet = self.socket.recv(2304 - len(data))
                        if not packet:
                            self.running = False
                            break
                        data += packet
                    
                    if len(data) == 2304:
                        # Convert binary to float values
                        chunk = struct.unpack('576f', data)
                        self.buffer.append_chunk(chunk)  # Store in buffer
                        self.new_data_callback()  # Notify new data
                    elif not self.running:
                        break
                except socket.timeout:
                    continue
                except socket.error as e:
                    self.status_callback(f"Socket error: {e}")
                    break
        except socket.timeout:
            self.status_callback("Connection timeout")
        except ConnectionRefusedError:
            self.status_callback("Connection refused - server not available")
        except Exception as e:
            self.status_callback(f"Error: {e}")  # Show error
        finally:
            if self.socket:
                self.socket.close()
            self.status_callback("Disconnected")
    
    def stop(self):
        """Stop the TCP service gracefully"""
        self.running = False
        if self.socket:
            self.socket.close()

