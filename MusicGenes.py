"""Provides the basic gene classes for the genetic music project
"""

from bisect import bisect_left
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

class Population(list):
    def __init__(self, chromosome, population_size, mutation_chance=0.05, carry_over_percent=0.1):
        assert(population_size > 2)
        assert(0.0 <= mutation_chance <= 1.0)
        assert(0.0 <= carry_over_percent <= 1.0)
        self.mutation_chance = mutation_chance
        self.carry_over_number = round(carry_over_percent * population_size)
        assert(self.carry_over_number != population_size)

        for i in range(population_size):
            new_genotype = Genotype()
            for name, gene in chromosome.items():
                new_genotype[name] = gene.get_random_value()
            self.append(new_genotype)

    def create_next_generation(self):
        self.sort(key=lambda genotype: genotype.fitness)
        new_genotypes = list()

        # Carry over
        new_genotypes.extend(self[:self.carry_over_number])

        # Cumulative Probability Distribution
        cumulative_fitness = 0
        cumulative_fitnesses = list()
        for chromosome in self.items():
            cumulative_fitness += chromosome.fitness
            cumulative_fitnesses.append(cumulative_fitness)

        # Generate new genotypes
        for i in range(len(self) - self.carry_over_number):

            # Select for cross-over
            index1 = bisect_left(cumulative_fitnesses, uniform(0, cumulative_fitness))
            index2 = bisect_left(cumulative_fitnesses, uniform(0, cumulative_fitness))
            while index1 is index2:
                index2 = bisect_left(cumulative_fitnesses, uniform(0, cumulative_fitness))

            genotype1 = self[index1]
            genotype2 = self[index2]

            assert len(genotype1) is len(genotype2)
            assert set(genotype1.keys()) is set(genotype2.keys())

            # Generate new genotype
            new_genotype = Genotype()
            for key in genotype1.keys():
                new_genotype[key] = _crossover(genotype1[key], genotype2[key])

            # Save
            new_genotypes.append(new_genotype)