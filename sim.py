import cv2
import numpy as np
from collections import deque


# I actually think distance propagation will work, but all sources have to be set at the start of propagation.
# each node only cares about its neighbor as a source.
# This is similar to simualtion of steady state electronic circuits.
# Can we propagate distance squared to avoid city block distance artifacts?


queue = deque()

# Adding elements (enqueue)
#queue.append(1)
#queue.append(2)
#queue.append(3)

# Removing elements (dequeue)
#print(queue.popleft())
#print(queue.popleft())


# How to simulate sound reflection.
# Distance (mag,phase) seems problematic.
# Computation has to revist locations.
# 1: (mag,phase) is a steady state solution
# 2: Does it work for all cells acting like a source.
# 3: Treat speaker like a sync?


# I could model presure and momentum.
# 1: Ball and spring mesh.
# 2: cell presure and face flow.



# first two are the complex sound energy,  The third is barrier.
WIDTH = 512
HEIGHT = 512
SPACE1 = np.zeros((HEIGHT, WIDTH, 3))
SPACE2 = np.zeros((HEIGHT, WIDTH, 3))
# 0:empty, 1:boundary, 2:blackhole, -1:visited
# Mark boundary as black hole (not obstacle, no reflection)
# to avoid dealing with boundary condition during search
SPACE1[0,:,2] = 1
SPACE1[HEIGHT-1,:,2] = 1
SPACE1[:,0,2] = -1
SPACE1[:,WIDTH-1,2] = 1
SPACE2[0,:,2] = 1
SPACE2[HEIGHT-1,:,2] = 1
SPACE2[:,0,2] = -1
SPACE2[:,WIDTH-1,2] = 1
QUEUE = deque()
# Cycles per space_unit
FREQ = 0.125

def add_sound(x,y, r,i):
    global SPACE1
    global QUEUE
    if x < 1 or x >= SPACE1.shape[1]:
        return
    if y < 0 or y > SPACE1.shape[0]:
        return
    if SPACE1[y,x,2] != 0:
        return
    #QUEUE.append((x,y,r,i))
    SPACE1[y,x,:] = [r,i,-1]


def run():
    global SPACE1
    global SPACE2
    #global QUEUE
    #phase change for face neighbors
    face_phase = (math.cos(

    
    while True:
        SPACE2[:,:,0:2] = 0
        for y in range(1,height-1):
            for x in range(1,width-1):
                dist = 1
                


        x,y,r,i = QUEUE.popleft()
        # Visit 8 neighbors.
        count = 0
        for x in range(-1,2):
            for y in range(-1,2):
                if 
                

# Put in two sound sources
add_sound(246,450)
add_sound(266,450)
















