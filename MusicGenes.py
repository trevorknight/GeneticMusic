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
        self.mutator = lambda cur, lower, upper: lower_bound
        self.randomizer = lambda: lower_bound

    def get_random_value(self):
        return self.randomizer()

    def get_mutated_value(self, current):
        return self.mutator(current, self.lower_bound, self.upper_bound)


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


class Genotype(dict):
    def __init__(self):
        self.fitness = 0


class Population:
    def __init__(self, chromosome, population_size, mutation_chance=0.05, crossover_chance=0.5, carry_over_percent=0.1):
        self.genotypes = []
        self.size = population_size
        self.carry_over_number = round(carry_over_percent * self.size)
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance
        for i in range(self.size):
            new_genotype = Genotype()
            for name, gene in chromosome.items():
                new_genotype[name] = gene.get_random_value()
            self.genotypes.append(new_genotype)

    def create_next_generation(self):
        self.genotypes.sort(key=lambda genotype: genotype.fitness)
        new_genotypes = []
        # More stuff here
    # def crossover(a, b):
    #     assert len(self.Genome) is len(other.Genome)
    #     assert set(self.Genome.keys()) is set(other.Genome.keys())
    #
    #     output = deepcopy(other)
    #     for key in output.Genome.keys():
    #         output.Genome[key].data = _crossover(output.Genome[key].data, self.Genome[key].data)
    #         if uniform(0.0, 1.0) > self.mutation_chance:
    #             output.Genome[key].mutate()
    #
    #     return output