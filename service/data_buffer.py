import numpy as np
from collections import deque

class DataBuffer:
    def __init__(self):
        self.buffer = deque(maxlen=1000)  # Circular buffer for real-time
        self.all_data = []  # Store all data for offline analysis

    def append_chunk(self, chunk):
        # Reshape flat list into 32x18 matrix
        chunk_np = np.array(chunk).reshape(32, 18)
        self.buffer.append(chunk_np)  # Save to buffer
        self.all_data.append(chunk_np)  # Save to complete dataset

    def get_latest_chunk(self):
        if not self.buffer:
            return np.zeros((32, 18))  # Return empty if no data
        return self.buffer[-1]  # Return latest
    
    def get_all_data(self):
        """Get all recorded data for offline analysis"""
        if not self.all_data:
            return np.zeros((0, 32, 18))
        return np.array(self.all_data)
    
    def get_channel_data(self, channel_index):
        """Get all data for a specific channel"""
        if not self.all_data or channel_index < 0 or channel_index >= 32:
            return np.array([])
        channel_data = [chunk[channel_index] for chunk in self.all_data]
        return np.concatenate(channel_data)
    
    def clear(self):
        """Clear all stored data"""
        self.buffer.clear()
        self.all_data.clear()