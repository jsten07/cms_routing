import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import yaml
from skimage.graph import route_through_array

speeds=[0.8, 0.7, 0.6]

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
 for i in range(len(route)):
            route1[i].append(speeds[0]) 
 route2= makeArrays(route)
 for i in range(len(route)):
            route2[i].append(speeds[1]) 
 route3= makeArrays(route)
 for i in range(len(route)):
            route3[i].append(speeds[2]) 

 all_routes.append([1, route1])
 all_routes.append([2, route2])
 all_routes.append([3, route3])

 middle = (startpoint[0] + endpoint[0])/2
 middle2 = (startpoint[1] + endpoint[1])/2
 #print(middle)
 middlePoint = (middle, middle2)
 #print(startpoint)
 #print(middlePoint)

 



 for i in range(1,math.floor(pop_size/2)):
     timeGridNew= [[random.random() for i in range(timeGrid.shape[1])] for j in range(timeGrid.shape[0])]
     timeGridNew = np.where(timeGrid >999, timeGrid, timeGridNew)
     change= (random.random() *150)
     middlePointNew = (math.floor(middlePoint[0] + change), math.floor(middlePoint[1]))
     #print(middlePointNew)
     route1, weight = route_through_array(timeGridNew, startpoint, middlePointNew, fully_connected=False, geometric=True)
     route2, weight = route_through_array(timeGridNew, middlePointNew, endpoint, fully_connected=False, geometric=True)
     route= route1[:-1] + route2
     route= makeArrays(route)
     speed=speeds[math.floor(random.random()*3)]
     for j in range(len(route)):
            route[j].append(speed) 
     all_routes.append([i, route])
     middlePointNew = (math.floor(middlePoint[0] - change), math.floor(middlePoint[1]))
     route1, weight = route_through_array(timeGridNew, startpoint, middlePointNew, fully_connected=False, geometric=True)
     route2, weight = route_through_array(timeGridNew, middlePointNew, endpoint, fully_connected=False, geometric=True)
     route= route1[:-1] + route2
     route= makeArrays(route)
     speed=speeds[math.floor(random.random()*3)]
     for j in range(len(route)):
            route[j].append(speed) 
     all_routes.append([i, route])

 return all_routes
