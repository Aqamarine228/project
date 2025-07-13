import logging
import socket
import struct

from config import RECEIVE_CHUNK_SIZE
from service.data_buffer import to_chunk


class TCPService:

    def __init__(self, new_data_callback, status_callback, host, port):

        self.__new_data_callback = new_data_callback
        self.__status_callback = status_callback
        self.__host = host
        self.__port = port
        self.__server_socket = None

    def start(self, kill_event):
        self.__status_callback("Starting TCP server...")
        try:
            self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__server_socket.bind((self.__host, self.__port))
            self.__server_socket.listen(1)

            self.__status_callback(f"TCP Server started on {self.__host}:{self.__port}")
            self.__status_callback("Waiting for connections...")


            while not kill_event.is_set():

                client_socket, client_address = self.__server_socket.accept()
                self.__status_callback(f"Client connected: {client_address}")
                logging.info(f"Client connected: {client_address}")

                try:
                    self.handle_connection(client_socket, kill_event)
                except OSError:
                    self.__status_callback("Error accepting connection")
                    logging.exception("Error accepting connection")
                except (ConnectionResetError, BrokenPipeError):
                    pass
                except Exception as e:
                    self.__status_callback(f"Connection closed: error handling client {client_address}: {e}")
                    logging.error(f"Connection closed: error handling client {client_address}: {e}")

                self.__status_callback(f"Client {client_address} disconnected")
                logging.info(f"Client {client_address} disconnected")
                client_socket.close()

        except ConnectionAbortedError:
            pass
        except Exception as e:
            self.__status_callback(f"Server error: {e}")
            logging.error(f"Server error: {e}")

    def handle_connection(self, client_socket, kill_event):
            while not kill_event.is_set():
                try:
                    data = b''
                    while len(data) < RECEIVE_CHUNK_SIZE:
                        packet = client_socket.recv(RECEIVE_CHUNK_SIZE - len(data))

                        if len(packet) == 0:
                            return

                        data += packet

                    if len(data) == RECEIVE_CHUNK_SIZE:
                        chunk = struct.unpack('576f', data)
                        self.__new_data_callback(to_chunk(chunk))

                except socket.timeout:
                    continue

    def stop(self):
        self.__status_callback("Stopping TCP Server...")

        if self.__server_socket:
            self.__server_socket.close()

        self.__status_callback("TCP Server stopped")
