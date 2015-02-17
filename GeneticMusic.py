__author__ = 'TrevorKnight'

import MidiOutput

with MidiOutput.MidiOutput() as out:
    out.play_note()

