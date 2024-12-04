import math
from vpython import *
import numpy as np
import pdb
import time

# Animate over time
# When the sources are different frequencies, interference will change over time (beats) 



I0 = 1.0e-12          # W/m^2
#I0 = 1.0e-6          # W/m^2

amplitude = 0.1 * 1e-6      # units.
phase = 0             # radians
wavelength = 2.0      # m/cycle
speed_of_sound = 343  # m/s
frequency = speed_of_sound / wavelength   # cycles/sec
two_pi = 2.0 * math.pi

print("frequency  ", frequency)


# Skip the previous simulation frames
frame_number = 120
number_of_frames = 120
number_of_cycles = 4


sources = []



source = simple_sphere(pos=vector(-2,0.5,0), color=color.red, radius=0.25)
# Phase and amplitude.
source.amplitude = amplitude
source.phase = phase
source.frequency = frequency + 10
sources.append(source)


source = simple_sphere(pos=vector(0,4,0), color=color.red, radius=0.25)
source.amplitude = amplitude
source.phase = 0  #math.pi  # phase
source.frequency = frequency
sources.append(source)


source = simple_sphere(pos=vector(2,0.5,0), color=color.red, radius=0.25)
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

for y in np.arange(0, 12, dy):
    for x in np.arange(-xmax-7, xmax+7, dx):
        vert = box(pos=vector(x,y,0), size=vector(dx,dy,0.01))
        vert.shininess = 0.0
        vertices.append(vert)


rate(2)

scene.autoscale = False
scene.camera.axis = vector(0, 0, -1)
scene.camera.pos = vector(0, 5.1, 10)
scene.camera.up = vector(0, 1, 0)

scene.camera.canvas.width = 1280
scene.camera.canvas.height = 800


my_text = text(text='Clara Law, Vicky Yan - Exploring Wave Dynamics: A Computational Model for Sound Wave Interference - Matter & Interactions I (2024)', pos=vector(0, -0.55, 0), align='center', color=color.white)
my_text.height = 0.4
my_text.length = 18.0
my_text.depth = 0

title_text = text(text='Three Sources with Different Frequencies - Time Simulation - 32 to 52 decibels ', pos=vector(0, 10.25, 0.2), align='center', color=color.white)
title_text.height = 0.4
title_text.length = 16.0
title_text.depth = 0


toggle = False

dt = 1.0 / frequency
t = 0


for time_counter in range(number_of_frames):
    t2 = number_of_cycles * time_counter / (frequency * number_of_frames)
    print("debug: ", t, "  ", t2)
    print("       time: ", t)
    print("       cycles: ", frequency * t)
    for vert in vertices:
        vx_total = 0
        vy_total = 0
        for source in sources:
            # phase and amplitude change.
            dist = mag(vert.pos - source.pos)
            dist = max(dist, source.radius)
            amplitude  = source.amplitude / (dist**2)
            phase = source.phase 
            phase += two_pi * source.frequency * t
            phase += two_pi * dist * source.frequency / speed_of_sound
            # Add up the vectors.
            vx = amplitude * cos(phase)
            vy = amplitude * sin(phase)
            vx_total += vx
            vy_total += vy
        vmag = math.sqrt(vx_total**2 + vy_total**2)
        if abs(vert.pos.x) < 0.01 and abs(vert.pos.y) < 0.01 :
            print("vmag: ", vmag)
        
        # Plot decibels.
        decibels = 10 * math.log10(vmag / I0)
        decibel_max = max(decibel_max, decibels)
        decibel_min = min(decibel_min, decibels)

        # Scale the color range to see interference pattern.
        green = (decibels - 32.0) / 20.0
        if abs(vert.pos.x) < 0.01 and abs(vert.pos.y) < 0.01 :
            print("green: ", green)
            print("vert: ", vert.pos)
            debug_vert = vert
        if True:
            vert.color = vector(0, green, 0)
        else:
            vert.color = vector(0, 0, green)
    #db.set_trace()
    print()
    #scene.capture(f"frame{frame_number:05}")
    print(time_counter, "  ", frame_number, "  ", t)
    print(two_pi * source.frequency * t)
    toggle = not toggle
    sleep(1)
    frame_number += 1
    t += dt


print(decibel_min)
print(decibel_max)
