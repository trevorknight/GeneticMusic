__author__ = 'TrevorKnight'

import MidiOutput
from time import sleep

out = MidiOutput.MidiOutput()
sleep(10)
out.play_note()