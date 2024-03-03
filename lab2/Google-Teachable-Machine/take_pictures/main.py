import cv2
import time

# IP camera URL
ip_camera_url = "http://192.168.195.188:4747/video"

# Open a connection to the IP camera
cap = cv2.VideoCapture(ip_camera_url)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Unable to connect to the IP camera.")
    exit()

# Set the desired frame rate (FPS)
fps = 10
delay = 1 / fps

# Loop to continuously capture frames
frame_count = 0
while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if ret:
        # Write the frame to a PNG file
        cv2.imshow("Webcam Image", frame)

        keyboard_input = cv2.waitKey(1)
        if keyboard_input == 27:
            file_name = f"frame_{frame_count}.png"
            cv2.imwrite(file_name, frame)
            print(f"Frame {frame_count} saved as {file_name}")

            # Increment frame count
            frame_count += 1

        # Wait for the specified delay

        # If frame rate is reached, reset frame count
    else:
        print("Error: Failed to capture frame from the camera.")
        break

# Release the camera
cap.release()