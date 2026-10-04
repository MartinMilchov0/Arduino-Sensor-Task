from flask import Flask, render_template
import random 
from datetime import datetime
import time, sys
from fhict_cb_01.CustomPymata4 import CustomPymata4
from flask import request, redirect
import requests
import json
import math

app = Flask(__name__)
statistics = dict()
arduinoID = list()
arduinoNumber = list()
received = False
data = []
statistics["arduinoID"] = None
temperature = 0
humidity = 0
brightness = 0 
statistics["humidityMax"] = 0
statistics["temperatureMax"] = 0
statistics["brightnessMax"] = 0
statistics["humidityMin"] = 10000
statistics["temperatureMin"] = 10000
statistics["brightnessMin"] = 10000
statistics["averageHumidity"] = 0
statistics["averageTemperature"] = 0
statistics["averageBrightness"] = 0

@app.route('/get_post', methods = ['POST'])
def get_data():
        global statistics 
        global temperature, humidity, brightness
        statistics = request.get_json()
        temperature = statistics["temperature"]
        humidity = statistics["humidity"]
        brightness = statistics["brightness"]
        if humidity > statistics["humidityMax"]:
            statistics["humidityMax"] = humidity
        if temperature > statistics["temperatureMax"]:
            statistics["temperatureMax"] = temperature
        if brightness > statistics["brightnessMax"]:
            statistics["brightnessMax"] = brightness
        if statistics["humidityMin"] == 0:
            statistics["humidityMin"] = 10000
        if statistics["temperatureMin"] == 0:
            statistics["temperatureMin"] = 10000
        if statistics["brightnessMin"] == 0:
            statistics["brightnessMin"] = 10000
        if humidity < statistics["humidityMin"]:
            statistics["humidityMin"] = humidity
        if temperature < statistics["temperatureMin"]:
            statistics["temperatureMin"] = temperature
        if brightness < statistics["brightnessMin"]:
            statistics["brightnessMin"] = brightness

        if humidity>0:
            statistics["humidityList"].append(humidity)
            statistics["humiditySum"]=sum(statistics["humidityList"])
        #calculating average and rounding up to the second decimal place
            statistics["averageHumidity"] = (math.ceil((statistics["humiditySum"]/len(statistics["humidityList"])*100))/100)
        if temperature>0:
            statistics["temperatureList"].append(temperature)
            statistics["temperatureSum"]=sum(statistics["temperatureList"])
            statistics["averageTemperature"] = (math.ceil((statistics["temperatureSum"]/len(statistics["temperatureList"])*100))/100)
        if brightness>0:
            statistics["brightnessList"].append(brightness)
            statistics["brightnessSum"]=sum(statistics["brightnessList"])
            statistics["averageBrightness"] = (math.ceil((statistics["brightnessSum"]/len(statistics["brightnessList"])*100))/100)
        jsonFile = json.dumps(statistics)
        return statistics

@app.route('/')
def index():
    global received 
    received = False
    global statistics 
    global arduinoNumber
    if data:
        for i in range(len(data)):
            if data[i]["arduinoID"] == statistics["arduinoID"]:
                received = True
                data[i] = statistics
        if not received:
            data.append(statistics)
    else:
        data.append(statistics)

    arduinoNumber = range(len(data))
    return render_template("index.html", statistics = data, arduinosNum = arduinoNumber)