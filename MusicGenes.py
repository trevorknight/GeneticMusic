"""Provides the basic gene classes for the genetic music project
"""

from enum import Enum
from random import randint
from random import uniform
from random import normalvariate

__authors__ = 'Richard Neal and Trevor Knight'


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


def _random_integer_mutate(current, lower_bound, upper_bound):
    return randint(lower_bound, upper_bound)


def _crossover(a, b):
    if randint(0, 1):
        return a
    else:
        return b


class _Gene:
    def __init__(self, lower_bound, upper_bound):
        if upper_bound < lower_bound:
            lower_bound, upper_bound = upper_bound, lower_bound
        self.data = lower_bound
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.mutator = lambda: self.lower_bound

    def crossover(self, other_gene):
        self.data = _crossover(self.data, other_gene.data)

    def mutate(self):
        self.data = self.mutator(self.data, self.lower_bound, self.upper_bound)


class DiscreteOrderedGene(_Gene):
    def __init__(self, lower_bound, upper_bound, mutator_type=MutatorTypes.gaussian):
        super(DiscreteOrderedGene, self).__init__(lower_bound, upper_bound)
        self.data = randint(self.lower_bound, self.upper_bound)
        if mutator_type is MutatorTypes.gaussian:
            self.mutator = _gaussian_integer_mutate
        else:
            self.mutator = _random_integer_mutate


class DiscreteUnorderedGene(_Gene):
    def __init__(self, lower_bound, upper_bound):
        super(DiscreteUnorderedGene, self).__init__(lower_bound, upper_bound)
        self.data = randint(self.lower_bound, self.upper_bound)
        self.mutator = _random_integer_mutate


class ContinuousGene(_Gene):
    def __init__(self, lower_bound, upper_bound, mutator_type=MutatorTypes.gaussian):
        super(ContinuousGene, self).__init__(lower_bound, upper_bound)
        self.data = uniform(lower_bound, upper_bound)
        if mutator_type is MutatorTypes.gaussian:
            self.mutator = _gaussian_mutate
        else:
            self.mutator = _random_mutate


class Chromosome:
    def __init__(self, genes):
        self.Genome = dict(genes)

    def crossover(self, other):
        output = Chromosome()
        combination = zip(self.Genome, other.Genome)
