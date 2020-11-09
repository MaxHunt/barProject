from flask import Flask, render_template, request, jsonify

import RPi.GPIO as GPIO
import os
import subprocess
import time
import board
import neopixel
import os
import random
import threading
import logging
import numpy
import requests
import json
import multiprocessing

from presets import PresetsAPI

#Basic Colours
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
#Shelf ID's 
#(24 LED's per Shelf) 
#Shelf
shelf1 = (0,23)
shelf2 = (24,47)
shelf3 = (48,71)
shelf4 = (72,95)
shelf5 = (96,119)
shelf6 = (120,143)
shelf7 = (144,167)
shelf8 = (168,191)
allshelfs=(0,191)
leftShelfs=(0,95)
rightShels=(96,191)
#Floor Boards
floorRight = (192,215)
floorMiddle = (216,273)
floorLeft = (274,298)
#BlackBoard
blackBoard=(299,449)
#bar
bar=(0,449)
#Board pin
pixel_pin = board.D18

#Secret Shelf Control Pins
##GPIO.setmode(GPIO.BOARD)
##BCM Mode is already set up from nepixel libaray
#Rasie
print (GPIO.getmode())
GPIO.setup(23, GPIO.OUT)
#Lower
GPIO.setup(24, GPIO.OUT)

# The number of NeoPixels
num_pixels = 450

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
 
#LED Object
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=ORDER
)
#define app
app = Flask(__name__)
presets_view = PresetsAPI.as_view('presets')
app.add_url_rule('/presets/', view_func= presets_view, methods = ['GET', 'POST'])
app.add_url_rule('/presets/<string:preset_id>', view_func = presets_view, methods=['PUT', 'DELETE'])

#Colour methods
def soildColourAll(r,g,b):
    pixels.fill((r, g, b))
    pixels.show()

def wipeLEDAll():
    pixels.fill((0, 0, 0))
    pixels.show()

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
    
#index starts at 0
def colourLED(r,g,b,index,show=True):
    pixels[index] = (r,g,b)
    if (show==True):
        pixels.show()

def movingLEDAll(r=255,g=0,b=0,speed=0.1):
    for i in range(num_pixels):
        colourLED(r,g,b,i)
        time.sleep(speed)

def setColourShelf(shelfnumber,r,g,b):
    #pixels.fill((r,g,b),shelfnumber[0],24)
    for i in range(shelfnumber[0],(shelfnumber[1]+1)):
        colourLED(r,g,b,i,False)
    pixels.show()

def setColourShelfWithoutShow(shelfnumber,r,g,b):
    #pixels.fill((r,g,b),shelfnumber[0],24)
    for i in range(shelfnumber[0],(shelfnumber[1]+1)):
        colourLED(r,g,b,i,False)

def lightUpAll(RGB,duration,interval,shelfnumber):
    sleepinterval=duration/interval
    roiRed=0   
    roiGreen=0
    roiBlue=0
    if (RGB[0]!=0):
        roiRed=RGB[0]/sleepinterval
    if (RGB[1]!=0): 
        roiGreen=RGB[1]/sleepinterval
    if (RGB[2]!=0):
        roiBlue=RGB[2]/sleepinterval
    for i in range(0,round(sleepinterval)):        
        for j in range(shelfnumber[0],(shelfnumber[1]+1)):
            pixels[j] = (round(roiRed*i),round(roiGreen*i),round(roiBlue*i))
        pixels.show()

def lightDownAll(RGB,duration,interval,shelfnumber):
    sleepinterval=duration/interval
    roiRed=0   
    roiGreen=0
    roiBlue=0
    if (RGB[0]!=0):
        roiRed=RGB[0]/sleepinterval
    if (RGB[1]!=0): 
        roiGreen=RGB[1]/sleepinterval
    if (RGB[2]!=0):
        roiBlue=RGB[2]/sleepinterval
    for i in range(0,round(sleepinterval)):        
        for j in range(shelfnumber[0],(shelfnumber[1]+1)):
            pixels[j] = (RGB[0]-(round(roiRed*i)),round(RGB[1]-(roiGreen*i)),round(RGB[2]-(roiBlue*i)))
        pixels.show()

