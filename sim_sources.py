import math
from vpython import *
import numpy as np
import pdb
import time

# Animate over time
# When the sources are different frequencies, interference will change over time (beats) 



#I0 = 1.0e-12          # W/m^2
I0 = 1.0e-6          # W/m^2

amplitude = 0.1     # units.
phase = 0             # radians
wavelength = 2.0      # m/cycle
speed_of_sound = 343  # m/s
frequency = speed_of_sound / wavelength   # cycles/sec
two_pi = 2.0 * math.pi

print("frequency  ", frequency)



sources = []

source = simple_sphere(pos=vector(-2,-3,0), color=color.red, radius=0.25)
# Phase and amplitude.
source.amplitude = amplitude
source.phase = phase
source.frequency = frequency + 10
sources.append(source)

source = simple_sphere(pos=vector(2,-3,0), color=color.red, radius=0.25)
source.amplitude = amplitude
source.phase = 0  #math.pi  # phase
source.frequency = frequency
sources.append(source)


source = simple_sphere(pos=vector(0,-2,0), color=color.red, radius=0.25)
source.amplitude = amplitude
source.phase = 0  #math.pi  # phase
source.frequency = frequency
sources.append(source)




vertices = []
dx = 0.1
dy = 0.1
xmax = 3

decibel_max = 0
decibel_min = 351

for y in np.arange(-xmax, xmax, dy):
    for x in np.arange(-xmax, xmax, dx):
        vert = box(pos=vector(x,y,0), size=vector(dx,dy,0.01))
        vert.shininess = 0.0
        vertices.append(vert)



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
        phase += two_pi * dist * source.frequency / speed_of_sound
        # Add up the vectors.
        source_vx = amplitude * cos(phase)
        source_vy = amplitude * sin(phase)
        total_vx += source_vx 
        total_vy += source_vy 
    vmag = math.sqrt(total_vx**2 + total_vy**2)    
    decibels = 10 * math.log10(vmag / I0)
    decibel_max = max(decibel_max, decibels)
    decibel_min = min(decibel_min, decibels)

    # Scale the color range to see interference pattern.
    green = (decibels - 35.0) / 20.0
        
    vert.color = vector(0, green, 0)


print(decibel_min)
print(decibel_max)
