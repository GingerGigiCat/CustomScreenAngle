from microbit import *
import radio

radio.on()
radio.config(group=24, power=3)

while True: # Literally just send from microbit to computer so that the python script on the computer can do most of the processing
    received = radio.receive()
    if received:
        print(received)
        display.set_pixel(0, 0, 7)
    else:
        display.set_pixel(0, 0, 1)