def thunderbirds101thread():
    while True:
        setColourShelf(floorLeft,255,255,255)
        setColourShelf(floorLeft,0,0,0)
        setColourShelf(floorRight,255,255,255)
        setColourShelf(floorRight,0,0,0)


##############################start up funcations####################################################################
def redToGreenTransferThread(r,g,b):
    for i in range(0,256):
        time.sleep(0.01)           
        soildColourAll(r-i,i,b)        
    
# def selfBrightnessIncrease(r,g,b,shelfnumber):
#     for i in numpy.arange(0,1.0,0.01):
#         pixels = neopixel.NeoPixel(
#             pixel_pin, num_pixels, brightness=i, auto_write=True, pixel_order=ORDER
#         )
#         print(i)
#         print(g)
#         pixelbrightness.fill((r,g,b))
#         time.sleep(0.07)        
#         #for j in range(shelfnumber[0],(shelfnumber[1]+1)):
#         #    pixelbrightness[j] = (r,g,b)
                   
def startupLights():
    print("StartUpProcedures")    
    redToGreenTransferThread(255,0,0)
    time.sleep(1)
    wipeLEDAll()
    time.sleep(1)
    soildColourAll(0,255,0)
    time.sleep(1)
    wipeLEDAll()

# def start_runner():
#     wipeLEDAll()
#     soildColourAll(255,0,0)
#     def start_loop():
#         not_started = True
#         while not_started:
#             print('In start loop')
#             try:
#                 r = requests.get('http://127.0.0.1:5000/')
#                 if r.status_code == 200:
#                     print('Server started, quiting start_loop')
#                     not_started = False
#                     startupLights()
#                 print(r.status_code)
#             except Exception as e:
#                 print('Server not yet started')
#                 print(e)
#             time.sleep(2)

#     print('Started runner')
#     thread = threading.Thread(target=start_loop)
#     thread.start()
#     print('Stopped') 

#######################################################################################################################



