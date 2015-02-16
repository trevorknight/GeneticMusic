"""Provides the basic gene classes for the genetic music project
"""

from enum import Enum
from math import round
from random import randint
from random import uniform
from random import normalvariate

__authors__ = 'richardneal and trevorknight'


class MutatorTypes(Enum):
    gaussian = 0
    random = 1


def _clamp(current, lower_bound, upper_bound):
    if upper_bound < lower_bound:
        lower_bound, upper_bound = upper_bound, lower_bound
    return max(lower_bound, min(current, upper_bound))


def _gaussian_mutate(current, lower_bound, upper_bound):
    result = normalvariate(current, (upper_bound - lower_bound) / 4)
    return _clamp(result, lower_bound, upper_bound)


def _gaussian_integer_mutate(current, lower_bound, upper_bound):
    return _clamp(round(_gaussian_mutate(current, lower_bound, upper_bound)))


def _random_mutate(current, lower_bound, upper_bound):
    return uniform(lower_bound, upper_bound)


class Gene:
    def __init__(self, lower_bound, upper_bound):
        if upper_bound < lower_bound:
            lower_bound, upper_bound = upper_bound, lower_bound
        self.data = lower_bound
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.mutator = lambda: self.lower_bound

    def crossover(self):
        pass

    def mutate(self):
        self.data = self.mutator(self.data, self.lower_bound, self.upper_bound)


class DiscreteOrderedGene(Gene):
    def __init__(self, lower_bound, upper_bound, mutator = MutatorTypes.gaussian):
        super(DiscreteOrderedGene, self).__init__(min, max)
        self.data = randint(self.lower_bound, self.upper_bound)
        self.mutator = _gaussian_integer_mutate


class ContinuousGene(Gene):
    def __init__(self, lower_bound, upper_bound, mutator = MutatorTypes.gaussian):
        super(ContinuousGene, self).__init__(lower_bound, upper_bound)
        self.data = uniform(min, max)
        self.mutator = _gaussian_mutate
