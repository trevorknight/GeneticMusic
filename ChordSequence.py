__author__ = 'Trevor Knight'

import music21


class ChordSequence(list):
    def __init__(self):
        self.time_signature = music21.meter.TimeSignature()
        c = music21.chord.Chord(['C3', 'E4', 'G3'])
        e_minor = music21.chord.Chord(['B2', 'E4', 'G3'])
        f = music21.chord.Chord(['C3', 'F3', 'A3'])
        self.sequence = [c, e_minor, f, f]
