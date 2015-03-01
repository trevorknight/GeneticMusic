__author__ = 'Trevor Knight'

import MusicGenes
from bisect import bisect_left
from random import randint
from random import uniform
from music21 import *


scale = [0, 2, 4, 5, 7, 9, 11]
subdivisions = [1, 2, 3]


def define_chromosome():
    nc = dict()
    nc["P1"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P2"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P3"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P4"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P5"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P6"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P7"] = MusicGenes.DiscreteOrderedGene(0, 100)

    nc["POneQuarter"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["PTwoEighths"] = MusicGenes.ContinuousGene(0, 100)
    nc["PTriplet"] = MusicGenes.ContinuousGene(0, 100)

    return nc

def _create_major_chord(s, root, offset):
    n1 = note.Note(root)
    n1.quarterLength = 4
    n2 = note.Note(root + 4)
    n2.quarterLength = 4
    n3 = note.Note(root + 7)
    n3.quarterLength = 4
    s.insert(offset + 0, n1)
    s.insert(offset + 0, n2)
    s.insert(offset + 0, n3)


def _translate_note(root, offset):
    return root + scale[offset]


def render_music(genotype):
    scale_weights = [genotype["P1"],
                     genotype["P2"],
                     genotype["P3"],
                     genotype["P4"],
                     genotype["P5"],
                     genotype["P6"],
                     genotype["P7"]]
    cumulative_scale_weights = list()
    total_scale_weight = 0
    for weight in scale_weights:
        total_scale_weight += weight
        cumulative_scale_weights.append(total_scale_weight)

    subdivide_weights = [genotype["POneQuarter"],
                         genotype["PTwoEights"],
                         genotype["PTriplets"]]
    cumulative_subdivide_weights = list()
    total_subdivide_weight = 0
    for weight in subdivide_weights:
        total_subdivide_weight += weight
        cumulative_subdivide_weights.append(weight)

    s = stream.Stream()
    for measure in range(0, 4):
        root = 60
        if measure % 2 == 1:
            root = 67
        _create_major_chord(s, root, 4 * measure)
        for beat in range(0, 4):

            rand_on_range = randint(0, total_subdivide_weight)
            index_of_chosen = bisect_left(cumulative_subdivide_weights, rand_on_range)
            number_notes = subdivisions[index_of_chosen]

            for note in range(0, number_notes):
                rand_on_range = randint(0, total_scale_weight)
                index_of_chosen = bisect_left(cumulative_scale_weights, rand_on_range)
                pitch = _translate_note(root, index_of_chosen)


    return s