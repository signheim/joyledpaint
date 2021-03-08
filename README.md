# JOYLEDPAINT
Raspberry Pi Pico Joystick 8x8 WS2812 Paint App

Needs pico_ws2812b library by benevpi (https://github.com/benevpi):
https://github.com/benevpi/pico_python_ws2812b

# How it works
Simple paint app for a 64 pixel 8x8 led matrix
with one-button control of all functions.

Move the joystick to color LED pixels with
a chosen color. Switch color by pressing the
button. Cycle through several colors
(including a delete mode). Press the button
long enough to erase the screen and start
new.

# Code preparations
Install the pico_ws2812b library by benevpi by
saving it to the pico (i.e. with Thonny) and name
it 'ws2812b.py'.

Also save the 'joyledpaint.py' as 'main.py'
to the pico to enable it without computer
connection.

# Parts
  - Raspberry Pi Pico
  - hw-504 joystick
  - 8x8 ws2812 led matrix

# Wiring
  - Joystick
    VRx -> GP27
    VRy -> GP26
    SW  -> GP16

  - 8x8 WS2812 LED Matrix
    din -> GP5
