import numpy as np
from pymoo.model.sampling import Sampling
import initial_population

import yaml


class SpatialSampling(Sampling):
 def __init__(self, startpoint, endpoint, timeGrid, var_type=np.float, default_dir=None) -> None:
    super().__init__()
    self.var_type = var_type
    self.default_dir = default_dir
    self.startpoint = startpoint
    self.endpoint = endpoint
    self.timeGrid = timeGrid
 def _do(self, problem, n_samples, **kwargs):
    landusemaps_np = initial_population.initialize_spatial(n_samples, self.startpoint, self.endpoint, self.timeGrid)
    #print(landusemaps_np)
    return landusemaps_np


