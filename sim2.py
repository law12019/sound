from vpython import *
import numpy as np
import pdb



wavelength = 2.0


source1 = simple_sphere(pos=vector(-2,-3,0), color=color.red, radius=0.25)
source2 = simple_sphere(pos=vector(2,-3,0), color=color.red, radius=0.25)


vertices = []
dx = 0.1
dy = 0.1
xmax = 3

for x in np.arange(-xmax, xmax, dx):
    for y in np.arange(-xmax, xmax, dy):
        v = box(pos=vector(x,y,0), size=vector(dx,dy,0.01))
        path_difference = abs(mag(v.pos - source1.pos) - mag(v.pos -source2.pos))
        n = path_difference % wavelength
        brightness = abs(n-0.5) / 0.5
        v.color = vector(brightness, 0, 0)
        vertices.append(v)
