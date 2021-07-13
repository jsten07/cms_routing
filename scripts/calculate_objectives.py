import numpy as np
import pickle
from datetime import datetime, timedelta

def makeArrays(route):
    routeNew = []
    for x in route:
      routeNew.append(list(x))
    return routeNew


def calculateBearing(route):
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
    
def calculateTime(route, timeGrids):
    #print("single route")
    #print(route)
    sumTime = 0
    routeList = makeArrays(route)
    routeWithBearing = calculateBearing(routeList)
    for x in range(len(routeWithBearing)-1):
      coordinate = routeWithBearing[x]
      #print(coordinate)
      bearing = coordinate[2]
      #print(speedIndex, bearing)
      #print(coordinate)
      #array = np.array(timeGrids[speedIndex][bearing])
      #print(array.shape)
      timeGrid =  timeGrids[bearing]
      sumTime = sumTime + timeGrid[coordinate[0]][coordinate[1]]
    hours_added = timedelta(minutes  = sumTime)
    return hours_added

def calculateFuelUse(route, timeGrids):
    #print("single route")
    #print(route)
    fuelUse = 0
    routeList = makeArrays(route)
    routeWithBearing = calculateBearing(routeList)
    #print("timeGrid", timeGrids[0][10][10])
    for x in range(len(routeWithBearing)-1):
      coordinate = routeWithBearing[x]
        
      #print(timeGrids[speedIndex][bearing])
      #print(coordinate)
      bearing = coordinate[2]
      timeGrid = timeGrids[bearing]
      fuelUse = fuelUse + (timeGrid[coordinate[0]][coordinate[1]]/60 * 154*33200)
    return fuelUse

def makeArrays(route):
    routeNew = []
    for x in route:
      routeNew.append(list(x))
    return routeNew

# calculate the total yield for sugarcane, soy, cotton and pasture
def calculate_time_differences(routes, startTime, endTime, timeGrids):

 timeDif= []
 #print("routes")
 #print(routes)
 # loop over the individuals in the population
 for route in routes:
    startTime_object = datetime.strptime(startTime, "%d.%m.%Y %H:%M" )
    endTime_object = datetime.strptime(endTime, "%d.%m.%Y %H:%M" )
    duration = calculateTime(route[1], timeGrids)
    eta = startTime_object + duration
    difference= endTime_object-eta
    total_seconds = difference.total_seconds()
    minutes = total_seconds/60
    timeDif.append(float(minutes) ** 2)
 #print("timeDif", timeDif)
 return(np.array(timeDif))



def calculate_fuelUse(routes,timeGrids):

 # loop over the individuals in the population
 all_fuel = []
 for route in routes:
  fuelUse = calculateFuelUse(route[1], timeGrids)
  fuelUseT = fuelUse/1000000
  all_fuel.append(fuelUseT)

 return(np.array(all_fuel))

def calculate_MinDistance(routes,Grids):

  all_KM = []
  for route in routes:
    #print("single route")
    #print(route)
    sumKM = 0
    routeList = makeArrays(route[1])
    routeWithBearing = calculateBearing(routeList)
    for x in range(len(routeWithBearing)-1):
      coordinate = routeWithBearing[x]
    #print("timeGrid", timeGrids[0][10][10])
        
      bearing = coordinate[3]

      #print(speedIndex, bearing)
      #print(coordinate)
      #array = np.array(timeGrids[speedIndex][bearing])
      #print(array.shape)
      timeGrid =  Grids[bearing]
      sumKM = sumKM + timeGrid[coordinate[0]][coordinate[1]]
    all_KM.append(sumKM)

  return all_KM

