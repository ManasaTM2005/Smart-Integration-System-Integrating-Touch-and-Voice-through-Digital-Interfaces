#!/usr/bin/env python
"""
Quick test to verify hand gesture keyboard is working
"""
import sys

print("Testing hand gesture keyboard installation...")
print("=" * 50)

# Test imports
try:
    import cv2
    print("✓ OpenCV installed")
except ImportError:
    print("✗ OpenCV not found")
    sys.exit(1)

try:
    import mediapipe
    print("✓ MediaPipe installed")
except ImportError:
    print("✗ MediaPipe not found")
    sys.exit(1)

try:
    from gesture_detector import GestureDetector
    print("✓ GestureDetector module loaded")
except ImportError as e:
    print(f"✗ GestureDetector error: {e}")
    sys.exit(1)

try:
    from virtual_keyboard import VirtualKeyboard
    print("✓ VirtualKeyboard module loaded")
except ImportError as e:
    print(f"✗ VirtualKeyboard error: {e}")
    sys.exit(1)

print("=" * 50)
print("All dependencies installed successfully!")
print("\nTo use hand gesture keyboard:")
print("  - Say: 'hand keyboard' or 'gesture keyboard'")
print("  - Point your finger at keys")
print("  - Make a fist to click")
print("=" * 50)
