import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import yaml
from skimage.graph import route_through_array

# array of differnet possible speeds
speeds=[0.8, 0.7, 0.6]

def makeArrays(route):
    """
    the route returned by the muation is a array of tuples. It needs to be an array

    Parameters
    ----------
    route : array
      one route the ship is going. Containing array of [gridCooridinateX, gridCoordinateY, speed]
    """
    routeNew = []
    for x in route:
      routeNew.append(list(x))
    return routeNew



# make initial population for genetic algorithm
def initialize_spatial(pop_size, startpoint, endpoint, timeGrid):
 """
    creates a initial population by making a random configuration of routes

    Parameters
    ----------
    pop_size : int
      the wanted population size
    startpoint: array, [cellX, cellY]
      the startpoint of the route
    endpoint: array, [cellX, cellY]
      the endpoint of the route
    timeGrid: array
      a grid containing the time for one specific context of bearing and speed

 """
 all_routes = []
 #calulate one route with the example time grid
 route, weight = route_through_array(timeGrid, startpoint, endpoint, fully_connected=False, geometric=True)
 route1= makeArrays(route)
 #assing the three different speeds to the route
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


 # finde the middle point of the route
 middle = (startpoint[0] + endpoint[0])/2
 middle2 = (startpoint[1] + endpoint[1])/2

 middlePoint = (middle, middle2)


 


 # create routes for the wanted population size
 for i in range(1,math.floor(pop_size/2)):
     
     #create a time grid with random costs
     timeGridNew= [[random.random() for i in range(timeGrid.shape[1])] for j in range(timeGrid.shape[0])]
     timeGridNew = np.where(timeGrid >999, timeGrid, timeGridNew)
     change= (random.random() *150)
     # set a middle point and move it up and downwoard to create more different routes
     middlePointNew = (math.floor(middlePoint[0] + change), math.floor(middlePoint[1]))
     route1, weight = route_through_array(timeGridNew, startpoint, middlePointNew, fully_connected=False, geometric=True)
     route2, weight = route_through_array(timeGridNew, middlePointNew, endpoint, fully_connected=False, geometric=True)
     route= route1[:-1] + route2
     route= makeArrays(route)
     speed=speeds[math.floor(random.random()*3)]
     # append one speed for the complete route
     for j in range(len(route)):
            route[j].append(speed) 
     all_routes.append([i, route])
     middlePointNew = (math.floor(middlePoint[0] - change), math.floor(middlePoint[1]))
     route1, weight = route_through_array(timeGridNew, startpoint, middlePointNew, fully_connected=False, geometric=True)
     route2, weight = route_through_array(timeGridNew, middlePointNew, endpoint, fully_connected=False, geometric=True)
     route= route1[:-1] + route2
     route= makeArrays(route)
     speed=speeds[math.floor(random.random()*3)]
     # append one speed for the complete route
     for j in range(len(route)):
            route[j].append(speed) 
     all_routes.append([i, route])

 return all_routes
