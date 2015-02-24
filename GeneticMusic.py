__author__ = 'TrevorKnight'

import MusicGenes
import music21


# Define Chromosome
def define_chromosome():
    new_chromosome = dict()
    new_chromosome['note1_p'] = MusicGenes.DiscreteOrderedGene(0, 11, MusicGenes.MutatorTypes.random)
    new_chromosome['note1_v'] = MusicGenes.ContinuousGene(0.1, 1.0)
    new_chromosome['note2_p'] = MusicGenes.DiscreteOrderedGene(0, 11, MusicGenes.MutatorTypes.random)
    new_chromosome['note2_v'] = MusicGenes.ContinuousGene(0.1, 1.0)
    new_chromosome['note3_p'] = MusicGenes.DiscreteOrderedGene(0, 11, MusicGenes.MutatorTypes.random)
    new_chromosome['note3_v'] = MusicGenes.ContinuousGene(0.1, 1.0)
    new_chromosome['note4_p'] = MusicGenes.DiscreteOrderedGene(0, 11, MusicGenes.MutatorTypes.random)
    new_chromosome['note4_v'] = MusicGenes.ContinuousGene(0.1, 1.0)
    return new_chromosome

# Create music from genotype
def create_stream(gt: MusicGenes.Genotype):
    s = music21.stream.Stream()
    n = music21.note.Note(gt['note1_p'])
    s.append(n)
    n = music21.note.Note(gt['note2_p'])
    s.append(n)
    n = music21.note.Note(gt['note3_p'])
    s.append(n)
    n = music21.note.Note(gt['note4_p'])
    s.append(n)
    return s

chromosome = define_chromosome()
population = MusicGenes.Population(chromosome, 5)

for genotype in population:
    stream = create_stream(genotype)
    stream.show('musicxml')
