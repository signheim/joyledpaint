####################################################
#                                                  #
#               J O Y L E D P A I N T              #
#                                                  #
#  Raspberry Pi Pico                               #
#  8 x 8 WS2812 LED Matrix                         #
#  HW-504 Joystick                                 #
#                                                  #
#  2021 by signheim                                #
#                                                  #
#  Includes pico_ws2812b library by benevpi:       #
#  https://github.com/benevpi/pico_python_ws2812b  #
#                                                  #
####################################################

from machine import Pin, ADC
import ws2812b

delay = 0.01    # delay between LED updatings
cPix = 0        # current Pixel (0-63), that's where joypaint will start
cCol = 0        # current Color is set to the first color in the cols-array, could be any
xTick = 0       # Ticks are used to enable slower and faster movements of the joystick
yTick = 0
thrTick = 5     # used to initiate a movement until a Tick reaches this threshold
waitTime = 100  # time for a long click (times the delay in the matrix-setup (100 x 0.01 = 1 sec)
lit = 0.2       # brightness of a hightlighted pixels
dim = 0.05      # brightness of drawn pixel
blink = 0       # used for blinking of active Pixel when in delete (black) mode
thrBlink = 10   # on and off for 10 delay-units
dirBlink = 1    # counts back and forth (via this direction variable dirBlink)
rows = 8        # 8 rows and 8 columns lead to 64 LEDs (pixels)
columns = 8
pixels = rows * columns

# Connect the joystick to pins
xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
button = Pin(16,Pin.IN, Pin.PULL_UP)

# The LED-matrix is connected to SPI-0 on GP-5 (Pin-7), a delay is set after each show()
matrix = ws2812b.ws2812b(pixels, 0, 5, delay)

# 7 colors (could be any number - as long as the last is black - for deleting)
cols = [
    [255, 255, 255],
    [255, 0, 0],
    [128, 128, 0],
    [0, 255, 0],
    [0, 128, 128],
    [0, 0, 255],
    [128, 0, 128],
    [0, 0, 0],
]

# First Pixel is set at the starting position
matrix.set_pixel(cPix, cols[cCol][0] * dim, cols[cCol][1] * dim, cols[cCol][2] * dim)

while True:
    
    # Read the joystick input
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    bValue = button.value()
    
    # set the current pixel to the darker color in case that a moving will happen
    # this leaves the last drawn pixel darker than the current pixel
    matrix.set_pixel(cPix, cols[cCol][0] * dim, cols[cCol][1] * dim, cols[cCol][2] * dim)
    
    # reset all moving instructions
    pixMove = 0;
    
    # calculate how much to joystick was moved horizontally and vertically
    # the thresholds are a desision after testing this particular joystick
    # around the middle-value nothing is added to the ticks
    # the more the joystick is bent, the more is added
    if xValue > 33500 or xValue < 31500:
        xTick += (xValue / 65535) - 0.5
    if yValue > 33800 or yValue < 31800:
        yTick += (yValue / 65535) - 0.5
    
    # once the Ticks exceed their thresholds they are resetted and the movement
    # is added to pixMove (1 for horizontal and 8 for vertical for it is a stripe)
    # as long as the current pixel wasn't already at the edge
    if xTick > thrTick:
        xTick = 0
        if cPix % columns != 7:
            pixMove += 1
    elif xTick < -thrTick:
        xTick = 0
        if cPix % columns != 0:
            pixMove -= 1
    if yTick > thrTick:
        yTick = 0
        if cPix < (rows - 1) * columns: 
            pixMove += columns
    elif yTick < -thrTick:
        yTick = 0
        if cPix >= columns:
            pixMove -= columns
    
    # if the button is pressed it is devounced first (bFree) and the current color
    # will be the next in the cols array, also bTime starts to count up
    # if it bTime reaches waitTime joypaint is resetted to black
    # and the current color to the first in the cols array
    if bValue == 0:
        bTime += 1
        if bFree:
            bFree = False
            cCol += 1
            if cCol > len(cols) - 1:
                cCol = 0
        if bTime >= waitTime:
            matrix.fill(0, 0, 0)
            cCol = 0
    else:
        bFree = True
        bTime = 0
            
    # the movement is now added to the current pixel
    cPix += pixMove;
    
    # if the last color in the cols array is selected the current pixel
    # will blink to indicate that it's color is not a drawing color
    # if any other color is selected it is now set with the full brightness
    # if it was the same as in the beginning if this loop because no
    # movement or color selection took place it will just be brighter
    if cCol == len(cols) - 1:
        if dirBlink > 0: matrix.set_pixel(cPix, cols[0][0] * dim, cols[0][1] * dim, cols[0][2] * dim)
        if blink > thrBlink - 1 or blink < 0: dirBlink *= -1
        blink += dirBlink
    else:
        matrix.set_pixel(cPix, cols[cCol][0] * lit, cols[cCol][1] * lit, cols[cCol][2] * lit)
    
    # update the LED matrix, all older activated pixels will stay activated
    matrix.show()
