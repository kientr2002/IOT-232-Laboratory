import sys
import time
import random

from Adafruit_IO import MQTTClient

AIO_FEED_IDs = ["button1", "button2"]
AIO_USERNAME = "kientranvictory"
AIO_KEY = "aio_TRfK93mydKgkYq9MYrVxhIug6fcJ"

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
    print("Nhan du lieu: " + payload + "; Feed_id:" + feed_id) 

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter = 10
sensor_type = 0
while True:
    counter = counter - 1
    if counter <= 0:
        counter = 10
        # TO DO
        print("====================================")        
        if sensor_type == 0:
            print("Temperature is publishing value:")   
            sensor_type = 1
            temp = random.randint(10, 20)
            print(temp)
            client.publish("sensor1", temp)
            
        elif sensor_type == 1:
            print("Humidity is publishing value: ")
            sensor_type = 2           
            humi = random.randint(50, 70)
            print(humi)            
            client.publish("sensor2", humi)
        elif sensor_type == 2:
            print("Light is publishing value: ")
            sensor_type = 0
            light = random.randint(100, 500)
            print(light)
            client.publish("sensor3", light)       
        print("====================================") 
    time.sleep(1)
    pass