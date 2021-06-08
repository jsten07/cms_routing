import numpy as np
from pymoo.model.mutation import Mutation
import random
import math
from skimage.graph import route_through_array

def makeArrays(route):
    routeNew = []
    for x in route:
      routeNew.append(list(x))
    return routeNew

N=100

# function to randomly change a certain patch
def mutation(route):
  #print(route)
  randomNumber = random.random()*len(route)
  startIndex= math.floor(randomNumber)
  startpoint = route[startIndex]
  endIndex= math.floor(startIndex + (random.random() * (len(route)-startIndex)))
  endpoint= route[endIndex]
  newGrid= [[random.random() for i in range(N)] for j in range(N)]
  manipulateRoute, weight = route_through_array(newGrid, startpoint[0:2], endpoint[0:2], fully_connected=False, geometric=True)
  manipulateRoute = makeArrays(manipulateRoute)
  manipulatedRoute = []
  for i in range(startIndex):
            manipulatedRoute.append(route[i])
  for x in manipulateRoute:
    manipulatedRoute.append(x)
  for i in range((endIndex+1),len(route)):
            manipulatedRoute.append(route[i])
  return manipulatedRoute
# class that performs the mutation
class SpatialNPointMutation(Mutation):
    def __init__(self, prob=None,point_mutation_probability=0.01):
        super().__init__()
        self.prob = prob
        self.point_mutation_probability = point_mutation_probability
    def _do(self, problem, X, **kwargs):
        offspring=[]
        #print(X)

        # loop over individuals in population
        for i in X:
            # performe mutation with certain probability
            if np.random.uniform(0, 1) < self.prob:
                mutated_individual = mutation(i[1])
                offspring.append([i[0], mutated_individual])
        # if no mutation
            else:
                offspring.append([i[0], i])
        offspring = np.array(offspring)
        return offspring