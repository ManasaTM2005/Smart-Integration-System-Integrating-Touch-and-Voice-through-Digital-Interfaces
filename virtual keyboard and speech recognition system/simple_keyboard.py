import cv2
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import threading
import time

class SimpleVirtualKeyboard:
    """Simple virtual keyboard interface with camera feed"""
    
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
        
        # Try to initialize camera
        self.cap = None
        self.camera_available = False
        try:
            def open_camera_simple():
                for idx in (0, 1, 2, 3):
                    try:
                        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                    except Exception:
                        try:
                            cap = cv2.VideoCapture(idx)
                        except Exception:
                            cap = None
                    if cap and cap.isOpened():
                        try:
                            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                            cap.set(cv2.CAP_PROP_FPS, 15)
                        except Exception:
                            pass
                        for _ in range(5):
                            cap.read()
                        return cap
                return None

            self.cap = open_camera_simple()
            if self.cap and self.cap.isOpened():
                self.camera_available = True
                print("[OK] Camera initialized")
            else:
                print("[WARNING] Camera could not be opened - will display black screen")
        except Exception as e:
            print(f"[WARNING] Camera initialization failed: {e}")
            self.camera_available = False
        
        self.text_input = ""
        self.current_frame = None
        self.camera_running = True
        
        self.setup_ui()
        if self.camera_available:
            self.start_camera()
        
    def setup_ui(self):
        """Setup the user interface"""
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Camera feed
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text="Camera Feed", font=("Arial", 12, "bold")).pack()
        self.canvas = Canvas(left_frame, bg="black", width=640, height=480)
        self.canvas.pack()
        
        # Right side - Keyboard and text
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)
        
        # Text display
        tk.Label(right_frame, text="Typed Text:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        self.text_display = tk.Entry(right_frame, font=("Arial", 14), width=40)
        self.text_display.pack(pady=10)
        
        # Status
        status_text = "Camera: OK" if self.camera_available else "Camera: NOT FOUND"
        status_color = "green" if self.camera_available else "red"
        self.status_label = tk.Label(right_frame, text=f"Status: {status_text}", 
                                     font=("Arial", 10), fg=status_color)
        self.status_label.pack(anchor=tk.W)
        
        # Instructions
        tk.Label(right_frame, text="Instructions:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(20, 5))
        instructions = """
1. Click on keys to type (mouse control)
2. Or use keyboard to type
3. Use 'Back' to delete
4. Use 'Space' for spaces
5. Use 'Enter' to confirm
6. Camera shows live feed
        """
        tk.Label(right_frame, text=instructions, font=("Arial", 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Virtual Keyboard
        tk.Label(right_frame, text="Virtual Keyboard:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(20, 10))
        
        self.keyboard_frame = tk.Frame(right_frame)
        self.keyboard_frame.pack(fill=tk.BOTH, expand=True)
        
        self.key_buttons = {}
        self.create_keyboard()
        
        # Control buttons
        button_frame = tk.Frame(right_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Clear", command=self.clear_text, 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Exit", command=self.close_app, 
                 font=("Arial", 10), width=15, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
    
    def create_keyboard(self):
        """Create the virtual keyboard buttons"""
        for row in self.keyboard_layout:
            row_frame = tk.Frame(self.keyboard_frame)
            row_frame.pack(pady=3, fill=tk.X)
            
            for key_label in row:
                if key_label == "Space":
                    width = 25
                elif key_label in ["Enter", "Back"]:
                    width = 10
                else:
                    width = 4
                
                btn = tk.Button(row_frame, text=key_label, font=("Arial", 10, "bold"),
                               width=width, height=2, bg="lightblue", 
                               command=lambda k=key_label: self.key_press(k))
                btn.pack(side=tk.LEFT, padx=2)
                self.key_buttons[key_label] = btn
    
    def start_camera(self):
        """Start camera feed in separate thread"""
        self.camera_thread = threading.Thread(target=self.update_camera, daemon=True)
        self.camera_thread.start()
        self.update_display()
    
    def update_camera(self):
        """Update camera frame"""
        while self.camera_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Add text overlay
                cv2.putText(frame, "Hand Gesture Keyboard", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Click keys to type or use mouse", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
                
                # Convert to PIL Image
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                self.current_frame = ImageTk.PhotoImage(image=img)
                
                time.sleep(0.03)
            except Exception as e:
                print(f"Camera error: {e}")
                break
    
    def update_display(self):
        """Update canvas with current frame"""
        if self.current_frame:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_frame)
        
        self.text_display.delete(0, tk.END)
        self.text_display.insert(0, self.text_input)
        
        self.root.after(30, self.update_display)
    
    def key_press(self, key):
        """Handle key press"""
        if key == "Space":
            self.text_input += " "
        elif key == "Back":
            self.text_input = self.text_input[:-1]
        elif key == "Enter":
            print("Text entered:", self.text_input)
        else:
            self.text_input += key
    
    def clear_text(self):
        """Clear all text"""
        self.text_input = ""
    
    def close_app(self):
        """Close the application"""
        self.camera_running = False
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
        self.root.quit()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def start_virtual_keyboard():
    """Start the virtual keyboard application"""
    root = tk.Tk()
    app = SimpleVirtualKeyboard(root)
    app.run()

if __name__ == "__main__":
    start_virtual_keyboard()
import cv2
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import threading
import time

class SimpleVirtualKeyboard:
    """Simple virtual keyboard interface with camera feed"""
    
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
        
        # Try to initialize camera
        self.cap = None
        self.camera_available = False
        try:
            def open_camera_simple():
                for idx in (0, 1, 2, 3):
                    try:
                        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                    except Exception:
                        try:
                            cap = cv2.VideoCapture(idx)
                        except Exception:
                            cap = None
                    if cap and cap.isOpened():
                        try:
                            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                            cap.set(cv2.CAP_PROP_FPS, 15)
                        except Exception:
                            pass
                        for _ in range(5):
                            cap.read()
                        return cap
                return None

            self.cap = open_camera_simple()
            if self.cap and self.cap.isOpened():
                self.camera_available = True
                print("[OK] Camera initialized")
            else:
                print("[WARNING] Camera could not be opened - will display black screen")
        except Exception as e:
            print(f"[WARNING] Camera initialization failed: {e}")
            self.camera_available = False
        
        self.text_input = ""
        self.current_frame = None
        self.camera_running = True
        
        self.setup_ui()
        if self.camera_available:
            self.start_camera()
        
    def setup_ui(self):
        """Setup the user interface"""
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Camera feed
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text="Camera Feed", font=("Arial", 12, "bold")).pack()
        self.canvas = Canvas(left_frame, bg="black", width=640, height=480)
        self.canvas.pack()
        
        # Right side - Keyboard and text
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)
        
        # Text display
        tk.Label(right_frame, text="Typed Text:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        self.text_display = tk.Entry(right_frame, font=("Arial", 14), width=40)
        self.text_display.pack(pady=10)
        
        # Status
        status_text = "Camera: OK" if self.camera_available else "Camera: NOT FOUND"
        status_color = "green" if self.camera_available else "red"
        self.status_label = tk.Label(right_frame, text=f"Status: {status_text}", 
                                     font=("Arial", 10), fg=status_color)
        self.status_label.pack(anchor=tk.W)
        
        # Instructions
        tk.Label(right_frame, text="Instructions:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(20, 5))
        instructions = """
1. Click on keys to type (mouse control)
2. Or use keyboard to type
3. Use 'Back' to delete
4. Use 'Space' for spaces
5. Use 'Enter' to confirm
6. Camera shows live feed
        """
        tk.Label(right_frame, text=instructions, font=("Arial", 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Virtual Keyboard
        tk.Label(right_frame, text="Virtual Keyboard:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(20, 10))
        
        self.keyboard_frame = tk.Frame(right_frame)
        self.keyboard_frame.pack(fill=tk.BOTH, expand=True)
        
        self.key_buttons = {}
        self.create_keyboard()
        
        # Control buttons
        button_frame = tk.Frame(right_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Clear", command=self.clear_text, 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Exit", command=self.close_app, 
                 font=("Arial", 10), width=15, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
    
    def create_keyboard(self):
        """Create the virtual keyboard buttons"""
        for row in self.keyboard_layout:
            row_frame = tk.Frame(self.keyboard_frame)
            row_frame.pack(pady=3, fill=tk.X)
            
            for key_label in row:
                if key_label == "Space":
                    width = 25
                elif key_label in ["Enter", "Back"]:
                    width = 10
                else:
                    width = 4
                
                btn = tk.Button(row_frame, text=key_label, font=("Arial", 10, "bold"),
                               width=width, height=2, bg="lightblue", 
                               command=lambda k=key_label: self.key_press(k))
                btn.pack(side=tk.LEFT, padx=2)
                self.key_buttons[key_label] = btn
    
    def start_camera(self):
        """Start camera feed in separate thread"""
        self.camera_thread = threading.Thread(target=self.update_camera, daemon=True)
        self.camera_thread.start()
        self.update_display()
    
    def update_camera(self):
        """Update camera frame"""
        while self.camera_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Add text overlay
                cv2.putText(frame, "Hand Gesture Keyboard", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, "Click keys to type or use mouse", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
                
                # Convert to PIL Image
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                self.current_frame = ImageTk.PhotoImage(image=img)
                
                time.sleep(0.03)
            except Exception as e:
                print(f"Camera error: {e}")
                break
    
    def update_display(self):
        """Update canvas with current frame"""
        if self.current_frame:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_frame)
        
        self.text_display.delete(0, tk.END)
        self.text_display.insert(0, self.text_input)
        
        self.root.after(30, self.update_display)
    
    def key_press(self, key):
        """Handle key press"""
        if key == "Space":
            self.text_input += " "
        elif key == "Back":
            self.text_input = self.text_input[:-1]
        elif key == "Enter":
            print("Text entered:", self.text_input)
        else:
            self.text_input += key
    
    def clear_text(self):
        """Clear all text"""
        self.text_input = ""
    
    def close_app(self):
        """Close the application"""
        self.camera_running = False
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
        self.root.quit()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def start_virtual_keyboard():
    """Start the virtual keyboard application"""
    root = tk.Tk()
    app = SimpleVirtualKeyboard(root)
    app.run()

if __name__ == "__main__":
    start_virtual_keyboard()
