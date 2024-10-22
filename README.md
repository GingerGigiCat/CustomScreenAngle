# Set your linux monitor to weird angles
> [!note]
> This will only work if you use **Linux**, and your display manager is **X11**, as it uses the command `xrandr` in order to set screen rotation

I had to do MATHS and TRIGONOMETRY to get this to work properly so you'd better appreciate it

Feel free to open a pull request if you have changes to make, or open an issue if you can't code but want something to be changed or fixed

## SETUP
1. Install python or use your favourite python interpreter
   > In a terminal run:
   > 
   > `sudo apt install python3` for **Debian/Ubuntu/Mint** based distros
   > ### or
   > `sudo dnf install python3` for **Fedora** distros
   > ### or
   > `sudo yum install python3` for **CentOS/RHEL** distros
   > ### or
   > `sudo pacman -S python` for **Arch** distros

2. Download main.py
3. Open it in python and run it.
   > Open a terminal in the folder that main.py was downloaded to, and run `python3 ./main.py`

## USAGE
1. Select your display/resolution if a list is given
2. Check that the resolution is correct, since it is likely to be incorrect if the screen has already been rotated by a custom angle
3. If the resolution is wrong, or to reset the angle, enter r to reset the angle and reget the resolution. If the resolution is still wrong, enter i to input a custom resolution, and probably open an issue so I can attempt to fix it.
4. Enter the angle you want to rotate to. This should rotate automatically, but if it does't, you can copy the command starting with `xrandr` that is output, into the terminal.
