#!/usr/bin/env python
"""
Quick launcher for the Hand Gesture Virtual Keyboard
Run this script directly from command line or double-click it
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gesture_keyboard_interface import launch_interface
    print("Launching Hand Gesture Virtual Keyboard Interface...")
    launch_interface()
except ImportError as e:
    print(f"Error: Missing required module: {e}")
    print("\nPlease ensure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error launching interface: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
