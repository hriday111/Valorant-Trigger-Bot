
#TODO: convert for loops to a functions.
import keyboard
import time
import ctypes
import PIL.ImageGrab
from keyboard import is_pressed
import winsound 
import numpy as np
from pynput.mouse import Button, Controller

mouse = Controller()

threshold_inc='ctrl + up'
threshold_dec='ctrl + down'
import serial
ser = serial.Serial('COM4',9600)
time.sleep(1)
FoundEnemy=False
def avg(lst):
    return sum(lst)// len(lst)
S_WIDTH,S_HEIGHT = (PIL.ImageGrab.grab().size)
print(S_WIDTH,S_HEIGHT)
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 60
def approx(r, g ,b):
        return PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE and PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE and PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE
def color_check(red, green, blue):
    if green >= 190:
        return False
        
    if green >= 140:
        return abs(red - blue) <= 8 and red - green >= 50 and blue - green >= 50 and red >= 105 and blue >= 105

    return abs(red - blue) <= 13 and red - green >= 60 and blue - green >= 60 and red >= 110 and blue >= 100

while True:
    threshold = 100
    if is_pressed(threshold_inc):
        threshold+=50
        print("Threshold:",threshold)
    if is_pressed(threshold_dec):
        threshold-=50
        print("Threshold:",threshold)
    
    
    
    x0,y0,xx,yy = (int(S_HEIGHT / 2 - threshold), int(S_WIDTH / 2 - threshold), int(S_HEIGHT / 2 + threshold), int(S_WIDTH / 2 + threshold))
    pmap = PIL.ImageGrab.grab()
    for x in range((S_WIDTH//2- threshold),(S_WIDTH//2+threshold)):
        for y in range((S_HEIGHT//2- threshold),(S_HEIGHT//2+threshold)):
            r, g, b = pmap.getpixel((x,y))
            if approx(r, g, b):
                x1,y1=mouse.position 
                print(x1-x,y1-y)
                ser.write(bytes(str(x1-x)+','+str(y1-y)+'\n', encoding='utf-8'))
                print(ser.readline())
                break

        break
    