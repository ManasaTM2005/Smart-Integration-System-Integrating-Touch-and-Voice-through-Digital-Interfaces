#!/usr/bin/env python
"""
Hand Gesture Virtual Keyboard Interface
Allows users to type using hand gestures detected by webcam
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
from virtual_keyboard import VirtualKeyboard


class GestureKeyboardInterface:
    """Main interface for launching gesture-controlled keyboard"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hand Gesture Virtual Keyboard Interface")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        self.keyboard_app = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the interface UI"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame, 
            text="Hand Gesture Virtual Keyboard",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Status label
        self.status_label = tk.Label(
            content_frame,
            text="Ready to start",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#27ae60"
        )
        self.status_label.pack(pady=10)
        
        # Instructions frame
        instructions_frame = tk.LabelFrame(
            content_frame,
            text="How to Use",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            padx=15,
            pady=15
        )
        instructions_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        instructions_text = """
1. Click "Launch Keyboard" to open the interface
2. Position your hand in front of the webcam
3. Point your index finger at the key you want
4. Close your fist (make a fist) to select the key
5. Watch your text appear in the display area above
6. Use Special Keys:
   • Space: Add a space
   • Back: Delete last character
   • Enter: Confirm input
   • Clear: Clear all text

Tips:
• Make sure your hand is visible in the camera
• Point clearly at keys for accurate detection
• Close your hand fully for clicks to register
• Keep good lighting for better hand detection
        """
        
        instructions_label = tk.Label(
            instructions_frame,
            text=instructions_text,
            font=("Arial", 10),
            bg="#ecf0f1",
            justify=tk.LEFT,
            wraplength=400
        )
        instructions_label.pack(anchor=tk.W)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Launch button
        launch_button = tk.Button(
            button_frame,
            text="🎥 Launch Keyboard",
            command=self.launch_keyboard,
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=15,
            relief=tk.RAISED,
            cursor="hand2"
        )
        launch_button.pack(side=tk.LEFT, padx=10)
        
        # Settings button (placeholder for future)
        settings_button = tk.Button(
            button_frame,
            text="⚙️ Settings",
            command=self.show_settings,
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        settings_button.pack(side=tk.LEFT, padx=10)
        
        # Exit button
        exit_button = tk.Button(
            button_frame,
            text="❌ Exit",
            command=self.root.quit,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            cursor="hand2"
        )
        exit_button.pack(side=tk.LEFT, padx=10)
    
    def launch_keyboard(self):
        """Launch the virtual keyboard application"""
        self.status_label.config(
            text="Starting keyboard interface...",
            fg="#f39c12"
        )
        self.root.update()
        
        try:
            # Create keyboard app in a separate thread to keep UI responsive
            def start_keyboard():
                try:
                    keyboard_root = tk.Toplevel(self.root)
                    self.keyboard_app = VirtualKeyboard(keyboard_root)
                    self.keyboard_app.run()
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Failed to launch keyboard:\n{str(e)}"
                    )
                    self.status_label.config(
                        text=f"Error: {str(e)[:50]}",
                        fg="#e74c3c"
                    )
            
            keyboard_thread = threading.Thread(target=start_keyboard, daemon=True)
            keyboard_thread.start()
            
            time.sleep(2)  # Give app time to start
            self.status_label.config(
                text="Keyboard interface is running",
                fg="#27ae60"
            )
        except Exception as e:
            messagebox.showerror(
                "Launch Error",
                f"Failed to launch keyboard:\n{str(e)}"
            )
            self.status_label.config(
                text=f"Error: {str(e)[:50]}",
                fg="#e74c3c"
            )
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo(
            "Settings",
            "Settings panel coming soon!\n\n" +
            "Future features:\n" +
            "• Camera selection\n" +
            "• Gesture sensitivity\n" +
            "• Keyboard layout customization\n" +
            "• Display preferences"
        )
    
    def run(self):
        """Run the interface"""
        self.root.mainloop()


def launch_interface():
    """Launch the gesture keyboard interface"""
    interface = GestureKeyboardInterface()
    interface.run()


if __name__ == "__main__":
    launch_interface()
