from microbit import *
import radio

rotat90 = Image("00200:"
                "00200:"
                "00200:"
                "00200:"
                "00200:")

rotat2 = Image("02000:"
               "00200:"
               "00200:"
               "00200:"
               "00020:")

rotat3 = Image("02000:"
               "02000:"
               "00200:"
               "00020:"
               "00020:")

rotat4 = Image("20000:"
               "02000:"
               "00200:"
               "00020:"
               "00002:")

rotat5 = Image("00000:"
               "22000:"
               "00200:"
               "00022:"
               "00000:")

rotat6 = Image("00000:"
               "20000:"
               "02220:"
               "00002:"
               "00000:")

rotatflat = Image("00000:"
                  "00000:"
                  "22222:"
                  "00000:"
                  "00000:")

rotat8 = Image("00000:"
               "00002:"
               "02220:"
               "20000:"
               "00000:")

rotat9 = Image("00000:"
               "00022:"
               "00200:"
               "22000:"
               "00000:")

rotat10 = Image("00002:"
                "00020:"
                "00200:"
                "02000:"
                "20000:")

rotat11 = Image("00020:"
                "00020:"
                "00200:"
                "02000:"
                "02000:")

rotat12 = Image("00020:"
                "00200:"
                "00200:"
                "00200:"
                "02000:")


accelerometer.set_range(2)
radio.on()
radio.config(group=24, power=3)


while True:
    x_val = accelerometer.get_x()
    if x_val/1000 < -6.5/7: # These if statements show a rotated line on the microbit screen that should appear flat with the rotation
        display.show(rotat90)
    elif x_val/1000 < -6/7:
        display.show(rotat2)
    elif x_val/1000 < -5.5/7:
        display.show(rotat3)
    elif x_val/1000 < -4.5/7:
        display.show(rotat4)
    elif x_val/1000 < -2.5/7:
        display.show(rotat5)
    elif x_val/1000 < -1.5/7:
        display.show(rotat6)
    elif x_val/1000 < 1.5/7:
        display.show(rotatflat)

    elif x_val/1000 < 2.5/7:
        display.show(rotat8)
    elif x_val/1000 < 4/7:
        display.show(rotat9)
    elif x_val/1000 < 5.5/7:
        display.show(rotat10)
    elif x_val/1000 < 6/7:
        display.show(rotat11)
    elif x_val/1000 < 6.5/7:
        display.show(rotat12)
    else:
        display.show(rotat90)
    print(x_val, x_val/1000 * 7)
    radio.send(str(x_val))
