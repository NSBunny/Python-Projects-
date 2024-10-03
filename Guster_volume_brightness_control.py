import cv2
import mediapipe as mp
import pyautogui
import screen_brightness_control
from math import hypot
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Hand volume control
    output_hands = hands.process(frame_rgb)
    landmark_list = []
    if output_hands.multi_hand_landmarks:
        for hand_landmarks in output_hands.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                height, width, color_channels = frame.shape
                x, y = int(landmark.x * width), int(landmark.y * height)
                landmark_list.append([id, x, y])
            
            draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    if landmark_list != []:
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[12][1], landmark_list[12][2]
        
        cv2.circle(frame, (x1, y1), 7, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 7, (0, 255, 0), cv2.FILLED)
        
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
        dist = hypot(x2 - x1, y2 - y1) // 4
        if dist > 40:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")
    
    # Hand brightness control
    output_brightness = hands.process(frame_rgb)
    landmark_list = []
    if output_brightness.multi_hand_landmarks:
        for hand_landmarks in output_brightness.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                height, width, color_channels = frame.shape
                x, y = int(landmark.x * width), int(landmark.y * height)
                landmark_list.append([id, x, y])
            
            draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    if landmark_list != []:
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]
        
        cv2.circle(frame, (x1, y1), 7, (255, 0, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 7, (255, 0, 0), cv2.FILLED)
        
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        
        length = hypot(x2 - x1, y2 - y1)
        brightness_level = np.interp(length, [15, 220], [0, 100])
        screen_brightness_control.set_brightness(int(brightness_level))
    
    cv2.imshow('Hand Control', frame)
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
