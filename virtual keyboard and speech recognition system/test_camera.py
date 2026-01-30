#!/usr/bin/env python
"""
Quick camera diagnostic tool
Tests camera availability and compatibility
"""

import cv2
import sys

def test_cameras():
    """Test all available camera indices"""
    print("=" * 60)
    print("CAMERA DIAGNOSTIC TEST")
    print("=" * 60)
    
    found_cameras = []
    
    # Test indices 0-5
    for idx in range(6):
        print(f"\nTesting camera index {idx}...")
        
        # Try DirectShow first (Windows)
        try:
            cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
            if cap and cap.isOpened():
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret:
                    print(f"  ✓ Camera {idx} FOUND (DirectShow)")
                    print(f"    Resolution: {int(width)}x{int(height)}")
                    print(f"    FPS: {fps}")
                    print(f"    Frame read: ✓ Success")
                    found_cameras.append(idx)
                else:
                    print(f"  ⚠ Camera {idx} opened but can't read frames")
                
                cap.release()
                continue
        except Exception as e:
            print(f"  DirectShow failed: {e}")
        
        # Try default backend
        try:
            cap = cv2.VideoCapture(idx)
            if cap and cap.isOpened():
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                # Try to read a frame
                ret, frame = cap.read()
                if ret:
                    print(f"  ✓ Camera {idx} FOUND (Default Backend)")
                    print(f"    Resolution: {int(width)}x{int(height)}")
                    print(f"    FPS: {fps}")
                    print(f"    Frame read: ✓ Success")
                    found_cameras.append(idx)
                else:
                    print(f"  ⚠ Camera {idx} opened but can't read frames")
                
                cap.release()
                continue
        except Exception as e:
            print(f"  Default backend failed: {e}")
        
        print(f"  ✗ Camera {idx} not available")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if found_cameras:
        print(f"✓ Found cameras at indices: {found_cameras}")
        print(f"✓ Recommend using index: {found_cameras[0]}")
        print("\nTo use camera in keyboard, it will automatically find it.")
    else:
        print("✗ No cameras found!")
        print("\nPossible solutions:")
        print("  1. Check if camera is physically connected")
        print("  2. Check Device Manager for USB camera device")
        print("  3. Try restarting the application")
        print("  4. Check if another application is using the camera")
        print("  5. Check camera permissions in Windows settings")
        print("  6. Try different USB ports")
        print("  7. Update camera drivers")
    
    print("\nOpenCV Version:", cv2.__version__)
    print("Python Version:", sys.version)
    print("=" * 60)

if __name__ == "__main__":
    test_cameras()
