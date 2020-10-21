from flask import Flask, render_template, request, jsonify
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
shelf9 = (192,215)
#Floor Boards
floorLeft = (216,239)
floorMiddle = (240,275)
floorRight = (276,299)
#BlackBoard
blackBoard=(300,449)
#Board pin
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 450
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
 
#LED Object
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)
#define app
app = Flask(__name__)


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
    elif (json["shelf"]=="9"): 
        setColourShelf(shelf9,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="10"): 
        setColourShelf(floorLeft,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="11"): 
        setColourShelf(floorMiddle,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    elif (json["shelf"]=="12"): 
        setColourShelf(floorRight,json["colour"]["r"],json["colour"]["g"],json["colour"]["b"])
    else:
        print("No Action")    
    print("Lights Started")
    return ("Success"), 204

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
    movingLEDAll(180,0,255,0.1)
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
    setColourShelf(shelf9,(random.randint(0, 255)),(random.randint(0, 255)),(random.randint(0, 255)))
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

##Run
if __name__ == '__main__':
    #start_runner()
    startupLights()
    app.run(debug=True, host='0.0.0.0')
    