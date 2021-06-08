import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import yaml
from skimage.graph import route_through_array

def makeArrays(route):
    routeNew = []
    for x in route:
      routeNew.append(x)
    return routeNew



# make initial population for genetic algorithm
def initialize_spatial(pop_size, startpoint, endpoint, N):
 all_routes = []
 # read land use map dedending on the year
 # iterate to get multiple realizations for the initial population
 for i in range(1,pop_size+1):
     timeGrid= [[random.random() for i in range(N)] for j in range(N)]
     route, weight = route_through_array(timeGrid, startpoint, endpoint, fully_connected=False, geometric=True)
     route= makeArrays(route)
     all_routes.append([i, route])

 #use uniform distribution to select 30% of the cells 
 return all_routes

# maps = initialize_spatial(3, default_directory)
# f, axes = plt.subplots(1,3)
# cmap = ListedColormap(["#10773e","#b3cc33", "#0cf8c1", "#a4507d",
#  "#877712","#be94e8","#eeefce","#1b5ee4",
# "#614040","#00000000"])
# for amap, ax in zip(maps, axes):
#  im = ax.imshow(amap,interpolation='none', cmap=cmap,vmin = 0.5, vmax =
# 10.5)

# plt.colorbar(im, orientation='horizontal')
# plt.show()