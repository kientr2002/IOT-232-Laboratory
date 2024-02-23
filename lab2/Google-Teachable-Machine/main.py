import sys
import time
import random
import cv2  # Install opencv-python
import numpy as np

from Adafruit_IO import MQTTClient
from simple_ai import *
from keras.models import load_model  # TensorFlow is required for Keras to work

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)
#"http://192.168.50.37:4747/video"

AIO_FEED_IDs = ["button1", "button2"]
AIO_USERNAME = "kientranvictory"
AIO_KEY = ""

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("====================================") 
    print("Nhan du lieu: " + payload + "; Feed_id:" + feed_id) 
    print("====================================") 

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter = 10
counter_ai = 1
sensor_type = 0
while True:
    ai_result = ai_detector(camera, model, class_names)
    print("AI output: ", ai_result)
    counter = counter - 1
    if counter <= 0:
        counter = 10
        # TO DO
        print("====================================")        
        if sensor_type == 0:
            print("Temperature is publishing value:")   
            sensor_type = 1
            temp = random.randint(10, 20)
            print(str(temp) + "oC")
            client.publish("sensor1", temp)
            
        elif sensor_type == 1:
            print("Humidity is publishing value: ")
            sensor_type = 2           
            humi = random.randint(50, 70)
            print(str(humi) + "%")            
            client.publish("sensor2", humi)
        elif sensor_type == 2:
            print("Light is publishing value: ")
            sensor_type = 0
            light = random.randint(100, 500)
            print(str(light) + "lux")
            client.publish("sensor3", light)       
        print("====================================") 
    
    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 1
    time.sleep(1)