import math
from vpython import *
import numpy as np
import pdb


#I0 = 1.0e-12          # W/m^2
I0 = 1.0e-6          # W/m^2

amplitude = 0.1     # units.
phase = 0             # radians
wavelength = 2.0      # m/cycle
speed_of_sound = 343  # m/s
frequency = speed_of_sound / wavelength   # cycles/sec
two_pi = 2.0 * math.pi


source1 = simple_sphere(pos=vector(-2,-3,0), color=color.red, radius=0.25)
# Phase and amplitude.
source1.amplitude = amplitude
source1.phase = phase
source1.frequency = frequency
source2 = simple_sphere(pos=vector(2,-3,0), color=color.red, radius=0.25)
source2.amplitude = amplitude
source2.phase = 0  #math.pi  # phase
source2.frequency = frequency




vertices = []
dx = 0.1
dy = 0.1
xmax = 3

decibel_max = 0
decibel_min = 351

for y in np.arange(-xmax, xmax, dy):
    for x in np.arange(-xmax, xmax, dx):
        v = box(pos=vector(x,y,0), size=vector(dx,dy,0.01))
        # phase and amplitude change.
        dist_1 = mag(v.pos - source1.pos)
        dist_1 = max(dist_1, source1.radius)
        amplitude_1  = source1.amplitude / (dist_1**2)
        phase_1 = source1.phase + two_pi * dist_1 * source1.frequency / speed_of_sound
        # phase and amplitude change.
        dist_2 = mag(v.pos - source2.pos)
        dist_2 = max(dist_2, source1.radius)
        amplitude_2  = source2.amplitude / (dist_2**2)
        phase_2 = source2.phase + two_pi * dist_2 * source2.frequency / speed_of_sound
        # Add up the vectors.
        vx_1 = amplitude_1 * cos(phase_1)
        vy_1 = amplitude_1 * sin(phase_1)
        vx_2 = amplitude_2 * cos(phase_2)
        vy_2 = amplitude_2 * sin(phase_2)
        vx = vx_1 + vx_2
        vy = vy_1 + vy_2
        vmag = math.sqrt(vx**2 + vy**2)
        
        # Plot decibels.
        decibels = 10 * math.log10(vmag / I0)
        decibel_max = max(decibel_max, decibels)
        decibel_min = min(decibel_min, decibels)
        print(x, " ", y, " : dist ", dist_1, "  mag:", decibels)
        #print(x, " ", y, " : dist ", dist_1, " ", dist_2, "  amp: ", amplitude_1, "  ", amplitude_2)

        # Scale the color range to see interference pattern.
        green = (decibels - 32.0) / 20.0
        
        v.color = vector(0, green, 0)
        #v.color = vector(0, 1, 0)
        vertices.append(v)



print(decibel_min)
print(decibel_max)
