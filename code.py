import time
import math

import board
import usb_hid
import digitalio
from analogio import AnalogIn

from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import supervisor

LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT

BTNS = [board.GP15, board.GP14, board.GP13]

for x in range(len(BTNS)):
            BTNS[x] = digitalio.DigitalInOut(BTNS[x])
            BTNS[x].direction = digitalio.Direction.INPUT
            BTNS[x].pull = digitalio.Pull.DOWN

keyboard = Keyboard(usb_hid.devices)
consumer_control = ConsumerControl(usb_hid.devices)

POTS = [[AnalogIn(board.GP26), 'Other'],
        [AnalogIn(board.GP27), 'Music'],
        [AnalogIn(board.GP28), 'Browsers']]

while True:
    Connection = supervisor.runtime.serial_connected
    LED.value = Connection

    if Connection:    
        message = ""

        for POT in POTS:
            value = round(((POT[0].value - 320) / (65535 - 320)) * 100)
            # print(f" - {POT[1]}: {value}\n")

            message += f" - {POT[1]}: {value}\n"
        print(message)

        if BTNS[0].value:
            consumer_control.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
            time.sleep(.001)
        if BTNS[1].value:
            consumer_control.send(ConsumerControlCode.PLAY_PAUSE)
            time.sleep(.001)
        if BTNS[2].value: 
            consumer_control.send(ConsumerControlCode.SCAN_NEXT_TRACK)
            time.sleep(.001)
        
        time.sleep(.5)
    else:
        time.sleep(5)

