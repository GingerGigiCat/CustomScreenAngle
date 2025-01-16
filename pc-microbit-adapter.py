import serial
import serial.tools.list_ports
from main import set_angle, monitor_selection, get_choice
import json
from screeninfo import Monitor

ports = list(serial.tools.list_ports.comports())
port_to_use = None
for port in ports:
    if "micro:bit" in str(port):
        print(f"Microbit found! At {port.device}")
        port_to_use = port.device

ser = serial.Serial(port_to_use, 115200)

def get_average_accelerometer(readings=50):
    i = 0
    average_accelerometer = 0
    ser.flush()
    while i < readings:
        theline = ser.readline()
        theline = theline.decode("utf-8")
        theline = theline.strip("\r").strip("\n")
        if theline:
            if i == 0:
                average_accelerometer = int(theline)
            else:
                average_accelerometer = (int(theline) + average_accelerometer) / 2

            i += 1

    return average_accelerometer

def accelerometer_to_angle(acc_reading, the_config):
    if the_config["reversed"]:
        minimum = the_config["angle_right90_avg"]
        maximum = the_config["angle_left90_avg"]
    else:
        minimum = the_config["angle_left90_avg"]
        maximum = the_config["angle_right90_avg"]

    zero_offset = the_config["angle_0_avg"]

    minimum -= zero_offset
    maximum -= zero_offset
    acc_reading -= zero_offset

    angle = acc_reading / maximum * 90
    return angle



def calibrate(monitor: Monitor):
    with open("auto_rotate_config.json", "w+") as the_file:
        content = the_file.read()
        if "{" in content and "}" in content:
            the_config = json.loads(content)
        else:
            the_config = {}

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

        average_accelerometer_0 = get_average_accelerometer(100)
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

        average_accelerometer_left90 = get_average_accelerometer(100)
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
        ∥bottom      top|
        ∥               |
        ∥               |
        ∥               |
        ∥               |
        ∥     right     |
        -----------------
        
        Then press enter.
        """)
        print("Getting data... Don't move the microbit/monitor")

        average_accelerometer_right90 = get_average_accelerometer(100)
        the_config["angle_right90_avg"] = average_accelerometer_right90
        print(f"Average accelerometer reading: {average_accelerometer_right90}")
        set_angle(90, monitor)

        if average_accelerometer_right90 > average_accelerometer_left90:
            the_config["reversed"] = False
        else:
            the_config["reversed"] = True

        input("\n\n\nGreat! Now physically rotate back to your favourite normal rotation, then press enter.")

        current = get_average_accelerometer(50)
        angle = accelerometer_to_angle(current, the_config)

        # User config



while True:
    theline = ser.readline()
    theline = theline.decode("utf-8")
    theline = theline.strip("\r").strip("\n")
    if theline:
        print(theline)