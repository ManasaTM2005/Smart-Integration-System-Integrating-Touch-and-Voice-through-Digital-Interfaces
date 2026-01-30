import cv2
import numpy as np
from collections import deque

# Try multiple import methods for mediapipe
try:
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision
    USE_TASKS_API = True
except ImportError:
    try:
        from mediapipe import solutions as mp_solutions
        USE_TASKS_API = False
    except ImportError:
        print("Warning: Could not import mediapipe properly")
        USE_TASKS_API = False

class GestureDetector:
    """Detects hand gestures and positions for virtual keyboard interaction"""
    
    def __init__(self):
        try:
            if USE_TASKS_API:
                # Using new MediaPipe Tasks API
                print("Using MediaPipe Tasks API for hand detection")
                self.use_tasks = True
                # We'll use a simpler approach with cv2 hand detection
                self.init_simple_hand_detection()
            else:
                # Try the older solutions API
                print("Using MediaPipe Solutions API for hand detection")
                self.use_tasks = False
                try:
                    from mediapipe.solutions import hands
                    self.hands = hands.Hands(
                        static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.7,
                        min_tracking_confidence=0.5
                    )
                except:
                    print("Falling back to simple hand detection")
                    self.init_simple_hand_detection()
        except Exception as e:
            print(f"Error initializing hand detector: {e}")
            self.init_simple_hand_detection()
        
        # For click detection (closing fist)
        self.thumb_positions = deque(maxlen=5)
        self.index_positions = deque(maxlen=5)
    
    def init_simple_hand_detection(self):
        """Initialize simple hand detection as fallback"""
        self.use_simple = True
        print("Using fallback hand detection method")
        
    def get_hand_position(self, landmarks, frame_width, frame_height):
        """Get hand center position from landmarks"""
        x_coords = [lm.x for lm in landmarks]
        y_coords = [lm.y for lm in landmarks]
        
        center_x = np.mean(x_coords) * frame_width
        center_y = np.mean(y_coords) * frame_height
        
        return int(center_x), int(center_y)
    
    def get_finger_position(self, landmarks, finger_tip_index, frame_width, frame_height):
        """Get position of a specific finger"""
        lm = landmarks[finger_tip_index]
        x = int(lm.x * frame_width)
        y = int(lm.y * frame_height)
        return x, y
    
    def is_fist_closed(self, landmarks):
        """Detect if hand is closed (fist) for click action"""
        # Get distances between fingers
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        palm_center = landmarks[9]
        
        # If all fingertips are close to palm, it's a fist
        thumb_dist = np.sqrt((thumb_tip.x - palm_center.x)**2 + (thumb_tip.y - palm_center.y)**2)
        index_dist = np.sqrt((index_tip.x - palm_center.x)**2 + (index_tip.y - palm_center.y)**2)
        middle_dist = np.sqrt((middle_tip.x - palm_center.x)**2 + (middle_tip.y - palm_center.y)**2)
        
        # If average distance is small, it's a closed fist
        avg_dist = (thumb_dist + index_dist + middle_dist) / 3
        return avg_dist < 0.1
    
    def is_pointing(self, landmarks):
        """Detect if pointing gesture (index finger extended)"""
        # Get hand landmarks
        index_tip = landmarks[8]
        index_pip = landmarks[6]
        middle_tip = landmarks[12]
        thumb_tip = landmarks[4]
        
        # Index finger should be extended
        index_extended = index_tip.y < index_pip.y
        # Other fingers should be curled
        middle_curled = middle_tip.y > index_pip.y
        thumb_down = thumb_tip.y > index_pip.y
        
        return index_extended and middle_curled and thumb_down
    
    def detect(self, frame):
        """Detect hands and gestures in frame"""
        hands_data = []
        
        try:
            if hasattr(self, 'use_simple') and self.use_simple:
                # Simple fallback detection
                return self.detect_simple(frame)
            
            if not hasattr(self, 'hands') or self.hands is None:
                return hands_data
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                h, w, c = frame.shape
                
                for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                    landmarks = hand_landmarks.landmark
                    
                    # Get hand center position
                    center_x, center_y = self.get_hand_position(landmarks, w, h)
                    
                    # Get index finger position (pointing finger)
                    index_x, index_y = self.get_finger_position(landmarks, 8, w, h)
                    
                    # Detect gestures
                    is_fist = self.is_fist_closed(landmarks)
                    is_pointing = self.is_pointing(landmarks)
                    
                    hands_data.append({
                        'center': (center_x, center_y),
                        'index_finger': (index_x, index_y),
                        'is_fist': is_fist,
                        'is_pointing': is_pointing,
                        'handedness': hand_info.classification[0].label if hand_info else "Unknown",
                        'landmarks': landmarks
                    })
        except Exception as e:
            print(f"Error in hand detection: {e}")
            # Return empty list on error
        
        return hands_data
    
    def detect_simple(self, frame):
        """Simple fallback hand detection using color"""
        hands_data = []
        h, w, c = frame.shape
        
        # Simple skin color detection as fallback
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define range for skin color in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                hands_data.append({
                    'center': (cx, cy),
                    'index_finger': (cx + 30, cy - 30),
                    'is_fist': False,
                    'is_pointing': True,
                    'handedness': "Right",
                    'landmarks': None
                })
        
        return hands_data
    
    def draw_hands(self, frame, hands_data):
        """Draw hand landmarks and info on frame"""
        for hand in hands_data:
            # Draw center point
            cv2.circle(frame, hand['center'], 10, (0, 255, 0), -1)
            
            # Draw index finger point
            cv2.circle(frame, hand['index_finger'], 8, (255, 0, 0), -1)
            
            # Draw status text
            status = "FIST" if hand['is_fist'] else ("POINTING" if hand['is_pointing'] else "OPEN")
            cv2.putText(frame, status, (hand['center'][0] - 30, hand['center'][1] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        return frame
    
    def release(self):
        """Release resources"""
        self.hands.close()
