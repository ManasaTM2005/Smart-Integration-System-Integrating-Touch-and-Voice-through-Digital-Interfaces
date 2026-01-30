# Hand Gesture Virtual Keyboard - User Guide

## Overview

The Hand Gesture Virtual Keyboard is an innovative interface that allows you to type without touching anything. It uses your webcam to detect hand gestures and translates them into keyboard input.

## Quick Start

### Method 1: Using the Launcher (Recommended)
```bash
python launch_gesture_keyboard.py
```
This opens a user-friendly interface with instructions and a launch button.

### Method 2: Direct Launch
```bash
python gesture_keyboard_interface.py
```

### Method 3: Using Voice Command
While running the main voice assistant:
```bash
python main.py
```
Then say any of these voice commands:
- "hand keyboard"
- "gesture keyboard"  
- "hand typing"
- "gesture typing"

## How to Use the Keyboard

### Basic Operation

1. **Position Yourself**: Sit in front of your webcam with good lighting
2. **See Your Hand**: Verify your hand appears in the camera feed on the left
3. **Point at Keys**: Extend your index finger to point at keyboard keys
4. **Select Keys**: Close your fist (make a fist) to click the highlighted key
5. **Watch Results**: Your typed text appears in the text display area

### Visual Feedback

- **Blue keys**: Not currently selected
- **Yellow highlight**: Key is being pointed at  
- **Red highlight**: Fist is closed (clicking)
- **Green flash**: Key was successfully pressed

### Hand Gestures

#### Pointing Gesture
- Extend your index finger
- Keep other fingers curled
- Your index finger position determines which key is selected

#### Click Gesture (Fist)
- Close all your fingers into a fist
- This selects/clicks the currently highlighted key
- Release to deselect

## Keyboard Layout

```
Q W E R T Y U I O P
A S D F G H J K L
Z X C V B N M Space Back
Enter
```

## Special Keys

| Key | Function |
|-----|----------|
| **Space** | Add a space character |
| **Back** | Delete the last character |
| **Enter** | Confirm/Submit (signal to application) |
| **Clear** | Delete all text at once |
| **Exit** | Close the keyboard application |

## Tips for Best Results

### Hand Detection
- ✓ Keep your hand fully visible in the camera
- ✓ Use natural lighting (avoid backlighting)
- ✓ Keep your hand at a comfortable distance (60-80cm from camera)
- ✓ Avoid shadows on your hand

### Gesture Recognition
- ✓ Extend your finger clearly when pointing
- ✓ Keep your wrist straight
- ✓ Make a clear fist when clicking (curl all fingers)
- ✓ Pause briefly between clicks for detection
- ✓ Move smoothly across keys

### Typing Efficiency
- ✓ Start slowly to get comfortable
- ✓ Ensure good keyboard visibility
- ✓ Take breaks if your arm gets tired
- ✓ Maintain consistent hand height

## Troubleshooting

### Camera Not Opening
**Problem**: "Camera could not be opened"
- Check if your webcam is connected
- Ensure no other application is using the camera
- Try restarting the application
- Click "Retry" if available

### Hand Not Detected
**Problem**: Hand landmarks not showing in camera feed
- Improve lighting in the room
- Move closer to the camera (60-80cm away)
- Ensure your entire hand is visible
- Avoid wearing sleeves that hide your hand

### Keys Not Responding to Clicks
**Problem**: Fist gestures aren't registering
- Make a more complete fist (curl all fingers tightly)
- Pause slightly after pointing before closing fist
- Check that your hand is clearly visible
- Reduce detection sensitivity in Settings (coming soon)

### Keyboard Lag
**Problem**: Interface feels sluggish
- Close other applications to free resources
- Improve lighting (helps with hand detection)
- Ensure smooth internet connection (if cloud features enabled)
- Reduce camera resolution in Settings (coming soon)

## Interface Overview

### Main Window (Launcher)
- **Status Display**: Shows current status and any errors
- **Instructions Panel**: Quick reference for using the keyboard
- **Launch Button**: Opens the full keyboard interface
- **Settings Button**: Configure detection sensitivity and more
- **Exit Button**: Close the application

### Keyboard Window

#### Left Panel (Camera Feed)
- Live video from your webcam
- Hand landmarks and detection visualization
- Cursor position indicator
- Gesture state display

#### Right Panel (Keyboard Area)
- **Text Display**: Shows the currently typed text
- **Status Information**: Detection status and feedback
- **Instructions**: How-to guide
- **Virtual Keyboard**: Interactive keys that respond to gestures
- **Control Buttons**: Clear and Exit buttons

## Advanced Features (Coming Soon)

- 📊 Gesture sensitivity customization
- 🎨 Custom keyboard layouts
- 🔤 Multiple language support
- 💾 Text history and clipboard integration
- 🎤 Voice-keyboard hybrid mode
- 📱 Multi-hand support

## Performance Notes

### System Requirements
- Webcam or built-in camera
- Python 3.7+
- 4GB+ RAM recommended
- Decent CPU for real-time processing

### Supported Platforms
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+)

### Resource Usage
- CPU: ~10-20% (varies with hand complexity)
- Memory: ~200-300MB
- GPU: Automatically used if available

## Integrating with Other Applications

### Getting Text from the Keyboard
The typed text is stored in the interface and can be:
1. Copied manually from the text display field
2. Used programmatically by importing `VirtualKeyboard`
3. Sent via Enter key to trigger external commands

### Example Integration (Python)
```python
from virtual_keyboard import VirtualKeyboard
import tkinter as tk

root = tk.Tk()
keyboard = VirtualKeyboard(root)

# Access typed text
text = keyboard.text_input

# Listen for Enter key in your application
# keyboard.key_press("Enter") will trigger your handler
```

## Customization Guide

### Change Keyboard Layout
Edit `virtual_keyboard.py` line with `self.keyboard_layout`:
```python
self.keyboard_layout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    # ... your custom layout
]
```

### Adjust Detection Sensitivity
In `gesture_detector.py`, modify the thresholds:
```python
min_detection_confidence=0.7,  # Lower = more lenient
min_tracking_confidence=0.5,
```

## Support & Feedback

For issues, suggestions, or contributions:
1. Check the Troubleshooting section above
2. Review the HAND_GESTURE_KEYBOARD_README.md file
3. Check error messages in the terminal

## License

This project is part of the Personal Linux Voice Assistant.

---

**Happy Typing with Your Hands!** 🎉
