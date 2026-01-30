import cv2
import numpy as np
import tkinter as tk
from tkinter import Canvas, Button, Entry, Label
from PIL import Image, ImageTk
import threading
import time
from gesture_detector import GestureDetector

class VirtualKeyboard:
    """Virtual keyboard interface with hand gesture control"""
    
    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
            
        self.root.title("Hand Gesture Virtual Keyboard")
        self.root.geometry("1400x800")
        
        # Keyboard layout
        self.keyboard_layout = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space', 'Back'],
            ['Enter']
        ]
        
        self.gesture_detector = GestureDetector()
        
        # Try to initialize camera with error handling and retries
        self.cap = None
        self.camera_available = False
        def open_camera():
            # Try DirectShow on Windows for more stable capture; fall back to default
            indices = [0, 1, 2, 3]
            for idx in indices:
                print(f"Attempting to open camera index {idx}...")
                try:
                    cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                    if cap.isOpened():
                        print(f"  ✓ Camera {idx} opened with DirectShow")
                except Exception as e:
                    print(f"  ✗ DirectShow failed for index {idx}: {e}")
                    try:
                        cap = cv2.VideoCapture(idx)
                        if cap.isOpened():
                            print(f"  ✓ Camera {idx} opened with default backend")
                    except Exception as e2:
                        print(f"  ✗ Default backend failed for index {idx}: {e2}")
                        cap = None

                if cap and cap.isOpened():
                    # set conservative properties to reduce load
                    try:
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        cap.set(cv2.CAP_PROP_FPS, 15)
                        print(f"  ✓ Camera {idx} properties set successfully")
                    except Exception as e:
                        print(f"  ⚠ Could not set camera properties: {e}")
                    # warm-up reads to stabilize camera auto exposure
                    try:
                        for _ in range(5):
                            ret, frame = cap.read()
                            if ret:
                                print(f"  ✓ Warmup read {_+1}/5 successful")
                            else:
                                print(f"  ⚠ Warmup read {_+1}/5 failed")
                    except Exception as e:
                        print(f"  ⚠ Error during warmup: {e}")
                    print(f"✓ Camera {idx} initialized successfully!")
                    return cap
                else:
                    if cap:
                        cap.release()
            print("✗ No camera found on any index")
            return None

        try:
            self.cap = open_camera()
            if self.cap and self.cap.isOpened():
                self.camera_available = True
                print("✓ Camera initialized successfully")
            else:
                print("✗ WARNING: Camera could not be opened")
                self.camera_available = False
        except Exception as e:
            print(f"✗ Camera error: {e}")
            self.camera_available = False
        
        self.text_input = ""
        self.selected_key = None
        self.click_detected = False
        self.highlight_timer = 0
        self.current_frame = None
        self.current_hands = []
        
        self.setup_ui()
        if self.camera_available:
            self.start_camera()
        else:
            self.root.after(1000, self.retry_camera)
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(main_frame, text="Hand Gesture Virtual Keyboard", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Full-width camera feed
        self.canvas = Canvas(main_frame, bg="black", width=640, height=480)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bottom status bar
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(status_frame, text="Status: Ready | Point at keys with index finger, FIST to type", 
                                     font=("Arial", 10), fg="green")
        self.status_label.pack(side=tk.LEFT, anchor=tk.W)
        
        tk.Button(status_frame, text="Exit", command=self.close_app, 
                 font=("Arial", 10), bg="red", fg="white", width=10).pack(side=tk.RIGHT, padx=5)
    
    
    def retry_camera(self):
        """Retry camera initialization"""
        if not self.camera_available:
            try:
                print("Attempting to reconnect camera...")
                # Try multiple indices
                for idx in [0, 1, 2, 3]:
                    print(f"  Trying camera index {idx}...")
                    try:
                        self.cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                    except:
                        self.cap = cv2.VideoCapture(idx)
                    
                    if self.cap and self.cap.isOpened():
                        print(f"  ✓ Camera {idx} connected!")
                        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        self.camera_available = True
                        self.status_label.config(text="Status: Camera Connected ✓", fg="green")
                        print("✓ Camera reconnected successfully")
                        self.start_camera()
                        return
                
                # If no camera found
                print("✗ No camera found")
                self.status_label.config(text="Status: Camera Not Found - Retrying...", fg="red")
                self.root.after(3000, self.retry_camera)
            except Exception as e:
                print(f"✗ Camera retry error: {e}")
                self.status_label.config(text=f"Status: Camera Error - Retrying...", fg="red")
                self.root.after(3000, self.retry_camera)
    
    def start_camera(self):
        """Start camera feed in separate thread"""
        self.camera_thread = threading.Thread(target=self.update_camera, daemon=True)
        self.camera_thread.start()
        self.update_display()
    
    def update_camera(self):
        """Update camera frame and detect hands with ULTRA-STABLE video"""
        consecutive_failures = 0
        frame_buffer = []  # Buffer for extreme frame smoothing
        BUFFER_SIZE = 15  # Use 15 frames for EXTREMELY smooth output
        hand_position_buffer = []  # Smooth hand position tracking
        HAND_BUFFER_SIZE = 8
        last_valid_hands = None  # Keep last valid hand detection
        
        while self.cap and self.cap.isOpened():
            try:
                # Use grab/retrieve pattern to reduce latency on some backends
                grabbed = self.cap.grab()
                if not grabbed:
                    consecutive_failures += 1
                else:
                    ret, frame = self.cap.retrieve()
                    if not ret or frame is None:
                        consecutive_failures += 1
                    else:
                        consecutive_failures = 0

                        # Flip frame for selfie-view
                        frame = cv2.flip(frame, 1)
                        
                        # AGGRESSIVE Multi-stage filtering for MAXIMUM noise reduction
                        # Stage 1: Bilateral filter (STRONG) - edge-preserving blur
                        frame = cv2.bilateralFilter(frame, 15, 100, 100)
                        
                        # Stage 2: Strong Gaussian blur - additional smoothing
                        frame = cv2.GaussianBlur(frame, (7, 7), 1.5)
                        
                        # Stage 3: Median blur - remove outliers
                        frame = cv2.medianBlur(frame, 5)
                        
                        # Stage 4: Morphological operations - aggressive noise removal
                        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                        frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
                        frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
                        
                        # Add frame to buffer for smoothing
                        frame_buffer.append(frame.copy())
                        if len(frame_buffer) > BUFFER_SIZE:
                            frame_buffer.pop(0)
                        
                        # Create MAXIMUM smoothed frame - heavily weighted toward older frames
                        if len(frame_buffer) >= 15:
                            # Ultra-aggressive weighting - heavily favor averaging
                            smooth_frame = frame_buffer[0].astype(float) * 0.12
                            smooth_frame += frame_buffer[1].astype(float) * 0.11
                            smooth_frame += frame_buffer[2].astype(float) * 0.10
                            smooth_frame += frame_buffer[3].astype(float) * 0.09
                            smooth_frame += frame_buffer[4].astype(float) * 0.09
                            smooth_frame += frame_buffer[5].astype(float) * 0.08
                            smooth_frame += frame_buffer[6].astype(float) * 0.08
                            smooth_frame += frame_buffer[7].astype(float) * 0.07
                            smooth_frame += frame_buffer[8].astype(float) * 0.06
                            smooth_frame += frame_buffer[9].astype(float) * 0.05
                            smooth_frame += frame_buffer[10].astype(float) * 0.05
                            smooth_frame += frame_buffer[11].astype(float) * 0.04
                            smooth_frame += frame_buffer[12].astype(float) * 0.03
                            smooth_frame += frame_buffer[13].astype(float) * 0.02
                            smooth_frame += frame_buffer[14].astype(float) * 0.01
                            smooth_frame = smooth_frame.astype(np.uint8)
                        elif len(frame_buffer) >= 10:
                            smooth_frame = frame_buffer[0].astype(float) * 0.15
                            smooth_frame += frame_buffer[1].astype(float) * 0.14
                            smooth_frame += frame_buffer[2].astype(float) * 0.13
                            smooth_frame += frame_buffer[3].astype(float) * 0.12
                            smooth_frame += frame_buffer[4].astype(float) * 0.11
                            smooth_frame += frame_buffer[5].astype(float) * 0.10
                            smooth_frame += frame_buffer[6].astype(float) * 0.09
                            smooth_frame += frame_buffer[7].astype(float) * 0.08
                            smooth_frame += frame_buffer[8].astype(float) * 0.07
                            smooth_frame += frame_buffer[9].astype(float) * 0.01
                            smooth_frame = smooth_frame.astype(np.uint8)
                        else:
                            smooth_frame = frame

                        # Detect hands on smoothed frame
                        hands_data = self.gesture_detector.detect(smooth_frame)
                        
                        # Use last valid detection if current is noisy
                        if not hands_data and last_valid_hands:
                            hands_data = last_valid_hands
                        elif hands_data:
                            last_valid_hands = hands_data
                        
                        # AGGRESSIVE hand position smoothing to prevent cursor jitter
                        if hands_data:
                            hand = hands_data[0]
                            index_finger = hand['index_finger']
                            
                            # Add position to buffer
                            hand_position_buffer.append(index_finger)
                            if len(hand_position_buffer) > HAND_BUFFER_SIZE:
                                hand_position_buffer.pop(0)
                            
                            # Compute heavily smoothed position - use median + average
                            if len(hand_position_buffer) > 0:
                                all_x = [pos[0] for pos in hand_position_buffer]
                                all_y = [pos[1] for pos in hand_position_buffer]
                                
                                # Use median to ignore outliers
                                median_x = int(np.median(all_x))
                                median_y = int(np.median(all_y))
                                
                                # Blend median with average for smoother motion
                                avg_x = int(np.mean(all_x))
                                avg_y = int(np.mean(all_y))
                                
                                final_x = int(median_x * 0.6 + avg_x * 0.4)
                                final_y = int(median_y * 0.6 + avg_y * 0.4)
                                
                                hand['index_finger'] = (final_x, final_y)

                        # Draw hand info
                        display_frame = self.gesture_detector.draw_hands(smooth_frame, hands_data)
                        
                        # Draw keyboard overlay on camera with hand position
                        display_frame = self.draw_keyboard_overlay(display_frame, hands_data)

                        # Draw cursor circle at index finger position
                        if hands_data:
                            hand = hands_data[0]
                            # Draw larger cursor
                            cv2.circle(display_frame, hand['index_finger'], 15, (0, 255, 255), 3)
                            cv2.circle(display_frame, hand['index_finger'], 20, (0, 255, 255), 2)

                        # Convert to RGB for display
                        frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(frame_rgb)
                        self.current_frame = ImageTk.PhotoImage(image=img)

                        # Store hands data for key detection
                        self.current_hands = hands_data

                # If camera fails multiple times, attempt to reopen
                if consecutive_failures >= 5:
                    print("Multiple camera read failures, attempting to restart camera")
                    try:
                        self.cap.release()
                    except Exception:
                        pass
                    # try reopening
                    time.sleep(0.5)
                    self.cap = None
                    self.camera_available = False
                    # attempt to re-open with same helper
                    try:
                        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                        if self.cap and self.cap.isOpened():
                            for _ in range(5):
                                self.cap.read()
                            consecutive_failures = 0
                            self.camera_available = True
                            self.status_label.config(text="Status: Camera Reconnected", fg="green")
                        else:
                            self.status_label.config(text="Status: Camera disconnected", fg="red")
                    except Exception as e:
                        print(f"Reopen camera error: {e}")
                        self.status_label.config(text="Status: Camera error", fg="red")
                time.sleep(0.03)  # ~30 FPS
            except Exception as e:
                print(f"Camera update error: {e}")
                self.camera_available = False
                break
                self.camera_available = False
                break
    
    def draw_keyboard_overlay(self, frame, hands_data):
        """Draw virtual keyboard overlay on camera feed"""
        h, w, c = frame.shape
        
        # Define keyboard positions on camera (bottom part)
        keyboard_y_start = int(h * 0.6)  # Start at 60% down
        keyboard_y_end = h
        keyboard_x_start = 0
        keyboard_x_end = w
        
        keyboard_width = keyboard_x_end - keyboard_x_start
        keyboard_height = keyboard_y_end - keyboard_y_start
        
        # Draw semi-transparent background for keyboard area
        overlay = frame.copy()
        cv2.rectangle(overlay, (keyboard_x_start, keyboard_y_start), (keyboard_x_end, keyboard_y_end), 
                     (50, 50, 100), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Draw keyboard grid
        self.keyboard_positions = {}  # Store key positions for detection
        
        key_width = keyboard_width // 10
        key_height = keyboard_height // 4
        
        row_count = 0
        for row_idx, row in enumerate(self.keyboard_layout):
            row_y = keyboard_y_start + row_idx * key_height
            
            # Center align keys
            keys_total_width = len(row) * key_width
            x_offset = (keyboard_width - keys_total_width) // 2
            
            for col_idx, key_label in enumerate(row):
                # Adjust width for special keys
                if key_label == "Space":
                    key_w = key_width * 3
                elif key_label in ["Enter", "Back"]:
                    key_w = key_width * 1.5
                else:
                    key_w = key_width
                
                key_x = keyboard_x_start + x_offset + col_idx * key_width
                key_y = row_y
                
                # Check if hand is pointing at this key
                is_selected = False
                if hands_data:
                    hand = hands_data[0]
                    finger_pos = hand['index_finger']
                    
                    if (key_x <= finger_pos[0] <= key_x + key_w and 
                        key_y <= finger_pos[1] <= key_y + key_height):
                        is_selected = True
                
                # Draw key
                color = (0, 255, 255) if is_selected else (100, 150, 255)  # Yellow if selected, blue otherwise
                thickness = 3 if is_selected else 2
                cv2.rectangle(frame, (int(key_x), int(key_y)), (int(key_x + key_w), int(key_y + key_height)), 
                             color, thickness)
                
                # Draw key label
                font_size = 0.6 if key_label in ["Space", "Enter", "Back"] else 0.8
                cv2.putText(frame, key_label, (int(key_x + 5), int(key_y + key_height - 5)),
                           cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 2)
                
                # Store position for click detection
                self.keyboard_positions[key_label] = {
                    'x': int(key_x),
                    'y': int(key_y),
                    'w': int(key_w),
                    'h': int(key_height)
                }
        
        return frame
    
    def update_display(self):
        """Update canvas with current frame"""
        if hasattr(self, 'current_frame'):
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_frame)
        
        # Check for fist clicks on keyboard overlay
        if hasattr(self, 'current_hands') and self.current_hands:
            hand = self.current_hands[0]
            
            # Detect clicks directly from hand position on camera
            if hand['is_fist']:
                self.detect_click_on_key()
        
        self.root.after(30, self.update_display)
    
    def detect_click_on_key(self):
        """Detect which key was clicked based on hand position in camera"""
        if not hasattr(self, 'current_hands') or not self.current_hands:
            return
        
        hand = self.current_hands[0]
        finger_pos = hand['index_finger']
        
        # Check if fist is closed (click detected)
        if hand['is_fist']:
            # Find which key was clicked using stored keyboard positions
            if hasattr(self, 'keyboard_positions'):
                for key_label, pos in self.keyboard_positions.items():
                    if (pos['x'] <= finger_pos[0] <= pos['x'] + pos['w'] and 
                        pos['y'] <= finger_pos[1] <= pos['y'] + pos['h']):
                        print(f"Clicking key: {key_label}")
                        self.key_press(key_label)
                        return
            else:
                # Fallback: use the old UI button detection
                try:
                    for key_label, btn in self.key_buttons.items():
                        btn_x = btn.winfo_x()
                        btn_y = btn.winfo_y()
                        btn_w = btn.winfo_width()
                        btn_h = btn.winfo_height()
                        
                        # Check if click is within button bounds
                        if (btn_x <= finger_pos[0] <= btn_x + btn_w and 
                            btn_y <= finger_pos[1] <= btn_y + btn_h):
                            self.key_press(key_label)
                            # Visual feedback
                            btn.config(bg="green", relief=tk.SUNKEN)
                            self.root.after(100, lambda b=btn: b.config(bg="lightblue", relief=tk.RAISED))
                            return
                except:
                    pass
    
    def key_press(self, key):
        """Handle key press"""
        if key == "Space":
            self.text_input += " "
        elif key == "Back":
            self.text_input = self.text_input[:-1]
        elif key == "Enter":
            # Could send signal to main app
            pass
        else:
            self.text_input += key
    
    def close_app(self):
        """Close the application"""
        if self.cap:
            self.cap.release()
        self.gesture_detector.release()
        self.root.quit()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def start_virtual_keyboard():
    """Start the virtual keyboard application"""
    root = tk.Tk()
    app = VirtualKeyboard(root)
    app.run()

if __name__ == "__main__":
    start_virtual_keyboard()
