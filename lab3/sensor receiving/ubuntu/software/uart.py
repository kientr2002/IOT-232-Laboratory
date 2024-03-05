from serial import Serial
import serial.tools.list_ports
import time

port_1 = "/dev/pts/12"
port_2 = "/dev/pts/11"


def getPort():
    global port_1
    return port_1
mess = ""

def processData(client, data):
    data = data.replace("s", "")
    data = data.replace("e", "")
    splitData = data.split(":")
    print(getPort() + " received data:")
    print(splitData)
    if splitData[1] == "T":
        client.publish("sensor1", splitData[2])
    if splitData[1] == "H":
        client.publish("sensor2", splitData[2])


if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
else:
    print("No Port can be found!!!")

def readSerial(client, flag_init):
    commPort = getPort()
    if commPort != "None":
        if flag_init == 0:
            print(ser)
        global mess
        bytesToRead = ser.inWaiting()
        if bytesToRead > 0:
            mess += ser.read(bytesToRead).decode("UTF-8")
            while "s" in mess and "e" in mess:
                start = mess.find("s")
                end = mess.find("e")
                processData(client, mess[start:end + 1])
                if end == len(mess):
                    mess = ""
                else:
                    mess = mess[end + 1:]
    else:
        print("No serial port available.")
        time.sleep(1)


def writeData(data):
    ser.write(str(data).encode())

# Example usage:
# readSerial(client)  # Call this function with your MQTT client
