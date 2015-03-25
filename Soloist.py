__author__ = 'Trevor Knight'

import music21
import MusicGenes as mG
import ChordSequence

class Soloist:
    def __init__(self, chord_sequence: ChordSequence):
        self._chord_sequence = chord_sequence
        self._chromosome = dict()
        self._chromosome["downbeat note"] = mG.SetOfWeightedPossibilitiesGene([0, 3, 5])

    def get_chromosome(self):
        return self._chromosome

    def create_score(self, genotype):
        s = music21.stream.Stream()
        chords_part = music21.stream.Part()
        s.append(chords_part)


        return s



