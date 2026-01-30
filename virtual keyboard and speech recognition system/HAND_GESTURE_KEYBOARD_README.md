# Hand Gesture Virtual Keyboard - Setup Guide

## Features Added

A new hand gesture-based virtual keyboard interface has been integrated into the voice assistant. This allows you to:

- **Point your finger** at virtual keyboard keys
- **Make a fist** to click/select keys
- **Type text** using hand gestures detected by your webcam
- **Control the interface** without touching anything

## How to Use

### Method 1: Voice Command (Recommended)
1. Start the voice assistant: `python main.py`
2. Say one of these wake commands:
   - "hey master"
   - "i am ready"
   - "yes master"
3. Once the assistant responds, say:
   - **"hand keyboard"** or
   - **"gesture keyboard"** or
   - **"hand typing"** or
   - **"gesture typing"**
4. The virtual keyboard interface will open automatically

### Method 2: Direct Launch
Run directly: `python virtual_keyboard.py`

## How to Type

### Step-by-Step Instructions:
1. **Position yourself** in front of your webcam
2. **Point your index finger** at the key you want to type
3. **Make a fist** (close your hand) to click the selected key
4. The text will appear in the input field above the keyboard

## Keyboard Controls

- **Letter keys (A-Z)**: Type letters
- **Space**: Add a space
- **Back**: Delete the last character
- **Enter**: Confirm/Submit text
- **Clear button**: Clear all text at once
- **Exit button**: Close the application

## Technical Details

### New Files Created:
1. **gesture_detector.py** - Hand detection and gesture recognition using MediaPipe
2. **virtual_keyboard.py** - GUI interface with virtual keyboard
3. **test_hand_gesture.py** - Test script to verify installation

### Modified Files:
1. **main.py** - Added import and handler for hand gesture keyboard
2. **strlists.py** - Added voice command strings for hand gesture keyboard

### Dependencies Installed:
- **mediapipe** - Hand detection and tracking
- **opencv-python** - Video capture and processing
- **tkinter** - GUI (built-in with Python)
- **PIL/Pillow** - Image processing

## How It Works

1. **Hand Detection**: MediaPipe detects your hand in real-time via webcam
2. **Gesture Recognition**: 
   - Points your index finger position
   - Detects when you make a fist
3. **Key Selection**: Shows which key you're pointing at
4. **Text Input**: Captures text and displays in input field

## Troubleshooting

### Camera not detected?
- Make sure your webcam is connected and working
- Check if other applications are using the camera
- Give the app permission to access camera (Windows may prompt)

### Hand not detected?
- Ensure adequate lighting
- Keep hand fully visible in frame
- Move hand closer to camera if detection is poor
- Wear a contrasting colored sleeve/shirt for better detection

### Performance slow?
- Close other applications
- Lower camera resolution
- Ensure proper ventilation for your computer

## Tips for Best Results

✓ **Good lighting** - Natural or bright artificial light
✓ **Steady hand** - Keep hand relatively still while selecting
✓ **Full visibility** - Keep entire hand visible in camera frame
✓ **Distance** - Position hand 30-50 cm from camera
✓ **Contrast** - Wear contrasting colored clothing
✓ **Clean camera** - Keep webcam lens clean

## Voice Commands Reference

To activate hand gesture keyboard, say:
- "hand keyboard"
- "gesture keyboard" 
- "hand typing"
- "gesture typing"

## Example Usage Scenario

```
User: "Hey master" (wake phrase)
Assistant: "Yes master proceed"
User: "Hand keyboard"
Assistant: "Starting hand gesture keyboard master"
Assistant: "Point your finger at keys and make a fist to click"
[Virtual keyboard opens with camera feed]
User: [Points at keys and makes fist to type]
```

## Advanced Features (Future Enhancements)

Potential improvements:
- Multi-hand support
- Swipe gestures for quick deletion
- Custom gesture commands
- Text-to-speech integration with typed text
- Predictive text suggestions
- Different keyboard layouts

## Support & Issues

If you encounter any issues:
1. Check that all dependencies are installed: `python test_hand_gesture.py`
2. Ensure camera permissions are granted
3. Check console output for error messages
4. Try restarting the application

## Enjoy your hands-free typing!

The hand gesture virtual keyboard brings a new dimension to voice-assisted computing. Practice makes perfect - it may take a few tries to get the right angle and gesture, but soon you'll be typing without touching!
