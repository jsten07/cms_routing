import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import yaml
from skimage.graph import route_through_array

def makeArrays(route):
    routeNew = []
    for x in route:
      routeNew.append(list(x))
    return routeNew



# make initial population for genetic algorithm
def initialize_spatial(pop_size, startpoint, endpoint, timeGrid):
 all_routes = []
 # read land use map dedending on the year
 # iterate to get multiple realizations for the initial population
 #print(timeGrid.shape[0])
 route, weight = route_through_array(timeGrid, startpoint, endpoint, fully_connected=False, geometric=True)
 route1= makeArrays(route)
 all_routes.append([1, route1])

 middle = (startpoint[0] + endpoint[0])/2
 middle2 = (startpoint[1] + endpoint[1])/2
 print(middle)
 middlePoint = (middle, middle2)
 print(startpoint)
 print(middlePoint)

 



 for i in range(1,math.floor(pop_size/2)+1):
     timeGridNew= [[random.random() for i in range(timeGrid.shape[1])] for j in range(timeGrid.shape[0])]
     timeGridNew = np.where(timeGrid >999, timeGrid, timeGridNew)
     change= (random.random() *150)
     middlePointNew = (math.floor(middlePoint[0] + change), math.floor(middlePoint[1]))
     print(middlePointNew)
     route1, weight = route_through_array(timeGridNew, startpoint, middlePointNew, fully_connected=False, geometric=True)
     route2, weight = route_through_array(timeGridNew, middlePointNew, endpoint, fully_connected=False, geometric=True)
     route= route1[:-1] + route2
     route= makeArrays(route) 
     all_routes.append([i, route])
     middlePointNew = (math.floor(middlePoint[0] - change), math.floor(middlePoint[1]))
     route1, weight = route_through_array(timeGridNew, startpoint, middlePointNew, fully_connected=False, geometric=True)
     route2, weight = route_through_array(timeGridNew, middlePointNew, endpoint, fully_connected=False, geometric=True)
     route= route1[:-1] + route2
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