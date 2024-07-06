# This code uses base provided by the hacky pi
# This attempts to write a gif directly to the display to bypass displayio

# Right now this code is really broken, I'm struggling to figure out why its only writing the display in the corner
# and not the full display. Functionally it works, but needs to be adjusted



# Import resources
import time, board, math, busio, terminalio, displayio, os, digitalio, gifio, struct
from adafruit_st7789 import ST7789

#Starts the display
tft_bl = board.GP13
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True
# Release any resources currently in use for the displays
displayio.release_displays()

# Define the pins
tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Make the displayio SPI bus
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=180, width=135, height=240, rowstart=0, colstart=0)

odg = gifio.OnDiskGif('/dedsec.gif')

# Display the GIF continuously
while True:
    # Get next frame from the GIF
    next_delay = odg.next_frame() # load next frame
    
    # Write the bitmap data directly to the display
    # Assuming odg.bitmap is the same size as the display
    display_bus.send(42, struct.pack(">hh", 0, display.width))
    display_bus.send(43, struct.pack(">hh", 0, display.height))
    display_bus.send(44, odg.bitmap)
    
    # Sleep for the frame delay specified by the GIF
    time.sleep(next_delay)
