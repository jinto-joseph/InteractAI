import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui
import sys

class GestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = None
        self.mp_draw = mp.solutions.drawing_utils
        self.cap = None
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.5
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x = 0
        self.prev_y = 0
        self.y_history = []  

    def initialize(self):
        print("Initializing Gesture Controller...")
        try:
            self.hands = self.mp_hands.Hands(
                max_num_hands=2,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open webcam.")
            print("Initialization successful. Starting gesture control...")
            return True
        except Exception as e:
            print(f"Error during initialization: {e}")
            return False

    def count_fingers(self, landmarks, hand_type):
        fingers = []
        if hand_type == "Right":
            fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)  
        else:
            fingers.append(1 if landmarks[4].x > landmarks[3].x else 0)
        finger_tips = [8, 12, 16, 20]
        finger_bases = [6, 10, 14, 18]
        for tip, base in zip(finger_tips, finger_bases):
            fingers.append(1 if landmarks[tip].y < landmarks[base].y else 0)
        return fingers  

    def control_system(self, right_fingers=None, left_fingers=None, right_landmarks=None, left_landmarks=None, frame_width=None, frame_height=None):
        current_time = time.time()

    
        if right_landmarks:
            index_tip = right_landmarks[8]
            x = int(index_tip.x * frame_width)
            y = int(index_tip.y * frame_height)
            screen_x = np.interp(x, [0, frame_width], [0, self.screen_width])
            screen_y = np.interp(y, [0, frame_height], [0, self.screen_height])
            screen_x = self.prev_x + (screen_x - self.prev_x) * 0.2 if self.prev_x else screen_x
            screen_y = self.prev_y + (screen_y - self.prev_y) * 0.2 if self.prev_y else screen_y
            self.prev_x, self.prev_y = screen_x, screen_y
            pyautogui.moveTo(screen_x, screen_y)

           
            self.y_history.append(y)
            if len(self.y_history) > 5: 
                self.y_history.pop(0)

        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None

        action = None

     
        if right_fingers and right_landmarks:
            thumb_up, index_up, middle_up, ring_up, pinky_up = right_fingers
            all_fingers_up = thumb_up and index_up and middle_up and ring_up and pinky_up
        
            if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
                pyautogui.click()
                action = "Left Click"
         
            elif index_up and middle_up and not thumb_up and not ring_up and not pinky_up:
                pyautogui.rightClick()
                action = "Right Click"
            
            elif index_up and thumb_up and not middle_up and not ring_up and not pinky_up:
                pyautogui.doubleClick()
                action = "Double Click"
           
            elif not thumb_up and index_up and middle_up and ring_up and pinky_up:
                pyautogui.scroll(800)  
                action = "Scroll Up"
           
            elif not thumb_up and index_up and middle_up and ring_up and not pinky_up:
                pyautogui.scroll(-800)  
                action = "Scroll Down"
         
            elif all_fingers_up and len(self.y_history) >= 5:
                y_diff = self.y_history[-1] - self.y_history[0]
                if y_diff > 50: 
                    pyautogui.press('volumedown')
                    action = "Volume Down"
                elif abs(y_diff) < 20:
                    pyautogui.press('volumeup')
                    action = "Volume Up"

        
        if left_fingers:
            thumb_up, index_up, middle_up, ring_up, pinky_up = left_fingers

            if middle_up and not thumb_up and not index_up and not ring_up and not pinky_up:
                pyautogui.hotkey('alt', 'f4')
                action = "Shutdown"
        
            elif index_up and not thumb_up and not middle_up and not ring_up and not pinky_up:
                pyautogui.hotkey('win', 'm')
                action = "Minimize"
         
            elif index_up and middle_up and not thumb_up and not ring_up and not pinky_up:
                pyautogui.hotkey('win', 'up')
                action = "Maximize/Restore"
       
            elif index_up and pinky_up and not thumb_up and not middle_up and not ring_up:
                pyautogui.hotkey('ctrl', '+')
                action = "Zoom In"
          
            elif pinky_up and not thumb_up and not index_up and not middle_up and not ring_up:
                pyautogui.hotkey('ctrl', '-')
                action = "Zoom Out"

        if action:
            self.last_gesture_time = current_time
            time.sleep(1)  
            self.y_history.clear() 
            return action

        return None

    def run(self):
        if not self.initialize():
            return
        print("Controls:")
        print("Right Hand Gestures:")
        print("  - Left Click: Thumb up only")
        print("  - Right Click: Index + Middle up")
        print("  - Double Click: Index + Thumb up")
        print("  - Scroll Up: Index + Middle + Ring + Pinky up (Fast)")
        print("  - Scroll Down: Index + Middle + Ring up (Fast)")
        print("  - Volume Up: All fingers up (Thumb + Index + Middle + Ring + Pinky), hold steady")
        print("  - Volume Down: All fingers up + move hand downward")
        print("  - Mouse Move: Any right hand movement (tracks index finger tip)")
        print("Left Hand Gestures:")
        print("  - Shutdown: Middle up only")
        print("  - Minimize: Index up only")
        print("  - Maximize/Restore: Index + Middle up")
        print("  - Zoom In: Index + Pinky up")
        print("  - Zoom Out: Pinky up only")
        print("Press 'q' to quit.")
        
        while True:
            success, frame = self.cap.read()
            if not success:
                print("Error: Could not read frame from webcam.")
                break
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_height, frame_width = frame.shape[:2]
            results = self.hands.process(frame_rgb)

            right_fingers, left_fingers = None, None
            right_landmarks, left_landmarks = None, None

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    hand_type = handedness.classification[0].label
                    fingers = self.count_fingers(hand_landmarks.landmark, hand_type)
                    if hand_type == "Right":
                        right_fingers = fingers
                        right_landmarks = hand_landmarks.landmark
                    elif hand_type == "Left":
                        left_fingers = fingers
                        left_landmarks = hand_landmarks.landmark
                    finger_count = sum(fingers)
                    cv2.putText(frame, f'{hand_type} Fingers: {finger_count}', (10 if hand_type == "Left" else 150, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                action = self.control_system(right_fingers, left_fingers, right_landmarks, left_landmarks, frame_width, frame_height)
                if action:
                    cv2.putText(frame, f'Action: {action}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('Gesture Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Gesture Controller stopped.")

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    controller = GestureController()
    controller.run()
