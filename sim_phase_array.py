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


spot = vector(0,2,0)


sources = []

for index in range(13):
    source = simple_sphere(pos=vector(-3+(index*0.5),-3,0), color=color.red, radius=0.25)
    # Phase and amplitude.
    source.amplitude = amplitude
    source.frequency = frequency
    # compute the phase to get reinforcement at a point.
    dist = mag(spot - source.pos)
    source.phase = - two_pi * dist * frequency / speed_of_sound
    sources.append(source)


db_min = 45
db_max = 50


vertices = []
dx = 0.1
dy = 0.1
xmax = 3

decibel_max = 0
decibel_min = 351

for y in np.arange(-xmax, xmax, dy):
    for x in np.arange(-xmax, xmax, dx):
        vert = box(pos=vector(x,y,0), size=vector(dx,dy,0.01))
        vertices.append(vert)




# animate the direction
for dir_x in range(30):
    # change the phases
    spot.x = (dir_x / 10) - 1.5
    for source in sources:
        source.phase = - two_pi * dist * frequency / speed_of_sound
        dist = mag(spot - source.pos)
    
    for vert in vertices:
        # Sum up contribution from all sources at this vertex
        total_vx = 0
        total_vy = 0
        for source in sources:
            # phase and amplitude change.
            dist = mag(vert.pos - source.pos)
            dist = max(dist, source.radius)
            amplitude  = source.amplitude / (dist**2)
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
        green = (decibels - db_min) / (db_max - db_min)
        
        vert.color = vector(0, green, 0)
    sleep(1)


