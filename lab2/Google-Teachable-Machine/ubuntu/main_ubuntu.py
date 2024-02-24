from Adafruit_IO import MQTTClient
from keras.models import load_model
import sys
import time
import threading
import cv2
import numpy as np


captured_label = ""
previous_capture_label = ""
score = ""
flag = 0
AIO_USERNAME = "kientranvictory"
AIO_KEY = ""

def connected(client):
    print("Ket noi thanh cong ...")

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)

def message(client, feed_id, payload):
    print("====================================") 
    print("Nhan du lieu: " + payload + "; Feed_id:" + feed_id) 
    print("====================================") 

def counter_second():
    # global captured_label
    global flag
    counter = 5    
    while True:
        counter = counter - 1
        if counter <= 0:
            counter = 5
            flag = 1
        time.sleep(1)  # Sleep 1 second before publishing again
                
            

# Start publishing sensor data in a separate thread
publish_thread = threading.Thread(target=counter_second)
publish_thread.start()

# Function to perform model prediction
def predict_image(image, model, class_names):
    global captured_label, counter, flag
    # Resize the raw image
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the model's input shape
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1
    if flag == 1:
        flag = 0
        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        captured_label = class_name[2:].strip()
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        
        # set up for adafruit-io
        client = MQTTClient(AIO_USERNAME, AIO_KEY)
        client.on_connect = connected
        client.on_disconnect = disconnected
        client.on_message = message
        client.on_subscribe = subscribe

        client.connect()
        print("AI-detected is publishing value:", captured_label) 
        client.publish("ai", captured_label)
    

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture("http://192.168.50.37:4747/video")

def predict_and_capture():
    while True:
        # Grab the web camera's image
        ret, image = camera.read()

        # Show the image in a window
        cv2.imshow("Webcam Image", image)

        # Perform prediction in a separate thread
        prediction_thread = threading.Thread(target=predict_image, args=(image, model, class_names))
        prediction_thread.start()

        # Listen to the keyboard for presses
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard
        if keyboard_input == 27:
            break

# Start capturing frames
predict_and_capture()

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()