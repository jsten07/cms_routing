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

def mutation(crossover_child, timeGrid):
    crossover_child_split_list= []
    
    crossover_child = makeArrays(crossover_child)
    #split crossover over child into 3 lists
    crossover_child_split_nparray = np.array_split(crossover_child, 3)
    for numpy_array in crossover_child_split_nparray:
        crossover_child_split_list.append(numpy_array)
   
    startpoint = crossover_child_split_list[0][-1]
    endpoint = crossover_child_split_list[2][0]
    # recalculate route from end point of list 1 to sarting point of list 3
    route, weight = route_through_array(timeGrid, startpoint, endpoint, 
                                        fully_connected=False, geometric=True)
    route_list = makeArrays(route)
    first_component = makeArrays(crossover_child_split_list[0])
    second_component = route_list[1:-1]#filter out starting point and endpoint from the new mid list
    third_component = makeArrays(crossover_child_split_list[2])
    #combine all the sections to a final mutated route
    mutated_child = first_component + second_component + third_component 
    
    return mutated_child

  
# class that performs the mutation
class SpatialNPointMutation(Mutation):
    def __init__(self, prob=None,point_mutation_probability=0.01):
        super().__init__()
        self.prob = prob
        self.point_mutation_probability = point_mutation_probability
        self.TimeGrid= [[random.random() for i in range(100)] for j in range(100)]
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