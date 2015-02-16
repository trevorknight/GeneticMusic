__author__ = 'TrevorKnight'

import MidiOutput
from time import sleep

with MidiOutput.MidiOutput() as out:
    out.play_note()

