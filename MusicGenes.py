"""Provides the basic gene classes for the genetic music project
"""

from copy import deepcopy
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
        return deepcopy(a)
    else:
        return deepcopy(b)


class _Gene:
    def __init__(self, lower_bound, upper_bound):
        if upper_bound < lower_bound:
            lower_bound, upper_bound = upper_bound, lower_bound
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.data = lower_bound
        self.mutator = lambda cur, lower, upper: lower_bound
        self.randomizer = lambda: s = lower_bound

    def randomize(self):
        self.data = self.randomizer()

    def mutate(self):
        self.data = self.mutator(self.data, self.lower_bound, self.upper_bound)


class DiscreteOrderedGene(_Gene):
    def __init__(self, lower_bound, upper_bound, mutator_type=MutatorTypes.gaussian):
        super(DiscreteOrderedGene, self).__init__(lower_bound, upper_bound)
        self.randomizer = lambda: randint(self.lower_bound, self.upper_bound)
        if mutator_type is MutatorTypes.gaussian:
            self.mutator = _gaussian_integer_mutate
        else:
            self.mutator = _random_integer_mutate


class DiscreteUnorderedGene(_Gene):
    def __init__(self, lower_bound, upper_bound):
        super(DiscreteUnorderedGene, self).__init__(lower_bound, upper_bound)
        self.randomizer = lambda: randint(self.lower_bound, self.upper_bound)
        self.mutator = _random_integer_mutate


class ContinuousGene(_Gene):
    def __init__(self, lower_bound, upper_bound, mutator_type=MutatorTypes.gaussian):
        super(ContinuousGene, self).__init__(lower_bound, upper_bound)
        self.randomizer = lambda: uniform(lower_bound, upper_bound)
        if mutator_type is MutatorTypes.gaussian:
            self.mutator = _gaussian_mutate
        else:
            self.mutator = _random_mutate


class Chromosome:
    def __init__(self, genes, mutation_chance=0.05):
        self.Genome = dict(genes)
        self.mutation_chance = mutation_chance
        self.score = 0

    def crossover(self, other):
        assert len(self.Genome) is len(other.Genome)
        assert set(self.Genome.keys()) is set(other.Genome.keys())

        output = deepcopy(other)
        for key in output.Genome.keys():
            output.Genome[key].data = _crossover(output.Genome[key].data, self.Genome[key].data)
            if uniform(0.0, 1.0) > self.mutation_chance:
                output.Genome[key].mutate()

        return output

class Population:
    def __init__(self, chromosome, population_size):
        self.population = []
        for i in range(population_size):
            new_chromosome = deepcopy(chromosome)
            for gene in new_chromosome:
                gene.randomize()
            self.population.append(new_chromosome)
