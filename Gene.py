__author__ = 'richardneal'
import random

class Gene:
    # def __new__(cls, *args):
    #     if type(args[0]) is type(int):
    #         instance = ContinuousGene

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def crossover(self):
        pass

    def mutate(self):
        pass

    def _clamp(self):
        self.data = max(min(self.data, self.max), self.min)

class Beat(Gene):

# class Mutator:
#     def seed(self):
#         pass
#
#     def mutate(self):
#         pass

class DiscreteOrderedGene(Gene):
    def __init__(self, min, max):
        super(DiscreteOrderedGene, self).__init__(min, max)
        self.data = random.randint(min, max)

    def mutate(self):
        self.data += 1

class ContinuousGene(Gene):
    def __init__(self, min, max):
        super(ContinuousGene, self).__init__(min, max)
        self.data = random.uniform(min, max)

    def mutate(self):
        mutation_range = (max - min)*0.05
        mutation_value = random.uniform(-mutation_range, mutation_range)
        self.data += mutation_value


class Chromosome:
    def __init__(self):
        self.data = [Beat()]*16

class Pitch(DiscreteOrderedGene):

class Velocity(Gene, ContinuousMutation):

class Duration(Gene, DiscreteOrderedMutation):

