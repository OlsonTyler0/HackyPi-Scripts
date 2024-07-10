# Imports required libraries
import time, os, usb_hid, digitalio, board, busio, terminalio, displayio
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard, Keycode
from keyboard_layout_win_uk import KeyboardLayout
from adafruit_st7789 import ST7789


#Options

# Task to kill
task = "notepad.exe"



# Release any resources currently in use for the displays
displayio.release_displays()

FONTSCALE = 3
TEXT_COLOR = 0xffffff

tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
tft_bl  = board.GP13 #GPIO pin to control backlight LED
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

# Make the display context
splash = displayio.Group()
display.show(splash)

#Init display
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True

# Function to print on display
def print_onTFT(text, x_pos, y_pos): 
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_group = displayio.Group(scale=FONTSCALE,x=x_pos,y=y_pos,)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

print_onTFT("Gaining", 60, 40)
print_onTFT("Access...", 40, 80)

try:
    # routine to mimic USB HID devices like keyboard, mouse, etc. through HackyPi
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayout(keyboard)
    time.sleep(2.7)
    keyboard.send(Keycode.WINDOWS, Keycode.R) # Executing WIN + R keyboard command
    time.sleep(0.4)
    keyboard_layout.write('cmd.exe') # text typing operation of keyboard through HackyPi
    keyboard.send(Keycode.ENTER)
    time.sleep(1.7)
    keyboard_layout.write("taskkill /IM " + task + " && exit")
    keyboard.send(Keycode.ENTER)
    keyboard.release_all()
except Exception as ex:
    keyboard.release_all()
    raise ex

time.sleep(1)

# release everything
displayio.release_displays()
led.deinit()
spi.deinit()

print("attempting exec")
import dedsec.py