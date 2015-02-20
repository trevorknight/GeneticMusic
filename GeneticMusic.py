__author__ = 'TrevorKnight'

import MusicGenes
# import MidiOutput
#
# with MidiOutput.MidiOutput() as out:
#     out.play_note()


chromosome = dict()
chromosome['first note'] = MusicGenes.DiscreteOrderedGene(1, 12, MusicGenes.MutatorTypes.random)
chromosome['first velocity'] = MusicGenes.ContinuousGene(0.1, 1.0)

population = MusicGenes.Population(chromosome, 5)

for genotype in population.genotypes:
    for k, v in genotype.items():
        print(k, ' ', v)
    print(genotype.fitness)
