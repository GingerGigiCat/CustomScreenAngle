import math
import os

def calc_x_shift(angle, v_res):
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

def form_xrandr_command(matrix, display_name="HDMI-1"):
    matrix_but_string = ""
    for value in matrix: # Convert the array to a string that xrandr will like
        matrix_but_string += f"{value},"
    matrix_but_string = matrix_but_string[:-1] # Remove the last character because it is a comma

    command = f"xrandr --output {display_name} --transform {matrix_but_string}"
    print(command)
    return command
def take_inputs():
    v_res = int(input("Enter V-Resolution: "))
    angle = int(input("Enter Angle: "))
    form_xrandr_command(calc_transform_matrix(angle, v_res))

take_inputs()
