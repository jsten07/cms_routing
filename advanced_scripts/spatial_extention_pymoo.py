
def _new_get_sampling_options():
    from pymoo.operators.sampling.latin_hypercube_sampling import LatinHypercubeSampling
    from pymoo.operators.sampling.random_sampling import FloatRandomSampling
    from pymoo.operators.integer_from_float_operator import IntegerFromFloatSampling
    from pymoo.operators.sampling.random_sampling import BinaryRandomSampling
    from pymoo.operators.sampling.random_permutation_sampling import PermutationRandomSampling
    from spatial_sampling import SpatialSampling

    SAMPLING = [
        ("real_random", FloatRandomSampling),
        ("real_lhs", LatinHypercubeSampling),
        ("bin_random", BinaryRandomSampling),
        ("int_random", IntegerFromFloatSampling, {'clazz': FloatRandomSampling}),
        ("int_lhs", IntegerFromFloatSampling, {'clazz': LatinHypercubeSampling}),
        ("perm_random", PermutationRandomSampling, dict(default_dir = None)),
        ("spatial", SpatialSampling)
    ]

    return SAMPLING

def _new_get_crossover_options():
        from pymoo.operators.crossover.differental_evolution_crossover import DifferentialEvolutionCrossover
        from pymoo.operators.crossover.exponential_crossover import ExponentialCrossover
        from pymoo.operators.crossover.half_uniform_crossover import HalfUniformCrossover
        from pymoo.operators.crossover.point_crossover import PointCrossover
        from pymoo.operators.crossover.simulated_binary_crossover import SimulatedBinaryCrossover
        from pymoo.operators.crossover.uniform_crossover import UniformCrossover
        from pymoo.operators.integer_from_float_operator import IntegerFromFloatCrossover
        from pymoo.operators.crossover.edge_recombination_crossover import EdgeRecombinationCrossover
        from pymoo.operators.crossover.order_crossover import OrderCrossover
        from spatial_crossover import SpatialOnePointCrossover
        #from spatial_crossover_constrained import SpatialOnePointCrossover
        CROSSOVER = [
            ("real_sbx", SimulatedBinaryCrossover, dict(prob=0.9, eta=30)),
            ("int_sbx", IntegerFromFloatCrossover, dict(clazz=SimulatedBinaryCrossover, prob=0.9, eta=30)),
            ("real_de", DifferentialEvolutionCrossover),
            ("(real|bin|int)_ux", UniformCrossover),
            ("(bin|int)_hux", HalfUniformCrossover),
            ("(real|bin|int)_exp", ExponentialCrossover),
            ("(real|bin|int)_one_point", PointCrossover, {'n_points': 1}),
            ("(real|bin|int)_two_point", PointCrossover, {'n_points': 2}),
            ("(real|bin|int)_k_point", PointCrossover),
            ("perm_ox", OrderCrossover),
            ("perm_erx", EdgeRecombinationCrossover),
            ("spatial_one_point_crossover", SpatialOnePointCrossover)
        ]
        return CROSSOVER

def _new_get_mutation_options():
    from pymoo.operators.mutation.no_mutation import NoMutation
    from pymoo.operators.mutation.bitflip_mutation import BinaryBitflipMutation
    from pymoo.operators.mutation.polynomial_mutation import PolynomialMutation
    from pymoo.operators.integer_from_float_operator import IntegerFromFloatMutation
    from pymoo.operators.mutation.inversion_mutation import InversionMutation
    from spatial_mutation import SpatialNPointMutation

    MUTATION = [
        ("none", NoMutation, {}),
        ("real_pm", PolynomialMutation, dict(eta=20)),
        ("int_pm", IntegerFromFloatMutation, dict(clazz=PolynomialMutation, eta=20)),
        ("bin_bitflip", BinaryBitflipMutation),
        ("perm_inv", InversionMutation),
        ("spatial_n_point_mutation", SpatialNPointMutation, dict(point_mutation_probability = 0.01))
    ]

    return MUTATION

import numpy as np
from pymoo.model.population import Population

offspring=2

def _new_crossover_do(self, problem, pop, parents, **kwargs):
        """

        This method executes the crossover on the parents. This class wraps the implementation of the class
        that implements the crossover.

        Parameters
        ----------
        problem: class
            The problem to be solved. Provides information such as lower and upper bounds or feasibility
            conditions for custom crossovers.

        pop : Population
            The population as an object

        parents: numpy.array
            The select parents of the population for the crossover

        kwargs : dict
            Any additional data that might be necessary to perform the crossover. E.g. constants of an algorithm.

        Returns
        -------
        offsprings : Population
            The off as a matrix. n_children rows and the number of columns is equal to the variable
            length of the problem.

        """

        if self.n_parents != parents.shape[1]:
            raise ValueError('Exception during crossover: Number of parents differs from defined at crossover.')

        # get the design space matrix form the population and parents
        X = pop.get("X")[parents.T].copy()

        # now apply the crossover probability
        do_crossover = np.random.random(len(parents)) < self.prob

        # execute the crossover
        _X = self._do(problem, X, **kwargs)

        X = _X

        off = Population.new("X", X)

        return off
