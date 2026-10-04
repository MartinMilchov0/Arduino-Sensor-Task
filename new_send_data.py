from datetime import datetime
import time
from fhict_cb_01.CustomPymata4 import CustomPymata4
import requests
import json
import random

statistics = dict()
done = False
DHTPIN  = 12
LDRPIN = 2

statistics["humidityMax"] = 0
statistics["temperatureMax"] = 0
statistics["brightnessMax"] = 0
statistics["humidityMin"] = 10000
statistics["temperatureMin"] = 10000
statistics["brightnessMin"] = 10000
statistics["humidityList"]=[]
statistics["humiditySum"]=0
statistics["averageHumidity"] = 0
statistics["temperatureList"]=[]
statistics["temperatureSum"]=0
statistics["averageTemperature"] = 0
statistics["brightnessList"]=[]
statistics["brightnessSum"]=0
statistics["averageBrightness"] = 0
statistics["arduinoID"] = random.randint(0, 100)

def setup():
    global board
    board = CustomPymata4(com_port = "COM3")
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05)
    board.set_pin_mode_analog_input(LDRPIN)
def DHTsensor():
    humidity, temperature,timestamp = board.dht_read(DHTPIN)
    time.sleep(0.01)
    return humidity, temperature
def LDRsensor():
    value, timestamp = board.analog_read(LDRPIN)
    return value

setup()
while not done:
    current_time = datetime.now()
    current_time = current_time.strftime("%d/%m/%Y %H:%M:%S")
    temperature = 0
    humidity = 0
    brightness = 0 
    humidity, temperature = DHTsensor()
    brightness = LDRsensor()

    statistics["time"] = current_time           
    statistics["humidity"] = humidity
    statistics["temperature"] = temperature
    statistics["brightness"] = brightness
    print(statistics)
    jsonFile = json.dumps(statistics)
    response = requests.post("http://127.0.0.1:5000/get_post", json = statistics)#ip might need to be changed at some point
    time.sleep(5)