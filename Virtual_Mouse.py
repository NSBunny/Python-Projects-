# Import necessary libraries/modules
import cv2 # OpenCV for computer vision
import mediapipe as mp # Mediapipe for hand tracking
import pyautogui # PyAutoGUI for controlling the mouse
import time # For timing operations
 # Custom module for hand tracking

# Initialize the webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 22280)
cap.set(4,22280)
# Initialize the hand detector from Mediapipe
hand_detector = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils
# Get the screen width and height using PyAutoGUI
screen_width, screen_height = pyautogui.size()
index_y = 0
# Start an infinite loop which continuously process frames from the webcam
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame) # Process the frame to detect hands
    hands = output.multi_hand_landmarks # Get the detected hand landmarks
    if hands:
        for hand in hands:
            draw.draw_landmarks(frame, hand) # Draw landmarks on the frame
            landmarks = hand.landmark # Draw landmarks on the frame
            # Iterate through landmarks
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                if id == 8:
                    cv2.circle(img=frame, center =(x,y), radius=10, color=(0,255,255)) # Draw a circle at the index finger tip
                    # Draw a circle at the index finger tip
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                    pyautogui.moveTo(index_x, index_y)  # Move the mouse cursor to the calculated position

                if id == 12:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    # Calculate the corresponding screen coordinates
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('outside ', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 40:
                        pyautogui.click() # Simulate a mouse click
                        pyautogui.sleep(1000)
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y) # Move the mouse cursor
    cv2.imshow('Virtual Mouse', frame)
    key = cv2.waitKey(30) # Check for a key press (27 corresponds to the "Esc" key
    if key == 27:
        break
# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()