import numpy as np
from collections import deque

from config import NUMBER_OF_CHANNELS, CHANNEL_LENGTH, BUFFER_LIMIT


class DataBuffer:
    def __init__(self, buffer_limit, number_of_channels):
        self.__buffer = deque(maxlen=buffer_limit)
        self.__number_of_channels = number_of_channels

    def append_chunk(self, chunk):
        self.__buffer.append(to_chunk(chunk))

    def is_empty(self):
        return len(self.__buffer) == 0

    def get_channel_data(self, channel_index):
        if not self.__buffer or channel_index < 0 or channel_index >= self.__number_of_channels:
            return np.array([])
        channel_data = [chunk[channel_index] for chunk in self.__buffer]
        return np.concatenate(channel_data)
    
    def clear(self):
        self.__buffer.clear()


def to_chunk(chunk):
    return np.array(chunk).reshape(NUMBER_OF_CHANNELS, CHANNEL_LENGTH)
