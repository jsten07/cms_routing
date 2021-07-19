import numpy as np
from pymoo.model.mutation import Mutation
import random
import math
from skimage.graph import route_through_array

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



# function to randomly change a certain patch

def mutation(crossover_child, timeGrid):
    """
    mutates one route, so changes a random part of it

    Parameters
    ----------
    crossover_child : array
      one route the ship is going, returned by the crossover
    """
    timeGridNew= [[random.random() for i in range(timeGrid.shape[1])] for j in range(timeGrid.shape[0])]
    timeGridNew = np.where(timeGrid >999, timeGrid, timeGridNew)
    crossover_child_split_list= []
    
    crossover_child = makeArrays(crossover_child)
    #split crossover over child into 3 lists
    randomNumber = random.random()*len(crossover_child)
    startIndex= math.floor(randomNumber)
    startpoint = crossover_child[startIndex]
    endIndex= math.floor(startIndex + (random.random() * (len(crossover_child)-startIndex)))
    endpoint= crossover_child[endIndex]

    # recalculate route from end point of list 1 to sarting point of list 3
    route, weight = route_through_array(timeGridNew, startpoint[0:2], endpoint[0:2], 
                                        fully_connected=False, geometric=True)
    route_list = makeArrays(route)
    speed= speeds[math.floor(random.random()*3)]
    for j in range(len(route_list)):
      route_list[j].append(speed) 
    first_component = makeArrays(crossover_child[0:startIndex])
    second_component = route_list[0:-1]#filter out starting point and endpoint from the new mid list
    third_component = makeArrays(crossover_child[endIndex:len(crossover_child)])
    #combine all the sections to a final mutated route
    mutated_child = first_component + second_component + third_component 
    #print(mutated_child)
    
    return mutated_child

  
# class that performs the mutation
class SpatialNPointMutation(Mutation):
    def __init__(self, timeGrid, prob=None,point_mutation_probability=0.01):
        super().__init__()
        self.prob = prob
        self.point_mutation_probability = point_mutation_probability
        self.TimeGrid= timeGrid
    def _do(self, problem, X, **kwargs):
        offspring=[]
        #print(X)

        # loop over individuals in population
        for i in X:
            # performe mutation with certain probability
            if np.random.uniform(0, 1) < self.prob:
                mutated_individual = mutation(i[1], self.TimeGrid)
                offspring.append([i[0], mutated_individual])
        # if no mutation
            else:
                offspring.append([i[0], i])
        offspring = np.array(offspring)
        return offspring