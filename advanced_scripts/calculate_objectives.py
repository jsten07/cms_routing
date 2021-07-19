import numpy as np
import pickle
from datetime import datetime, time, timedelta

# Array of fuel cost per hour for the different engine powers [0.6, 0.7, 0.8]
fuelArray=[152*33200, 154*33200, 156*33200]


def calculateTime(route, timeGrids):
    """
    calculate the time needed to go the specific route based on the time grids #

    Parameters
    ----------
    route : array
      one route the ship is going. Containing array of [gridCooridinateX, gridCoordinateY, speed]
    timeGrids : array
      arrays of the time needed for the grid cell, the first dimension are the three different speeds [0.8, 0.7, 0.6]
      the second dimension the direction of the gird [N, S, E, W]. 
      The third and fourt dimension is then the grid for this combination of speed and bearing.
    """
    sumTime = 0
    routeList = makeArrays(route)
    #calculate the bearing for each gird cell
    routeWithBearing = calculateBearing(routeList)

    for x in range(len(routeWithBearing)-1):
      coordinate = routeWithBearing[x]
      speed = coordinate[2]
      speedIndex = 0
      if(speed == 0.8):
        speedIndex = 0
      elif(speed == 0.7):
        speedIndex = 1
      else:
        speedIndex = 2
        
      bearing = coordinate[3]

      #select time grid for specific speed and bearing
      timeGrid =  timeGrids[speedIndex][bearing]
      sumTime = sumTime + timeGrid[coordinate[0]][coordinate[1]]
    hours_added = timedelta(minutes  = sumTime)
    return hours_added

def calculateFuelUse(route, timeGrids):
    """
    calculate the fuel use needed to go the specific route based on the time grids 

    Parameters
    ----------
    route : array
      one route the ship is going. Containing array of [gridCooridinateX, gridCoordinateY, speed]
    timeGrids : array
      arrays of the time needed for the grid cell, the first dimension are the three different speeds [0.8, 0.7, 0.6]
      the second dimension the direction of the gird [N, S, E, W]. 
      The third and fourt dimension is then the grid for this combination of speed and bearing.
    """
    fuelUse = 0
    routeList = makeArrays(route)
    #calculate the bearing for each gird cell
    routeWithBearing = calculateBearing(routeList)
    for x in range(len(routeWithBearing)-1):
      coordinate = routeWithBearing[x]
      speed = coordinate[2]
      speedIndex = 0
      if(speed == 0.8):
        speedIndex = 0
      elif(speed == 0.7):
        speedIndex = 1
      else:
        speedIndex = 2
        

      bearing = coordinate[3]
      #select time grid for specific speed and bearing
      timeGrid = timeGrids[speedIndex][bearing]
      fuelUse = fuelUse + (timeGrid[coordinate[0]][coordinate[1]]/60 * fuelArray[speedIndex])
    return fuelUse

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


def calculateBearing(route):
    """
    calculates the bearing for each grid cell

    Parameters
    ----------
    route : array
      one route the ship is going. Containing array of [gridCooridinateX, gridCoordinateY, speed]
    """
    route
    for i in range(len(route)-1):
        if route[i][0]< route[i+1][0]:
            route[i].append(0) #up
        elif route[i][0] > route[i+1][0]:
            route[i].append(1) # down
        elif route[i][1] < route[i+1][1]:
            route[i].append(2) #right
        elif route[i][1] > route[i+1][1]:
            route[i].append(3) #left
        else:
             route[i].append("error")
    return route


def calculate_time_differences(routes, startTime, endTime, timeGrids):
 """
    functions calculates the time differences depending on the start and end time for each route in the population

    Parameters
    ----------
    routes : array
      array of all routes that are in the population
    startTime : str, day.month.year hours:minutes
      start time of the ship
    endTime : str, day.month.year hours:minutes
      booked port time, the ship shlould arrive
    timeGrids : array
      arrays of the time needed for the grid cell, the first dimension are the three different speeds [0.8, 0.7, 0.6]
      the second dimension the direction of the gird [N, S, E, W]. 
      The third and fourt dimension is then the grid for this combination of speed and bearing.

 """

 timeDif= []
 # loop over the individuals in the population
 for route in routes:
    startTime_object = datetime.strptime(startTime, "%d.%m.%Y %H:%M" )
    endTime_object = datetime.strptime(endTime, "%d.%m.%Y %H:%M" )
    duration = calculateTime(route[1], timeGrids )
    eta = startTime_object + duration
    difference= endTime_object-eta
    total_seconds = difference.total_seconds()
    minutes = total_seconds/60
    timeDif.append(float(minutes) ** 2)
 return(np.array(timeDif))



def calculate_fuelUse(routes,timeGrids):
 """
    functions calculates the fuel use for each route in the population

    Parameters
    ----------
    routes : array
      array of all routes that are in the population
    timeGrids : array
      arrays of the time needed for the grid cell, the first dimension are the three different speeds [0.8, 0.7, 0.6]
      the second dimension the direction of the gird [N, S, E, W]. 
      The third and fourt dimension is then the grid for this combination of speed and bearing.

 """

 # loop over the individuals in the population
 all_fuel = []
 for route in routes:
  fuelUse = calculateFuelUse(route[1], timeGrids)
  fuelUseT = fuelUse/1000000
  all_fuel.append(fuelUseT)

 return(np.array(all_fuel))

def calculate_MinDistance(routes,Grids):
  """
    functions calculates the difference in km for each route in the population

    Parameters
    ----------
    routes : array
      array of all routes that are in the population
    timeGrids : array
      arrays of the time needed for the grid cell, the first dimension are the three different speeds [0.8, 0.7, 0.6]
      the second dimension the direction of the gird [N, S, E, W]. 
      The third and fourt dimension is then the grid for this combination of speed and bearing.

 """
  all_KM = []
  for route in routes:
    sumKM = 0
    routeList = makeArrays(route[1])
    routeWithBearing = calculateBearing(routeList)
    for x in range(len(routeWithBearing)-1):
      coordinate = routeWithBearing[x]
        
      bearing = coordinate[3]

      timeGrid =  Grids[bearing]
      sumKM = sumKM + timeGrid[coordinate[0]][coordinate[1]]
    all_KM.append(sumKM)

  return all_KM

