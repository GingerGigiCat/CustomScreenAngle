<p></p>
<center><img style="max-height:40vh; margin:0 auto" src="https://cloud-m3nwxccz4-hack-club-bot.vercel.app/0pxl_20250118_222421911.mp.jpg" alt="A picture of a monitor rotated to around 45º"></center>

# Set your linux monitor to weird angles
> [!note]
> This will only work if you use **Linux**, and your display manager is **X11**, as it uses the command `xrandr` in order to set screen rotation

> [!WARNING]
> If you are using cinnamon, or any other window manager that offers fractional scaling, **DISABLE FRACTIONAL SCALING**, trust me i know from experience
> 
> Also, you may want to consider killing cinnamon so that it goes into fallback mode, which stops flickering when changing angles



I had to do MATHS and TRIGONOMETRY to get this to work properly so you'd better appreciate it

Feel free to open a pull request if you have changes to make, or open an issue if you can't code but want something to be changed or fixed

Yes the monitor is still fully usable.

I have no idea what will happen if you try with multiple monitors, I haven't tried.

## Now with automatic rotation with a microbit!

To use with a microbit, just upload the python microbit files `microbit_on_monitor.py` and `microbit_receiver.py` to https://python.microbit.org/v/3/, then save hex files and put them on the microbits.

Ideally, the microbit should be mounted so that the display of the microbit is parallel to the display of your monitor. I would have 3D printed a bracket to attach it to my monitor, but I don't have a 3D printer (yet)

The microbit on the monitor wirelessly transmits to the microbit at the computer

If using with microbits, run `pc_microbit_adapter.py` on the pc. It should automatically detect your monitor and prompt you through a setup process.

The angle will be automatically set when you are rotating your display! It will snap to -90, 0 and 90 degrees, because that's probably what you actually want your monitor set as.

A more practical use case with this, than using wacky rotations, is automatically rotating only between portrait and landscape, which this can do! You are prompted whether to enable it in the setup, and you can edit it in the json file `auto_rotate_config.json`



## Setup
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

2. Download main.py, or do `git clone https://github.com/GingerGigiCat/CustomScreenAngle`
3. Open it in python and run it.
   > Open a terminal in the folder that main.py was downloaded to with `cd CustomScreenAngle` to go into the folder if you did git clone, and run `python3 ./main.py`

## Usage
1. Select your display/resolution if a list is given
2. Check that the resolution is correct, since it is likely to be incorrect if the screen has already been rotated by a custom angle
3. If the resolution is wrong, or to reset the angle, enter r to reset the angle and reget the resolution. If the resolution is still wrong, enter i to input a custom resolution, and probably open an issue so I can attempt to fix it.
> [!note]
> Note that if your display becomes unusable, you can enter `r` or `0` as the angle, to **reset the rotation**
4. Enter the angle you want to rotate to (between -90 and 90, or else linux cries in pain). This should rotate automatically, but if it doesn't, you can copy the command starting with `xrandr` that is output, into the terminal.


## Gallery
This was the old cover image
<center><img style="max-height:40vh; margin:0 auto" src="https://cloud-6d0f8u903-hack-club-bot.vercel.app/0pxl_20241016_201340650.mp_2.jpg" alt="A picture of a monitor rotated to around 45º"></center>


You can have just a slight tilt
<center><img style="max-height:40vh; margin:0 auto" src="https://cloud-3erbv079e-hack-club-bot.vercel.app/0pxl_20241016_201435065.mp.jpg" alt="A picture of a monitor rotated to around 15º"></center>


You can optimise to have the most lines of code possible from corner to corner. You can also do this to fit the longest lines of code horizontally, so you can finally fit your whole Java class names on one line (fit not guaranteed)
<center><img style="max-height:40vh; margin:0 auto" src="https://cloud-3erbv079e-hack-club-bot.vercel.app/1pxl_20241016_201542358.mp_2.jpg" alt="A picture of a monitor rotated to fit the most lines of code from corner to corner"></center>