#Flask and Ajax returns
@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/api/shelfLights', methods=['POST'])
def shelfLights():
    json = request.get_json()
    print (json)  
    if (json["shelf"]=="1"): 
        setColourShelf(shelf1,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="2"): 
        setColourShelf(shelf2,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="3"): 
        setColourShelf(shelf3,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="4"): 
        setColourShelf(shelf4,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="5"): 
        setColourShelf(shelf5,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="6"): 
        setColourShelf(shelf6,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="7"): 
        setColourShelf(shelf7,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="8"): 
        setColourShelf(shelf8,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="10"): 
        setColourShelf(floorLeft,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="11"): 
        setColourShelf(floorMiddle,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="12"): 
        setColourShelf(floorRight,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="13"): 
        setColourShelf(blackBoard,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    else:
        print("No Action") 
    print("Lights Started")
    return ("Success"), 200

@app.route('/api/allLightsOn', methods=['POST'])
def allLightsOn():      
    soildColourAll(0,255,0)
    print("Lights Started")
    return ("Success"), 204

@app.route('/api/allLightsOff', methods=['POST'])
def allLightsOff():    
    json = request.get_json()
    wipeLEDAll()
    print ("Lights Stopped")    
    return ("Success"), 204

@app.route('/api/movingLEDrun', methods=['POST'])
def movingLEDrun():    
    json = request.get_json()
    print ("Lights Started") 
    lightDownAll([0,255,0],1,0.01,bar) 
    #movingLEDAll(180,0,255,0.1)
    print ("Lights Stopped")    
    return ("Success"), 204

@app.route('/api/shelfRandomColours', methods=['POST'])
def shelfRandomColours():    
    json = request.get_json()
    print ("Lights Started")  
    setColourShelf(shelf1,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(shelf2,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(shelf3,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(shelf4,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(shelf5,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(shelf6,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(shelf7,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(shelf8,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(floorLeft,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(floorMiddle,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(floorRight,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    setColourShelf(blackBoard,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
    print ("Lights Stopped")    
    return ("Success"), 204

@app.route('/api/rainbow', methods=['POST'])
def rainbow():    
    json = request.get_json()
    print ("Lights Started")
    while True: 
        rainbow_cycle(0.001)
    print ("Lights Stopped")    
    return ("Success"), 204

@app.route('/api/raise', methods=['POST'])
def raiseShelf():
    GPIO.output(24, GPIO.HIGH)
    print("Start Raise")
    GPIO.output(23, GPIO.LOW)
    print("Wait for Raise")
    time.sleep(28)
    GPIO.output(23, GPIO.HIGH)
    print("Rasie Finshed")
    return ("Success"), 200 

@app.route('/api/lower', methods=['POST'])
def lowerShelf():
    GPIO.output(23, GPIO.HIGH)
    print("Start Lower")
    GPIO.output(24, GPIO.LOW)
    print("Wait for Lower")
    time.sleep(32)
    GPIO.output(24, GPIO.HIGH)
    print("Lower Finshed")
    return ("Success"), 200

@app.route('/api/raisefab', methods=['POST'])
def raisefab():
    wipeLEDAll()
#     shelf1 = (0,23)
# shelf2 = (24,47)
# shelf3 = (48,71)
# shelf4 = (72,95)
# shelf5 = (96,119)
# shelf6 = (120,143)
# shelf7 = (144,167)
# shelf8 = (168,191)
# #Floor Boards
# floorRight = (192,215)
# floorMiddle = (216,273)
# floorLeft = (274,298)
# #BlackBoard 20 height 22 long
# blackBoard=(299,449)
   #5
    for i in range(48,(119+1)):
        colourLED(192,192,192,i,False)
    for i in range(144,(298+1)):
        colourLED(192,192,192,i,False)
    for i in range(319,(341+1)):
        colourLED(192,192,192,i,False)
    for i in range(363,(387+1)):
        colourLED(192,192,192,i,False)
    pixels.show()
    time.sleep(2)
    #4
    wipeLEDAll()
    for i in range(48,(191+1)):
        colourLED(247,255,0,i,False)
    for i in range(319,(341+1)):
        colourLED(247,255,0,i,False)
    pixels.show()
    #3
    time.sleep(2)
    wipeLEDAll()
    setColourShelfWithoutShow(floorLeft,255,0,0)
    setColourShelfWithoutShow(floorMiddle,255,0,0)
    setColourShelfWithoutShow(floorRight,255,0,0)
    setColourShelfWithoutShow(shelf8,255,0,0)
    setColourShelfWithoutShow(shelf7,255,0,0)
    setColourShelfWithoutShow(shelf6,255,0,0)
    setColourShelfWithoutShow(shelf5,255,0,0)
    setColourShelfWithoutShow(shelf4,255,0,0)
    setColourShelfWithoutShow(shelf1,255,0,0)
    for i in range(319,(341+1)):
        colourLED(255,0,0,i,False)
    for i in range(363,(387+1)):
        colourLED(255,0,0,i,False)
    pixels.show()
    time.sleep(2)
    #2
    wipeLEDAll()
    setColourShelfWithoutShow(floorLeft,0,255,0)
    setColourShelfWithoutShow(floorMiddle,0,255,0)
    setColourShelfWithoutShow(floorRight,0,255,0)
    setColourShelfWithoutShow(shelf7,0,255,0)
    setColourShelfWithoutShow(shelf6,0,255,0)
    setColourShelfWithoutShow(shelf5,0,255,0)
    setColourShelfWithoutShow(shelf4,0,255,0)
    setColourShelfWithoutShow(shelf2,0,255,0)
    setColourShelfWithoutShow(shelf1,0,255,0)
    for i in range(319,(341+1)):
        colourLED(0,255,0,i,False)
    for i in range(363,(387+1)):
        colourLED(0,255,0,i,False)
    pixels.show()
    time.sleep(2)
    #1
    wipeLEDAll()
    setColourShelfWithoutShow(floorRight,0,0,255)
    setColourShelfWithoutShow(shelf8,0,0,255)
    setColourShelfWithoutShow(shelf7,0,0,255)
    setColourShelfWithoutShow(shelf6,0,0,255)
    setColourShelfWithoutShow(shelf5,0,0,255)
    pixels.show()
    time.sleep(0.2)
    #Engines fire
    t_end = time.time() + 4.5
    while (time.time() < t_end):    
        pixels.show()
        for i in range(192,(215+1)):
            colour = random.randint(0,3)
            if (colour==0):
                pixels[i] = (255,0,0)
            elif (colour==1):
                pixels[i] = (255,255,0)
            elif (colour==2):
                pixels[i] = (255,137,0)
    #Move Thunderbird 1 Up
    setColourShelfWithoutShow(shelf8,0,0,0)
    setColourShelfWithoutShow(floorRight,0,0,0)
    t_end = time.time() + 0.25
    while (time.time() < t_end):
        pixels.show()
        for i in range(168,(191+1)):
            colour = random.randint(0,3)
            if (colour==0):
                pixels[i] = (255,0,0)
            elif (colour==1):
                pixels[i] = (255,255,0)
            elif (colour==2):
                pixels[i] = (255,137,0)
    setColourShelfWithoutShow(shelf7,0,0,0)
    setColourShelfWithoutShow(shelf8,0,0,0)
    t_end = time.time() + 0.25
    while (time.time() < t_end):
        pixels.show()
        for i in range(144,(167+1)):
            colour = random.randint(0,3)
            if (colour==0):
                pixels[i] = (255,0,0)
            elif (colour==1):
                pixels[i] = (255,255,0)
            elif (colour==2):
                pixels[i] = (255,137,0)
    setColourShelfWithoutShow(shelf6,0,0,0)
    setColourShelfWithoutShow(shelf7,0,0,0)
    t_end = time.time() + 0.125
    while (time.time() < t_end):
        pixels.show()
        for i in range(120,(143+1)):
            colour = random.randint(0,3)
            if (colour==0):
                pixels[i] = (255,0,0)
            elif (colour==1):
                pixels[i] = (255,255,0)
            elif (colour==2):
                pixels[i] = (255,137,0)
    setColourShelfWithoutShow(shelf5,0,0,0)
    setColourShelfWithoutShow(shelf6,0,0,0)
    t_end = time.time() + 0.0625
    while (time.time() < t_end):
        pixels.show()
        for i in range(96,(119+1)):
            colour = random.randint(0,3)
            if (colour==0):
                pixels[i] = (255,0,0)
            elif (colour==1):
                pixels[i] = (255,255,0)
            elif (colour==2):
                pixels[i] = (255,137,0)
    lightUpAll([0,255,0],1,0.1,bar)
    stop_thread101 = False
    wipeLEDAll()
    #Quick Start
    #trumpt
    lightDownAll([255,255,255],2,0.1,allshelfs)
    lightDownAll([255,255,255],2,0.1,allshelfs)
    lightDownAll([255,255,255],0.8,0.1,allshelfs)
    #trumbone
    wipeLEDAll()
    setColourShelfWithoutShow(shelf5,255,0,239)
    setColourShelfWithoutShow(shelf4,255,0,239)
    setColourShelfWithoutShow(shelf6,255,0,239)
    pixels.show()
    wipeLEDAll()
    setColourShelfWithoutShow(shelf3,255,0,239)
    setColourShelfWithoutShow(shelf7,255,0,239)
    pixels.show()
    wipeLEDAll()
    setColourShelfWithoutShow(shelf1,255,0,239)
    setColourShelfWithoutShow(shelf2,255,0,239)
    setColourShelfWithoutShow(shelf8,255,0,239)
    pixels.show()
    time.sleep(0.15)
    wipeLEDAll()
    #thread101 = multiprocessing.Process(target=thunderbirds101thread)
    #thread101.start()
    #main fast sequence
    #loop1
    setColourShelfWithoutShow(shelf2,0,247,255)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf6,0,247,255)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf3,0,247,255)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf8,0,247,255)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf1,0,247,255)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf4,0,247,255)
    pixels.show()
    time.sleep(0.3)
    setColourShelfWithoutShow(shelf7,0,247,255)
    pixels.show()
    time.sleep(0.3)
    setColourShelfWithoutShow(shelf5,0,247,255)
    pixels.show()
    time.sleep(0.3)
    setColourShelfWithoutShow(bar,0,247,255)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(bar,255,100,255)
    pixels.show()
    time.sleep(0.2)
    #loop 2
    wipeLEDAll()
    setColourShelfWithoutShow(shelf5,255,0,239)
    setColourShelfWithoutShow(shelf4,255,0,239)
    setColourShelfWithoutShow(shelf6,255,0,239)
    pixels.show()
    wipeLEDAll()
    setColourShelfWithoutShow(shelf3,255,0,239)
    setColourShelfWithoutShow(shelf7,255,0,239)
    pixels.show()
    wipeLEDAll()
    setColourShelfWithoutShow(shelf1,255,0,239)
    setColourShelfWithoutShow(shelf2,255,0,239)
    setColourShelfWithoutShow(shelf8,255,0,239)
    pixels.show()
    time.sleep(0.15)
    wipeLEDAll()
    setColourShelfWithoutShow(shelf2,50,255,93)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf6,50,255,93)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf3,50,255,93)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf8,50,255,93)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf1,50,255,93)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(shelf4,50,255,93)
    pixels.show()
    time.sleep(0.3)
    setColourShelfWithoutShow(shelf7,50,255,93)
    pixels.show()
    time.sleep(0.3)
    setColourShelfWithoutShow(shelf5,50,255,93)
    pixels.show()
    time.sleep(0.3)
    setColourShelfWithoutShow(bar,50,255,93)
    pixels.show()
    time.sleep(0.1)
    setColourShelfWithoutShow(bar,255,100,255)
    pixels.show()
    time.sleep(0.6)
    wipeLEDAll()
    #fastsequencemain
    lightUpAll([0,255,0],0.5,0.1,bar)
    wipeLEDAll()
    lightUpAll([0,255,0],0.4,0.1,bar)
    time.sleep(0.1)
    wipeLEDAll()    
    setColourShelf(floorMiddle,255,255,0)
    setColourShelf(blackBoard,255,255,0)
    pixels.show()
    time.sleep(0.2)
    lightUpAll([255,0,0],0.5,0.1,bar)
    wipeLEDAll()
    lightUpAll([255,0,0],0.4,0.1,bar)
    time.sleep(0.2)
    wipeLEDAll()
    setColourShelf(floorMiddle,0,255,255)
    setColourShelf(blackBoard,0,255,255)
    pixels.show()
    time.sleep(0.2)
    lightUpAll([0,0,255],0.5,0.1,bar)
    wipeLEDAll()
    lightUpAll([0,0,255],0.4,0.1,bar)
    time.sleep(0.2)
    wipeLEDAll()
    setColourShelf(floorMiddle,238,130,238)
    setColourShelf(blackBoard,238,130,238)
    pixels.show()
    time.sleep(0.2)
    lightUpAll([255,0,255],0.5,0.1,bar)
    wipeLEDAll()
    lightUpAll([255,0,255],0.4,0.1,bar)
    time.sleep(0.2)
    setColourShelf(floorMiddle,255,0,127)
    setColourShelf(blackBoard,255,0,127)
    pixels.show()
    time.sleep(0.3)
    setColourShelf(bar,255,0,255)
    time.sleep(0.3)
    #endingTronbone
    wipeLEDAll()
    setColourShelf(shelf4,255,0,0)
    time.sleep(0.2)
    wipeLEDAll()
    setColourShelf(shelf7,255,0,0)
    time.sleep(0.2)
    wipeLEDAll()
    setColourShelfWithoutShow(shelf2,255,0,0)
    setColourShelfWithoutShow(shelf1,255,0,0)
    pixels.show()
    time.sleep(0.2)
    wipeLEDAll()
    setColourShelf(shelf8,255,0,0)
    time.sleep(0)
    wipeLEDAll()
    setColourShelf(shelf3,255,0,0)
    time.sleep(0)
    wipeLEDAll()
    setColourShelfWithoutShow(shelf5,255,0,0)
    setColourShelfWithoutShow(shelf6,255,0,0)
    pixels.show()
    time.sleep(0.2)
    wipeLEDAll()
    setColourShelf(blackBoard,255,0,0)
    time.sleep(0.2)
    wipeLEDAll()
    setColourShelf(leftShelfs,255,0,0)
    time.sleep(0.2)
    setColourShelf(rightShels,255,0,0)
    time.sleep(0.2)
    lightUpAll([255,255,89],3,0.1,bar)
    lightDownAll([255,255,89],3,0.1,bar)
    time.sleep(5)
    #thread101.terminate()
    return ("Success"), 200

##Run
if __name__ == '__main__':
    #start_runner()
    #startupLights()
    app.run(debug=True, host='0.0.0.0')
    