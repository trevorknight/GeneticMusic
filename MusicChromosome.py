__author__ = 'richardneal'
from random import randint
from random import uniform


class Gene:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def crossover(self):
        pass

    def mutate(self):
        pass

    def _clamp(self):
        self.data = max(min(self.data, self.max), self.min)


class DiscreteOrderedGene(Gene):
    def __init__(self, min, max):
        super(DiscreteOrderedGene, self).__init__(min, max)
        self.data = randint(min, max)

    def mutate(self):
        self.data += 1


class ContinuousGene(Gene):
    def __init__(self, min, max):
        super(ContinuousGene, self).__init__(min, max)
        self.data = uniform(min, max)

    def mutate(self):
        mutation_range = (max - min)*0.05
        mutation_value = uniform(-mutation_range, mutation_range)
        self.data += mutation_value


class Beat():
    def __init__(self):
        self.pitch = DiscreteOrderedGene(1, 12)
        self.velocity = DiscreteOrderedGene(0.5, 1.0)


class Chromosome:
    def __init__(self):
        self.data = [Beat()]*16

