import time
import math

import board
import usb_hid
import digitalio
from analogio import AnalogIn

import supervisor

LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT

POTS = [[AnalogIn(board.GP26), 'Discord'],
        [AnalogIn(board.GP27), 'Spotify'],
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

        time.sleep(.5)
    else:
        time.sleep(5)
