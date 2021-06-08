import numpy as np
from pymoo.model.sampling import Sampling
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import initial_population

import yaml

startpoint=(1,10)
endpoint= (99,99)
startTime="15:00"
endTime="18:00"
N = 100

class SpatialSampling(Sampling):
 def __init__(self, var_type=np.float,default_dir=None) -> None:
    super().__init__()
    self.var_type = var_type
    self.default_dir = default_dir
 def _do(self, problem, n_samples, **kwargs):
    landusemaps_np = initial_population.initialize_spatial(n_samples, startpoint, endpoint, N)
    #print(landusemaps_np)
    return landusemaps_np


