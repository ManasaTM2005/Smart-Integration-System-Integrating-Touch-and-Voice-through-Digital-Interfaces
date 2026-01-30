import os
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume',1.0) 
    voices = engine.getProperty('voices')  
    # Use voice index 1 if available, otherwise use index 0
    voice_index = min(1, len(voices) - 1) if voices else 0
    if voices:
        engine.setProperty('voice', voices[voice_index].id)  
    engine.say(text)
    engine.runAndWait()