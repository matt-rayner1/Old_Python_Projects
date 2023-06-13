import matplotlib.pyplot as plt
import random
from scipy.stats.mstats import gmean
from math import sin, cos, pi

#-------------------------------------------------------------------------INTRO
"""
NAME: the_wibbler.py
AUTHOR: matt rayner

DESCRIPTION: Creates a series of .pngs to use to create a nice calming gif
             (in conjunction with "gif_make.py")
             Yes, this code is an absolute shit show. 
             No. I will not make it any better.

USAGE: no command line arguments or user input at runtime. change values in
       the program as needed directly for different changes (described below)
       
NOTE: probably best to put this file in a dedicated folder, as it will
      spit out 50 .pngs all over your face
"""

#------------------------------------------------------------------------SET UP
points = 50
 
#more frames makes a slower but more detailed .gif 
#(unless you change "duration" in gif_make.py)
frames = 50

#+200 offset as gmean() only works with positive values
x_init = [random.randint(1,100) + 200 for i in range(points)]
y_init = [random.randint(1,100) + 200 for i in range(points)]

#change scales_x/y for larger or smaller wibbling behaviour
scales_x = [random.uniform(1,5) for i in range(points)]
scales_y = [random.uniform(1,5) for i in range(points)]

#"choice" is for use with ULTRA-WIBBLE. comment out if not in use
#choice = [random.randint(1,4) for i in range(points)]

#set size of final plots. each added value adds 72 pixels (8 * 72 = 576 pixels)
fig= plt.figure(figsize=(8,8))

#-------------------------------------------------------PLOT GENERATOR FUNCTION
def plot_make(points, plot_no, x, y):
    gmean_x = 0
    gmean_y = 0
    theta = (plot_no/frames) * -2 * pi
    
    #!!!!!!!!!!WARNING: INCOMING CLUSTERFUCK OF ZOMBIE CODE!!!!!!!!!!!
    
    #for ULTRA-WIBBLE behaviour try this entire loop (replace other loops: )
    #(also remember to de-comment "choice" variable in SET-UP section)
    """
    for i in range(points):
        if choice[i] == 1:
            x[i] -= scales_x[i] * cos(theta)
            y[i] += scales_y[i] * sin(theta)
        elif choice[i] == 2:
            x[i] += scales_x[i] * cos(-theta)
            y[i] += scales_y[i] * sin(-theta)
        elif choice[i] == 3:
            x[i] -= scales_x[i] * cos(theta)
            y[i] -= scales_y[i] * sin(theta)    
        elif choice[i] == 4:
            x[i] += scales_x[i] * cos(theta)
            y[i] += scales_y[i] * cos(theta)
    """
    #for RANDOM-WIBBLE behaviour try this entire loop (replace other loops: )
    """
    for i in range(points):
        dice = random.randint(1,3)
        if dice == 1:
            x[i] -= scales_x[i] * cos(theta)
            y[i] += scales_y[i] * sin(theta)
        elif dice == 2:
            x[i] += scales_x[i] * cos(-theta)
            y[i] += scales_y[i] * sin(-theta)
        elif dice == 3:
            x[i] -= scales_x[i] * cos(theta)
            y[i] -= scales_y[i] * sin(theta)
    """
    #default wibbling behaviour. Try different versions for different results.
    for i in range(points):
        if i % 2 == 1:
            x[i] += scales_x[i] * cos(theta)
            y[i] += scales_y[i] * sin(theta)
        else:
            #version 1
            x[i] -= scales_x[i] * cos(theta)
            y[i] += scales_y[i] * sin(theta)
            #version 2
            #x[i] += scales_x[i] * cos(-theta)
            #y[i] += scales_y[i] * sin(-theta)
            #version 3
            #x[i] -= scales_x[i] * cos(theta)
            #y[i] -= scales_y[i] * sin(theta)

    gmean_x = gmean(x)
    gmean_y = gmean(y)
    
    #draws a line from each point to the central geometric mean point
    #bit of a kludge but it works fine
    for i in range(points):
        temp_x = [x[i], gmean_x]
        temp_y = [y[i], gmean_y]
        plt.plot(temp_x, temp_y, 'mo', linestyle = '-', markersize = 5)
        plt.plot(gmean_x, gmean_y, 'mo', markersize = 10)
    
    #saves current plot in a .png and clears the plot so loop can repeat again
    #if the wibbler is wibbling off the screen change the x and y lims
    #{:03d} used to avoid sorting errors in gif_make.py
    axes = plt.gca()
    axes.set_xlim([100,400])
    axes.set_ylim([100,400])
    plt.axis("off")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig('plot_{:03d}.png'.format(plot_no))
    plt.clf()
    
    return x, y

#---------------------------------------------------------RECURSIVE DRIVER LOOP
for plot_no in range(frames):
    x_init, y_init = plot_make(points, plot_no, x_init, y_init)