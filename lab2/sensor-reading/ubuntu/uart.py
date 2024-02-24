import serial.tools.list_ports
import time
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

mess = ""

def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    if len(splitData) >= 2:  # Kiểm tra xem có đủ phần tử để truy cập không
        if splitData[1] == "T":
            client.publish("sensor1", splitData[2])
            print(splitData[2])

def readSerial(client):
    commPort = getPort()
    if commPort != "None":
        ser = serial.Serial(port=commPort, baudrate=115200)
        print(ser)

        global mess

        while True:
            bytesToRead = ser.inWaiting()
            if bytesToRead > 0:
                mess += ser.read(bytesToRead).decode("UTF-8")
                while "#" in mess and "!" in mess:
                    start = mess.find("!")
                    end = mess.find("#")
                    processData(client, mess[start:end + 1])
                    if end == len(mess):
                        mess = ""
                    else:
                        mess = mess[end + 1:]
                    time.sleep(1)
    else:
        print("No serial port available.")

# Example usage:
# readSerial(client)  # Call this function with your MQTT client