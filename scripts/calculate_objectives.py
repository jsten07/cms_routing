import numpy as np
import pickle
from datetime import datetime, timedelta


def calculateTime(route, timeGrid):
    #print("single route")
    #print(route)
    sumTime = 0
    for x in route:
      sumTime = sumTime + timeGrid[x[0]][x[1]]
    minutes_added = timedelta(minutes  = sumTime)
    return minutes_added

def makeArrays(route):
    routeNew = []
    for x in route:
      routeNew.append(list(x))
    return routeNew

# calculate the total yield for sugarcane, soy, cotton and pasture
def calculate_time_differences(routes, startTime, endTime, timeGrid):

 timeDif= []
 #print("routes")
 #print(routes)
 # loop over the individuals in the population
 for route in routes:
    startTime_object = datetime.strptime(startTime, "%d.%m.%Y %H:%M" )
    endTime_object = datetime.strptime(endTime, "%d.%m.%Y %H:%M" )
    duration = calculateTime(route[1], timeGrid)
    eta = startTime_object + duration
    difference= endTime_object-eta
    total_seconds = difference.total_seconds()
    minutes = total_seconds/60
    timeDif.append(float(minutes) ** 2)
 #print("timeDif", timeDif)
 return(np.array(timeDif))



def calculate_fuelUse(routes,timeGrid):

 # loop over the individuals in the population
 all_fuel = []
 for route in routes:
  duration = calculateTime(route[1], timeGrid)
  seconds = duration.total_seconds()
  fuelUse = float(seconds) * 100
  all_fuel.append(fuelUse)

 return(np.array(all_fuel))

