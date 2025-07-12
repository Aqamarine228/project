import threading
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np

from config import SERVER_HOST, SERVER_PORT, BUFFER_LIMIT, NUMBER_OF_CHANNELS
from service.data_buffer import DataBuffer
from service.tcp import TCPService


class MainViewModel(QObject):
    status_changed = pyqtSignal(str)  # Signal to show status
    new_data = pyqtSignal(np.ndarray)  # Signal for new data

    def __init__(self):
        super().__init__()

        self.__buffer = DataBuffer(BUFFER_LIMIT, NUMBER_OF_CHANNELS)
        self.__tcp_kill_event = threading.Event()
        self.__tcp_service = TCPService(self.on_new_data, self.on_status_change, SERVER_HOST, SERVER_PORT)
        self.__tcp_thread = None
        self.__visualization_paused = False

    def start_tcp(self):
        self.__tcp_kill_event.clear()
        self.__tcp_service = TCPService(self.on_new_data, self.on_status_change, SERVER_HOST, SERVER_PORT)
        self.__tcp_thread = Thread(target=self.__tcp_service.start, args=(self.__tcp_kill_event,))
        self.__tcp_thread.start()

    def stop_tcp(self):
        if self.__tcp_service:
            self.__tcp_kill_event.set()
            self.__tcp_service.stop()

    def on_status_change(self, status):
        self.status_changed.emit(status)

    def on_new_data(self, chunk):
        if not self.__visualization_paused:
            self.__buffer.append_chunk(chunk)
            self.new_data.emit(chunk)
    
    def stop_visualization(self):
        self.__visualization_paused = True
    
    def resume_visualization(self):
        self.__visualization_paused = False

    def get_channel_data(self, channel_index):
        return self.__buffer.get_channel_data(channel_index)
    
    def clear_data(self):
        self.__buffer.clear()

    def has_data(self):
        return not self.__buffer.is_empty()

