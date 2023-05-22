import time
import math

import board
import usb_hid
import digitalio

from analogio import AnalogIn
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import supervisor

def initButtons():
    GPIO = [board.IO3, board.IO5, board.IO7]
    BIND = [ConsumerControlCode.SCAN_PREVIOUS_TRACK,
            ConsumerControlCode.PLAY_PAUSE,
            ConsumerControlCode.SCAN_NEXT_TRACK]
    
    temp = []
    for num in range(len(GPIO)):
        BTN = digitalio.DigitalInOut(GPIO[num])
        BTN.direction = digitalio.Direction.INPUT
        BTN.pull = digitalio.Pull.DOWN
        
        temp.append([BTN, BIND[num]])
    return temp

def initPots():
    GPIO = [board.IO1, board.IO2, board.IO4, board.IO6]
    lines = ["Line_one", "Line_two", "Line_three", "Line_four"]

    temp = []
    for x in range(len(GPIO)):
        POT = AnalogIn(GPIO[x])
        temp.append([POT, None, lines[x]])
    
    return temp

def initConnect(POTS):
    for POT in POTS:
        value = round(((POT[0].value) / 52070) * 100)
        print(f"{POT[2]}: {value}")


LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT

CC = ConsumerControl(usb_hid.devices)
BTNS = initButtons()
POTS = initPots()

Connected = False

while True:
    Connection = supervisor.runtime.serial_connected
    LED.value = Connected

    if Connection:
        if not Connected:
            initConnect(POTS)
            Connected = True
        
        for POT in POTS:
            value = round(((POT[0].value) / 52070) * 100)
            if value != POT[1]:
                POT[1] = value
                print(f"{POT[2]}: {value}")

        for Button in BTNS:
            if Button[0].value:
                CC.send(Button[1])
                time.sleep(0.4)
    else:
        if Connected: Connected = False
        time.sleep(2)