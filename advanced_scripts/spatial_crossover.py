import numpy as np
from skimage.graph import route_through_array
import random
import math

from pymoo.model.crossover import Crossover



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


def closest_node(node, nodes):
    """
    find the closest point to this point

    Parameters
    ----------
    node : array
      one point where the nearest should be found
    nodes : array of node
      points where the nearest should be found from
    """
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.argmin(dist_2)

def findDuplicate(node, nodes, index):
    """
    proof if the ship goes through one point twice

    Parameters
    ----------
    node : array
      one point which should be proofed
    nodes : array of node
      points which should be compared with node
    index : int
      number where to start in nodes
    """
    nodes= nodes[index: len(nodes)]
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.where(dist_2 == 0)

def eleminateDuplicates(start, route):
    """
    eleminate points, where the ship goes through twice

    Parameters
    ----------
    start : int
      index where to start on the route 
    route : array 
      route which shcould be proofed on duplicates
    """
    for i in range(start, len(route)):
      duplicate=findDuplicate(route[i], route, i)
      duplicate=duplicate[0]
      if len(duplicate) > 1:
        newRoute=route[:i] + route[i+duplicate[1]:]
        return eleminateDuplicates(i, newRoute)
    return route

def crossover(route1, route2, timeGrid):
  """
    combines two routes of the population to two new routes

    Parameters
    ----------
    route1 : array
      first route which should be used
    route2 : array
      second route which schould be used
    timeGrid: array
      a grid containing the time for one specific context of bearing and speed
    """
  timeGridNew= [[random.random() for i in range(timeGrid.shape[1])] for j in range(timeGrid.shape[0])]
  timeGridNew = np.where(timeGrid >999, timeGrid, timeGridNew)

  index1 = math.floor(random.random()*min(len(route1), len(route2)))
  index2 = min(len(route2) -1, len(route1)-1, (index1 + math.floor(random.random()*(len(route1) -index1)+ 10)))

  crossoverPoint1 = route1[index1]

  crossoverPoint2 = route2[index2]
  
  
  crossoverRoute1, weight = route_through_array(timeGridNew, crossoverPoint1[0:2], crossoverPoint2[0:2], fully_connected=False, geometric=True)
  crossoverRoute1= makeArrays(crossoverRoute1)


  crossoverPoint1 = route2[index1]
  #index= closest_node(crossoverPoint1, route2)

  crossoverPoint2 = route1[index2]
  crossoverRoute2, weight = route_through_array(timeGridNew, crossoverPoint1[0:2], crossoverPoint2[0:2], fully_connected=False, geometric=True)
  crossoverRoute2= makeArrays(crossoverRoute2)

  speed= speeds[math.floor(random.random()*3)]
  for j in range(len(crossoverRoute1)):
      crossoverRoute1[j].append(speed) 

  for i in range(len(crossoverRoute2)):
      crossoverRoute2[i].append(speed) 
      
  child1= []
  child2= []
  for i in range(index1-1):
    child1.append(route1[i])
    child2.append(route2[i])
  for x in crossoverRoute1:
    child1.append(x)
  for x in crossoverRoute2:
    child2.append(x)
  for i in range(index2 +1,len(route2)):
    child1.append(route2[i])
  for i in range(index2 +1,len(route1)):
    child2.append(route1[i])
  return[child1, child2, crossoverRoute1]


class SpatialOnePointCrossover(Crossover):
 """
    class to conduct the crossover

"""



 def __init__(self, timeGrid, n_points, **kwargs):
    super().__init__(2, 2, 1.0) # (n_parents,n_offsprings,probability)
    self.n_points = n_points
    self.TimeGrid = timeGrid
 def _do(self, problem, X, **kwargs):

    _, n_matings= X.shape[0],X.shape[1]

    child_1 = []
    child_2 = []
    parent1_index = X[0][0][0]
    parent2_index = X[1][0][0]
    parent1 = X[0][0][1]
    parent2 = X[1][0][1]

    
    childs=crossover(parent1,parent2, self.TimeGrid)
    child_1= eleminateDuplicates(0, childs[0])
    child_2= eleminateDuplicates(0, childs[1]) 
        
    return np.array([[parent1_index, list(childs[0])], [parent2_index, list(childs[1])]])