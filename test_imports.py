#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test service layer imports
    from service.data_buffer import DataBuffer
    print("✓ DataBuffer imported successfully")
    
    from service.tcp import TCPService
    print("✓ TCPService imported successfully")
    
    # Test viewmodel imports
    from viewmodel.main import MainViewModel
    print("✓ MainViewModel imported successfully")
    
    # Test view imports
    from view.channel_plot_widget import ChannelPlotWidget
    print("✓ ChannelPlotWidget imported successfully")
    
    from view.offline_analysis_widget import OfflineAnalysisWidget
    print("✓ OfflineAnalysisWidget imported successfully")
    
    from view.main_view import MainView
    print("✓ MainView imported successfully")
    
    print("\n🎉 All imports successful! The application should work correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")