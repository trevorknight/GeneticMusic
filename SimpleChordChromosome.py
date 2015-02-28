__author__ = 'Trevor Knight'

import MusicGenes
from bisect import bisect_left
from random import randint
from random import uniform
from music21 import *

def define_chromosome():
    nc = dict()
    nc["P1"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P2"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P3"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P4"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["P5"] = MusicGenes.DiscreteOrderedGene(0, 100)
    nc["PSubdivide"] = MusicGenes.ContinuousGene(0.0, 1.0)
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
    chord_tones = [0, 2, 4, 5, 7, 9, 11]
    return root + chord_tones[offset]

def render_music(genotype):
    probabilities = [genotype["P1"],\
                     genotype["P2"],\
                     genotype["P3"],\
                     genotype["P4"],\
                     genotype["P5"]]
    cumulative_probabilities = list()
    total_probability = 0
    for prob in probabilities:
        total_probability += prob
        cumulative_probabilities.append(total_probability)

    s = stream.Stream()
    for measure in range(0, 4):
        root = 60
        if measure % 2 == 1:
            root = 67
        _create_major_chord(s, root, 4 * measure)
        for beat in range(0, 4):
            rand_on_range = randint(0, total_probability)
            index_of_chosen = bisect_left(cumulative_probabilities, rand_on_range)
            current_note = _translate_note(root, index_of_chosen)

            subdivide = uniform(0.0, 1.0) > genotype["PSubdivide"]

            if subdivide:
                rand_on_range = randint(0, total_probability)
                index_of_chosen = bisect_left(probabilities, rand_on_range)
                subdivide_note = _translate_note(root, index_of_chosen)
                note1 = note.Note(current_note)
                note1.quarterLength = 0.5
                note2 = note.Note(subdivide_note)
                note2.quarterLength = 0.5
                s.insert(4 * measure + beat, note1)
                s.insert(4 * measure + beat + 0.5, note2)
            else:
                note1 = note.Note(current_note)
                note1.quarterLength = 1
                s.insert(4 + measure + beat, note1)
    return s