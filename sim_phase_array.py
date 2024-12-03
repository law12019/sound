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
    source = simple_sphere(pos=vector(-3+(index*0.5),-6,0), color=color.red, radius=0.25)
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

scene.lights[0].pos.x = 10
scene.lights[1].pos.x = 10

decibel_max = 0
decibel_min = 351

for y in np.arange(-6, 4, dy):
    for x in np.arange(-xmax-3, xmax+3, dx):
        vert = box(pos=vector(x,y,0), size=vector(dx,dy,0.01))
        vertices.append(vert)




# animate the direction
for dir_x in range(30):
    green_min = 10000
    green_max = 0
    # change the phases
    spot.x = (dir_x / 2) - 7
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
        # print(vert.pos.y)    y goes from -6 to 0
        green = (decibels*((vert.pos.y + 40)/37) - db_min) / (db_max - db_min)
        #green = (decibels - db_min) / (db_max - db_min)
        green_min = min(green_min, green)
        green_max = max(green_max, green)

        vert.color = vector(0, green, 0)

    print(green_min, "  ", green_max)
    sleep(1)


