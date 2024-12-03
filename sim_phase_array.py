import math
from vpython import *
import numpy as np
import pdb
import time


# Phase array of sources for directed beam


#I0 = 1.0e-12          # W/m^2
I0 = 1.0e-6          # W/m^2

amplitude = 0.1     # units.
phase = 0             # radians
wavelength = 2.0      # m/cycle
speed_of_sound = 343  # m/s
frequency = speed_of_sound / wavelength   # cycles/sec
two_pi = 2.0 * math.pi

print("frequency  ", frequency)


spot = vector(0,9,0)


sources = []

for index in range(13):
    source = simple_sphere(pos=vector((index*0.5-3),0.5,0), color=color.red, radius=0.25)
    # Phase and amplitude.
    source.amplitude = amplitude
    source.frequency = frequency
    # compute the phase to get reinforcement at a point.
    dist = mag(spot - source.pos)
    source.phase = - two_pi * dist * frequency / speed_of_sound
    sources.append(source)


db_min = 48
db_max = 54


vertices = []
dx = 0.1
dy = 0.1
xmax = 3


decibel_max = 0
decibel_min = 351

for y in np.arange(0, 12, dy):
    for x in np.arange(-xmax-6, xmax+6, dx):
        vert = box(pos=vector(x,y,0), size=vector(dx,dy,0.01))
        vert.shininess = 0.0
        vertices.append(vert)

scene.autoscale = False
scene.camera.axis = vector(0, 0, -1)
scene.camera.pos = vector(0, 6, 10)
scene.camera.up = vector(0, 1, 0)



# animate the direction
for dir_x in range(60):
    green_min = 10000
    green_max = 0
    # change the phases.  Move the beam back and forth
    if dir_x < 30:
        spot.x = (dir_x / 2) - 7
    else:
        spot.x = ((60-dir_x) / 2) - 7
        
    for source in sources:
        dist = mag(spot - source.pos)
        source.phase = - two_pi * dist * frequency / speed_of_sound
    
    for vert in vertices:
        # Sum up contribution from all sources at this vertex
        total_vx = 0
        total_vy = 0
        for source in sources:
            # phase and amplitude change.
            dist = mag(vert.pos - source.pos)
            dist = max(dist, source.radius)
            #amplitude  = source.amplitude / (dist**2)
            # Use a 2d simulation to show the beam better (it will not decrease with distance).
            amplitude  = source.amplitude / (dist)
            phase = source.phase 
            #phase += two_pi * source.frequency * t
            phase += two_pi * dist * source.frequency / speed_of_sound
            # Add up the vectors.
            source_vx = amplitude * cos(phase)
            source_vy = amplitude * sin(phase)
            total_vx += source_vx 
            total_vy += source_vy 
        vmag = math.sqrt(total_vx**2 + total_vy**2)
        
        # Plot decibels.
        decibels = 10 * math.log10(vmag / I0)
        decibel_max = max(decibel_max, decibels)
        decibel_min = min(decibel_min, decibels)
        #print(x, " ", y, " : dist ", dist_1, "  mag:", decibels)
        #print(x, " ", y, " : dist ", dist_1, " ", dist_2, "  amp: ", amplitude_1, "  ", amplitude_2)

        # Scale the color range to see interference pattern.
        # print(vert.pos.y)    y goes from -6 to 0
        #green = (decibels*((vert.pos.y + 40)/37) - db_min) / (db_max - db_min)
        green = (decibels - db_min) / (db_max - db_min)
        green_min = min(green_min, green)
        green_max = max(green_max, green)

        vert.color = vector(0, green, green)

    #pdb.set_trace()
    print(green_min, "  ", green_max)
    sleep(1)


