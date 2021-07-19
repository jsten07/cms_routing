from pymoo import factory
from pymoo.model.crossover import Crossover
import spatial_extention_pymoo
# add spatial functions to pymoo library
factory.get_sampling_options = spatial_extention_pymoo._new_get_sampling_options
factory.get_crossover_options = spatial_extention_pymoo._new_get_crossover_options
factory.get_mutation_options = spatial_extention_pymoo._new_get_mutation_options
Crossover.do = spatial_extention_pymoo._new_crossover_do

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pymoo.util.misc import stack
from pymoo.model.problem import Problem

from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.factory import get_termination
from pymoo.optimize import minimize
from pymoo.model.problem import Problem


from pymoo.optimize import minimize

from calculate_objectives import calculate_time_differences 
from calculate_objectives import calculate_fuelUse
from calculate_objectives import calculate_MinDistance


import random


def runAlgorithm(startpoint, endpoint, startTime, endTime, timeGrids, population, offspring, generations ):
 """
    run the algorithm and return the result as a pymoo result object https://pymoo.org/interface/result.html

    Parameters
    ----------
    startpoint: array, [cellX, cellY]
      the startpoint of the route
    endpoint: array, [cellX, cellY]
      the endpoint of the route
    startTime: str, day.month.year hours:minutes
      start time of the ship
    endTime: str, day.month.year hours:minutes
      booked port time, the ship shlould arrive
    population: int
      the wanted population, number of routes that will be returned
    offspirng: int
      number of new routes calculated with each iteration
    generations: int
      number of iterations
 """
 timeGrid=timeGrids[0]
    
 class MyProblem(Problem):

    # define the number of variables etc.
    def __init__(self):
        super().__init__(n_var=2, # nr of variables
                        n_obj=2, # nr of objectives
                        n_constr=0, # nr of constraints
                        xl=0.0, # lower boundaries
                        xu=1.0) # upper boundaries

                        # define the objective functions
    def _evaluate(self, X, out, *args, **kwargs):
        f1 = calculate_time_differences(X[:], startTime, endTime, timeGrids)
        f2 = calculate_fuelUse(X[:], timeGrids)
        out["F"] = np.column_stack([f1, f2])

 problem = MyProblem()
 print(problem)
  # load own sampling, crossover and mutation method
 algorithm = NSGA2(
    pop_size=population,
    n_offsprings= offspring,
    sampling=get_sampling("spatial", startpoint= startpoint, endpoint=endpoint, timeGrid = timeGrid),
    crossover=get_crossover("spatial_one_point_crossover", timeGrid = timeGrid, n_points = 1.0),
    mutation=get_mutation("spatial_n_point_mutation", timeGrid=timeGrid, prob = 1.0),
    eliminate_duplicates=False
 )
 termination = get_termination("n_gen", generations)

 # run algorithm itself
 res = minimize(problem,
               algorithm,
               termination,
               seed=1, 
               save_history=True,   
               verbose=True)
               
 return(res)
