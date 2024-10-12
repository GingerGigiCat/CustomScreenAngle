import math
import os
import subprocess

def calc_x_shift(angle, v_res): # Calculate the amount of pixels to shift the display horizontrally by, using fancy trigonometry.
    print(f"Angle: {angle}")
    print(f"V_res: {v_res}")
    print(f"sin{angle} = {round(math.sin(math.radians(angle)), 8)}") # math.radians is needed because python maths is weird and to prevent catastrophic failure.
    x_shift = v_res * round(math.sin(math.radians(angle)), 8)
    print(f"X shift: {x_shift}")
    return x_shift

def calc_transform_matrix(angle, v_res):
    # Using this syntax: cos(x),-sin(x),shift_left,sin(x),cos(x),shift_up,0,0,1
    r_angle = math.radians(angle) # python is dumb so this has to be done
    matrix = []
    matrix.append(round(math.cos(r_angle), 8))
    matrix.append(round(-math.sin(r_angle), 8))
    matrix.append(calc_x_shift(angle, v_res))
    matrix.append(round(math.sin(r_angle), 8))
    matrix.append(round(math.cos(r_angle), 8))
    matrix.append(0)
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
def take_inputs():
    v_res = int(input("Enter V-Resolution: "))
    h_res = int(input("Enter H-Resolution: "))
    while True:
        angle = int(input("Enter Angle: "))
        os.system(form_xrandr_command(calc_transform_matrix(angle, v_res), v_res+h_res))

take_inputs()
