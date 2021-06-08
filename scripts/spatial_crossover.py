import numpy as np
from skimage.graph import route_through_array
import random
import math

from pymoo.model.crossover import Crossover

N =100

def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.argmin(dist_2)

def crossover(route1, route2):
  randomNumber = math.floor(random.random()*len(route1))
  crossoverPoint1 = route1[randomNumber]
  index= closest_node(crossoverPoint1, route2)
  crossoverPoint2 = route2[index]
  newGrid= [[random.random() for i in range(N)] for j in range(N)]
  crossoverRoute, weight = route_through_array(newGrid, crossoverPoint1[0:2], crossoverPoint2[0:2], fully_connected=False, geometric=True)
  child1= []
  child2= []
  for i in range(randomNumber):
    child1.append(route1[i])
  for i in range(index):
    child2.append(route2[i])
  for x in crossoverRoute:
    child1.append(x)
  for i in range(len(crossoverRoute) -1, 0, -1):
    child2.append(crossoverRoute[i])
  for i in range(index +1,len(route2)):
    child1.append(route2[i])
  for i in range(randomNumber,len(route1)):
    child2.append(route1[i])
  return[child1, child2, crossoverRoute]


class SpatialOnePointCrossover(Crossover):



 def __init__(self,n_points, **kwargs):
    super().__init__(2, 2, 1.0) # (n_parents,n_offsprings,probability)
    self.n_points = n_points
 def _do(self, problem, X, **kwargs):
    #print(X)
    _, n_matings= X.shape[0],X.shape[1]
    # child land use maps
    child_1 = []
    child_2 = []
    parent1_index = X[0][0][0]
    parent2_index = X[1][0][0]
    parent1 = X[0][0][1]
    parent2 = X[1][0][1]
    #print("parent1",parent1,"parent2", parent2)
    #print(rows)
    #print(protectedArea.shape)
    
    childs=crossover(parent1,parent2)
    child_1= childs[0]
    child_2= childs[1]
        
    return np.array([[parent1_index, list(child_1)], [parent2_index, list(child_2)]])
