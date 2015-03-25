__author__ = 'Trevor Knight'

import music21
import MusicGenes as mg
import ChordSequence

class Soloist:
    def __init__(self):
        self.chromosome = dict()
        self.chromosome["phrase_length"] = mg.DiscreteUnorderedGene(1, 8)
        self.chromosome["downbeat note"] = mg.SetOfWeightedPossibilitiesGene([0, 3, 5])

    def CreateScore(self, chord_sequence: ChordSequence):
        s = music21.Score.score()
        for chord in chord_sequence.sequence:
            pass
        return s



