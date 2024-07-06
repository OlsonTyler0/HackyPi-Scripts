# This code uses base provided by Hacky Pi
# Code loads a gif onto the screen and plays it frame by frame
# Due to reliance on displayio its slow Writing directly to the display has some issues.
# Faced toward the USB in order to look the best

# Import the required libraries
import time, board, math, busio, terminalio, displayio, os, digitalio, gifio
from adafruit_st7789 import ST7789

# Start the displays
tft_bl = board.GP13
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True
# Release any resources currently in use for the displays
displayio.release_displays()

# Define the numbers for the pins
tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
tft_bl  = board.GP13
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

    
# Make the displayio SPI bus
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=180, width=135, height=240, rowstart=40, colstart=53)

# Make the main display context
main = displayio.Group()
display.root_group = main

# Load dedsec.gif 
odg = gifio.OnDiskGif('/dedsec.gif')

# Calculate time between frames
start = time.monotonic()
next_delay = odg.next_frame() #loads the first frame
end = time.monotonic()
overhead = end-start

# Put onto the display time
face = displayio.TileGrid(
    odg.bitmap,
    pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.RGB565_SWAPPED
    ),
)

main.append(face)

# Display Repeatedly
while True:
    # sleep for the frame delay specified by gif,
    # minus overhead measured to advance between frames
    time.sleep(max(0, next_delay-overhead))
    next_delay = odg.next_frame() # load next frames