# This code uses base provided by the hacky pi and then additional code in 
# order to display a dedsec gif.
# Faced toward the USB in order to look the best
# DisplayIO makes this really slow, need to work on directly writing to screen.


import time, board, math, busio, terminalio, displayio, os, digitalio, gifio
from adafruit_st7789 import ST7789

tft_bl = board.GP13
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True
# Release any resources currently in use for the displays
displayio.release_displays()

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

# Change this to change the gif used
odg = gifio.OnDiskGif('/dedsec.gif')

start = time.monotonic()
next_delay = odg.next_frame() #loads the first frame
end = time.monotonic()
overhead = end-start

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
    next_delay = odg.next_frame() # load next frame

