#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 10:22:29 2019

@author: daniel
"""


from numba import njit
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
from matplotlib import animation
from IPython.display import HTML

@njit
def game_of_life_jit(world):
    """
    Calculates the next state of the game of life for a given array. 

    parameters:
    world (np.ndarray): a two-dimentional binary numpy array
    
    returns:
    next_state (np.ndarray): The next time step of world in the game of life
    """
    next_state = np.empty_like(world)
    width, height = world.shape
    for x in range(width):
        for y in range(height):
            neighbours = 0
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if i != 0 or j != 0:
                        xi = (x+i + width)%width
                        yj = (y+j + height)%height
                        neighbours += world[xi, yj]
                if neighbours == 3:
                    next_state[x,y] = 1
                elif neighbours == 2 and world[x,y] == 1:
                    next_state[x,y] = 1
                else:
                    next_state[x,y] = 0
    return next_state


if __name__ == "__main__":
    world = np.zeros(shape = (300, 300))
    for x in [150]:
        world[x, 50:250] = 1
        world[x-5, 50:250] = 1
        world[x+5, 50:250] = 1
    fig, ax = plt.subplots(figsize = (10,10))
    img = ax.imshow(world, cmap = "gray")
    
    
    def init():
        return img,
    
    def animate(i):
        global world
        world = game_of_life_jit(world)
        ax.set_title(f"step {i}")
        img.set_data(world)
        img.autoscale()
        fig.canvas.draw()
        return img,
    
    a = animation.FuncAnimation(fig, animate, init_func=init, blit=True, interval = 5, frames = 1000, repeat = False)
    plt.show()