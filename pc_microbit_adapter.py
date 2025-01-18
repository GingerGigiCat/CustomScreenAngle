import serial
import serial.tools.list_ports
from main import set_angle, monitor_selection, get_choice
import json
from screeninfo import Monitor
import time
import math

ports = list(serial.tools.list_ports.comports())
port_to_use = None
for port in ports:
    if "micro:bit" in str(port):
        print(f"Microbit found! At {port.device}")
        port_to_use = port.device

ser = serial.Serial(port_to_use, 115200)

def get_average_accelerometer(readings=50):
    i = 0
    total = 0
    temp = ser.read_all()
    temp = ser.readline()
    while i < readings:
        theline = ser.readline()
        #print(theline)
        theline = theline.decode("utf-8")
        theline = theline.strip("\r").strip("\n")
        if "<DAPLink:Overflow>" in theline:
            #print("RESETTINGS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            total = 0
            i = 0
            continue
        if theline:
            try:
                int(theline)
            except ValueError:
                #print(theline)
                continue
            if i == 0:
                total = int(theline)
            else:
                total += int(theline)

            i += 1

    return total / readings

def accelerometer_to_angle(acc_reading, the_config):
    if the_config["reversed"]:
        minimum = the_config["angle_right90_avg"]
        maximum = the_config["angle_left90_avg"]
    else:
        minimum = the_config["angle_left90_avg"]
        maximum = the_config["angle_right90_avg"]

    zero_offset = the_config["angle_0_avg"]
    #print(acc_reading)
    minimum -= zero_offset
    maximum -= zero_offset
    adjusted_acc_reading = acc_reading - zero_offset
    if adjusted_acc_reading < 0:
        adjusted_acc_reading = (adjusted_acc_reading / -minimum) * 1000
    else:
        adjusted_acc_reading = (adjusted_acc_reading / maximum) * 1000
    #print(adjusted_acc_reading)



    angle = math.degrees(math.asin(min(max(adjusted_acc_reading / 1000, -1), 1))) # See https://www.bbc.co.uk/bitesize/guides/zcrccdm/revision/7 this makes sure it's actually the right angle
    #angle = acc_reading / maximum * 90 # <--- BAD SILLY CODE
    #print(angle)
    #print("\n\n")
    if the_config["reversed"]:
        angle = 0-angle
    return angle



def calibrate(monitor: Monitor):
    try:
        the_file = open("auto_rotate_config.json", "r")
    except FileNotFoundError:
        the_file = open("auto_rotate_config.json", "w+")

    content = the_file.read()
    print(content)
    if "{" in content and "}" in content:
        the_config = json.loads(content)
        if get_choice(["y", "n"], "Config found! Do you want to use it? (y/n) ", "Must be y or n ") == "y":
            the_file.close()
            return the_config
        else:
            the_file.close()
            the_file = open("auto_rotate_config.json", "w+")
    else:
        the_config = {}
        the_file.close()
        the_file = open("auto_rotate_config.json", "w+")

    input(
    """First, make sure the microbit is attached to the screen so that it is parallel to the monitor. 
    
    Now, make sure the screen is at 0º 
    
    --------------------------------
    |             top              |
    |                              |
    | left                   right |
    |                              |
    |            bottom            |
    ================================
    
    Then press enter.
    """)
    print("Getting data... Don't move the microbit/monitor")

    average_accelerometer_0 = get_average_accelerometer(400)
    the_config["angle_0_avg"] = average_accelerometer_0

    print(f"Average accelerometer reading: {average_accelerometer_0}")


    input(
    """
    Next, physically rotate the screen anticlockwise to -90º
    
    -----------------
    |     right     ∥
    |               ∥
    |               ∥
    |               ∥
    |               ∥
    |top      bottom∥
    |               ∥
    |               ∥
    |               ∥
    |               ∥
    |     left      ∥
    -----------------
    
    Then press enter.
    """)
    print("Getting data... Don't move the microbit/monitor")

    average_accelerometer_left90 = get_average_accelerometer(400)
    the_config["angle_left90_avg"] = average_accelerometer_left90
    print(f"Average accelerometer reading: {average_accelerometer_left90}")
    set_angle(-90, monitor)


    input(
    """
    
    Ok, now rotate the screen all the way around clockwise to 90º past 0
    
    -----------------
    ∥     left      |
    ∥               |
    ∥               |
    ∥               |
    ∥               |
    ∥bottom      top|          (see how the little picture to the left
    ∥               |           has changed, isn't that nice?)
    ∥               |
    ∥               |
    ∥               |
    ∥     right     |
    -----------------
    
    Then press enter.
    """)
    print("Getting data... Don't move the microbit/monitor")

    average_accelerometer_right90 = get_average_accelerometer(400)
    the_config["angle_right90_avg"] = average_accelerometer_right90
    print(f"Average accelerometer reading: {average_accelerometer_right90}")
    set_angle(90, monitor)

    if average_accelerometer_right90 > average_accelerometer_left90:
        the_config["reversed"] = False
    else:
        the_config["reversed"] = True

    input("\n\n\nGreat! Now physically rotate back to your favourite normal rotation, then press enter.")

    current = get_average_accelerometer(100)
    angle = accelerometer_to_angle(current, the_config)
    print(f"Current raw accelerometer reading: {current}, current angle: {round(angle, 3)}º")
    print(current, angle)

    if angle < -45:
        set_angle(-90, monitor)
    elif angle < 45:
        set_angle(0, monitor)
    elif angle < 135:
        set_angle(90, monitor)

    # User config
    wacky_choice = get_choice(["y", "n"], "Do you want to enable wacky rotations, such as 30º, -53º etc? (y/n) ", "Must be y or n ")
    if wacky_choice == "y":
        the_config["allow_wacky_rotations"] = True


    save_choice = get_choice(["y", "n"], "Do you want to save this calibration config? (y/n) ", "Must be y or n ")
    if save_choice == "y":
        content = json.dumps(the_config)

        the_file.write(content)

    return the_config


print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
the_monitor = monitor_selection()
the_config = calibrate(monitor=the_monitor)
allow_wacky = the_config["allow_wacky_rotations"]
current_angle = 0
time_of_last_change = 0
time_of_last_big_angle_change = 0
last_big_angle = 0

while True:
    current_acc = get_average_accelerometer(50)
    angle = accelerometer_to_angle(current_acc, the_config)

    if allow_wacky:
        if angle < -82:
            new_angle = -90
        elif angle < -4:
            new_angle = angle
        elif angle < 4:
            new_angle = 0
        elif angle < 82:
            new_angle = angle
        elif angle >= 82:
            new_angle = 90

    else:
        if angle < -45:
            new_angle = -90
        elif angle < 45:
            new_angle = 0
        elif angle < 135:
            new_angle = 90

    if (current_angle - new_angle > 1 or current_angle - new_angle < -1) or time.time_ns() / 1000000 - time_of_last_big_angle_change < 1000:
        set_angle(new_angle, the_monitor, print_output=False)
        current_angle = new_angle
        #print(new_angle)

        if (last_big_angle - new_angle > 1 or last_big_angle - new_angle < -1):
            last_big_angle = new_angle
            time_of_last_big_angle_change = time.time_ns() / 1000000  # time in milliseconds

