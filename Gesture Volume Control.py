import cv2  # display an image in a window.
import mediapipe as mp  # we use mediapipe for handtracking
import pyautogui  # controling the system's volume

# Declaring variables and objects
x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()  # tracking hands
drawing_utils = mp.solutions.drawing_utils
# Running a while loop to continuously process frames from the webcam
while True:
    _, image = webcam.read()
    image = cv2.flip(image, 1)  # flip frame
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # converting color BGR to RGB
    output = my_hands.process(rgb_image)  # Process the image with hand tracking
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)  # Draw landmarks on the image
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                # Get the pixel coordinates of the landmark
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    # Draw a circle at the fingertip position
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=9)
                    x1 = x
                    y1 = y
                if id == 4:
                    # Draw a circle at the fingertip position
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=9)
                    x2 = x
                    y2 = y
        # Calculate the distance between the two fingertip points
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (0.5) // 4
        cv2.line(image, (x1, y1), (x2, y2), (0, 265, 0), 4)  # Draw a lines between two fingertips
        if dist > 40:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")

    # Display the image in a window titled "Hand volume control using python
    cv2.imshow("Hand volume control using python", image)
    key = cv2.waitKey(30)
    if key == 27:
        break
webcam.release()
cv2.destroyAllWindows()
