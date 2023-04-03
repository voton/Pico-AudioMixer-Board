import time
import math

import board
import busio
import usb_hid
import digitalio
from analogio import AnalogIn

from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from lcd import i2c_pcf8574_interface, lcd


import supervisor

LAST_MESSAGE = None

TIMER = 0
LINE = 0

def init_LCD():
    i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
    i2c = i2c_pcf8574_interface.I2CPCF8574Interface(i2c, 0x27)

    display = lcd.LCD(i2c, num_rows=2, num_cols=16)
    display.set_backlight(True)
    display.set_display_enabled(True)
    
    return display

def init_custom_charset():
    square = [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F]

    display.create_char(0, square)

def LCD_print(text):
    global LAST_MESSAGE
    if text != LAST_MESSAGE:
        
        print('refresh')
        
        display.clear()
        display.print(text)
        LAST_MESSAGE = text
        time.sleep(.1)

def LCD_message(POTS):    
    global TIMER
    global LINE
    
    TIMER += 1
    if TIMER >= 10:
        LINE += 1
        TIMER = 0
        
        if LINE >= len(POTS): LINE = 0
    
    msg = f"{POTS[LINE][1]}\n"
    
    value = round(round(((POTS[LINE][0].value - 320) / (65535 - 320)) * 10) * 1.6)
    for x in range(value): msg += '\x00'

    LCD_print(str(msg))	


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


display = init_LCD()
init_custom_charset()

while True:
    Connection = supervisor.runtime.serial_connected
    LED.value = Connection

    LCD_message(POTS)

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

