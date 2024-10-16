import math
import os
import subprocess
import screeninfo
import Xlib.display

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def get_choice(inputs=["r", "i", ""], message="Enter your choice:", error_message="Try again, choice not recognised:"):
    the_input = input(message)
    while True:
        if the_input.lower() in inputs:
            return the_input.lower()
        else:
            the_input = input(error_message)

def get_number(message="Enter a number:", range=[0, 10000], allow_decimal=False):
    while True:
        while True:
            the_input = input(message)
            good = True
            if the_input in ["reset", "fix", "r"]:
                return "reset"

            if "." in the_input and not allow_decimal: # Checks if there is a decimal and if it should be allowed
                good = False
                print("Must be a whole number, without a decimal point.")
                break

            try: float(the_input) # Try to convert the input to a float but catch if it fails, to check for formatting errors. The response is less specific than checking for every single thing wrong with an input, but it's quicker.
            except ValueError:
                good = False
                print("Not a valid number.")
                break

            if not (range[0] <= float(the_input) <= range[1]): # Check if the input is within a range
                good = False
                print(f"Must be betwen {range[0]} and {range[1]}")

            if good:
                print(float(the_input))
                return float(the_input)

#get_number("Enter an angle", range=[-90, 90], allow_decimal=True)
#get_number("Enter an angle", range=[-90, 90], allow_decimal=True)
#get_number("Enter an angle", range=[-90, 90], allow_decimal=True)
#get_number("Enter an angle", range=[-90, 90], allow_decimal=True)



def calc_pixel_shift(angle, v_res, h_res): # Calculate the amount of pixels to shift the display horizontally by, using fancy trigonometry.
    print(f"sin{angle} = {round(math.sin(math.radians(angle)), 8)}") # math.radians is needed because python maths is weird and to prevent catastrophic failure.
    x_shift = 0
    y_shift = 0
    if angle >= 0:
        x_shift = v_res * round(math.sin(math.radians(angle)), 8)
    elif angle < 0:
        y_shift = h_res * round(math.sin(math.radians(-angle)), 8)
    print(f"X shift: {x_shift}")
    print(f"Y shift: {y_shift}")
    return x_shift, y_shift

def calc_transform_matrix(angle, v_res, h_res):
    # Using this syntax: cos(x),-sin(x),shift_left,sin(x),cos(x),shift_up,0,0,1
    r_angle = math.radians(angle) # python is dumb so this has to be done
    matrix = []
    matrix.append(round(math.cos(r_angle), 8))
    matrix.append(round(-math.sin(r_angle), 8))
    matrix.append(calc_pixel_shift(angle, v_res, h_res)[0])
    matrix.append(round(math.sin(r_angle), 8))
    matrix.append(round(math.cos(r_angle), 8))
    matrix.append(calc_pixel_shift(angle, v_res, h_res)[1])
    matrix.append(0)
    matrix.append(0)
    matrix.append(1)
    print(f"Transform: {matrix}")
    return matrix

def form_xrandr_command(matrix: list, max_size: int, display_name: str ="HDMI-1"):
    matrix_but_string = ""
    for value in matrix: # Convert the array to a string that xrandr will like
        matrix_but_string += f"{value},"
    matrix_but_string = matrix_but_string[:-1] # Remove the last character because it is a comma

    command = f"xrandr --output {display_name} --transform {matrix_but_string} --fb {max_size}x{max_size}"
    print(command)
    return command


def run_it():
    monitors = screeninfo.get_monitors()
    if len(monitors) > 1:
        counter = 0
        for monitor in monitors:
            counter += 1
            primary_text = ""
            if monitor.is_primary:
                primary_text = " (Primary Monitor)"
            print(f"{counter}:  {monitor.name}, {monitor.width}x{monitor.height}")
        mon_num = int(input(f"Enter a number monitor to choose (1-{len(monitors)}): "))
    elif len(monitors) == 1:
        print(f"Monitor detected: {monitors[0].name}, {monitors[0].width}x{monitors[0].height}")
    else:
        print("No monitors detected")
    print("Does your resolution look wrong? This can happen if you've already rotated your screen.")
    choice_reget_resolution = get_choice(["r", "i", ""], f"\nType R then enter if you want to try to get the resolution again.\nType I then enter to manually input a resolution.\n\n{color.BOLD}Or just press enter to continue with the recognised resolution.{color.END}", "Try again, choice must be R, I or just enter")
    


def take_initial_inputs():
    v_res = int(input("Enter V-Resolution: "))
    h_res = int(input("Enter H-Resolution: "))
    while True:
        angle = int(input("Enter Angle: "))
        os.system(form_xrandr_command(calc_transform_matrix(angle, v_res, h_res), v_res+h_res))

#run_it()
take_initial_inputs()
