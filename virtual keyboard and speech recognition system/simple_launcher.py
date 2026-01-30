#!/usr/bin/env python
"""
Simple Hand Gesture Virtual Keyboard Launcher
Direct launch with minimal UI
"""

import tkinter as tk
from tkinter import messagebox, Button, Label, Frame
import threading
import time
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from virtual_keyboard import VirtualKeyboard


def launch_keyboard():
    """Launch the virtual keyboard"""
    print("\n" + "="*60)
    print("🎥 LAUNCHING HAND GESTURE VIRTUAL KEYBOARD")
    print("="*60)
    print("Loading keyboard interface...")
    
    try:
        # Create keyboard window
        keyboard_root = tk.Toplevel(launcher_root)
        keyboard_app = VirtualKeyboard(keyboard_root)
        
        # Update status
        status_label.config(text="✓ Keyboard is running!", fg="green")
        print("✓ Keyboard interface loaded successfully!")
        print("="*60)
        
    except Exception as e:
        error_msg = f"Failed to launch keyboard:\n{str(e)}"
        print(f"✗ Error: {error_msg}")
        messagebox.showerror("Launch Error", error_msg)
        status_label.config(text="✗ Error loading keyboard", fg="red")


def main():
    """Main launcher interface"""
    global launcher_root, status_label
    
    print("\n" + "="*60)
    print("HAND GESTURE VIRTUAL KEYBOARD - LAUNCHER")
    print("="*60)
    
    launcher_root = tk.Tk()
    launcher_root.title("Hand Gesture Virtual Keyboard - Launcher")
    launcher_root.geometry("600x500")
    launcher_root.configure(bg="#2c3e50")
    
    # Make window always on top initially
    launcher_root.attributes('-topmost', True)
    
    # Center window
    launcher_root.update_idletasks()
    width = launcher_root.winfo_width()
    height = launcher_root.winfo_height()
    x = (launcher_root.winfo_screenwidth() // 2) - (width // 2)
    y = (launcher_root.winfo_screenheight() // 2) - (height // 2)
    launcher_root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Title
    title_frame = Frame(launcher_root, bg="#2c3e50", height=80)
    title_frame.pack(fill="x", padx=0, pady=0)
    
    title_label = Label(
        title_frame,
        text="🎮 Hand Gesture Virtual Keyboard",
        font=("Arial", 26, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title_label.pack(pady=20)
    
    # Content frame
    content_frame = Frame(launcher_root, bg="#ecf0f1")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Instructions
    instructions = Label(
        content_frame,
        text="""HOW TO USE:

1. Click the "Launch Keyboard" button below
2. Wait for the keyboard window to open
3. Position your hand in front of the camera
4. Point your index finger at keys
5. Make a fist to click/select keys
6. Watch your text appear!

QUICK TIPS:
• Keep your hand fully visible in camera
• Point clearly at each key
• Make a complete fist to click
• Use Space for spaces, Back to delete

SPECIAL KEYS:
• Space - Add a space
• Back - Delete last character
• Enter - Confirm input
• Clear - Clear all text
• Exit - Close the keyboard""",
        font=("Arial", 11),
        bg="#ecf0f1",
        justify="left",
        wraplength=500
    )
    instructions.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Button frame
    button_frame = Frame(content_frame, bg="#ecf0f1")
    button_frame.pack(pady=20)
    
    # Status label
    status_label = Label(
        button_frame,
        text="✓ Ready to launch",
        font=("Arial", 11, "bold"),
        bg="#ecf0f1",
        fg="#27ae60"
    )
    status_label.pack(pady=10)
    
    # Launch button
    launch_btn = Button(
        button_frame,
        text="🎥 LAUNCH KEYBOARD",
        command=launch_keyboard,
        font=("Arial", 14, "bold"),
        bg="#27ae60",
        fg="white",
        padx=40,
        pady=15,
        relief="raised",
        cursor="hand2",
        activebackground="#229954"
    )
    launch_btn.pack(side="left", padx=10)
    
    # Exit button
    exit_btn = Button(
        button_frame,
        text="❌ EXIT",
        command=launcher_root.quit,
        font=("Arial", 12, "bold"),
        bg="#e74c3c",
        fg="white",
        padx=30,
        pady=10,
        relief="raised",
        cursor="hand2",
        activebackground="#c0392b"
    )
    exit_btn.pack(side="left", padx=10)
    
    # Allow window to be focused
    launcher_root.after(100, lambda: launcher_root.attributes('-topmost', False))
    
    print("✓ Launcher window created")
    print("✓ Waiting for user input...")
    print("="*60)
    
    launcher_root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
