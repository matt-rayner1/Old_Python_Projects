from PIL import Image
import glob

#-------------------------------------------------------------------------INTRO
#NAME: gif_make.py
#AUTHOR: matt rayner (but basically copied and pasted from solutions online)

#DESCRIPTION: creates a .gif from ordered .png files located in the same folder
#USAGE: just run the script in the same place as your .pngs.
#       loop = 0: infinite loop, duration = 50: duration in ms of each frame

#------------------------------------------------------------------BEGIN SCRIPT
frames = []

imgs = glob.glob("*.png")

for img in imgs:
    new_frame = Image.open(img)
    frames.append(new_frame)
    
frames[0].save("animation.gif", format="GIF", 
                  append_images = frames[1:], 
                  save_all = True,
                  duration = 50, loop = 0)