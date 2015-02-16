__author__ = 'TrevorKnight'

import mido
from time import sleep

class MidiOutput:
    def __init__(self):
        self.port = None

    def __enter__(self):
        print('enter')
        mido.set_backend('mido.backends.rtmidi')
        self.port = mido.open_output("GeneticMusicOutVirtualPort", virtual=True)
        sleep(1)  # Ensure the virtual MIDI port has time to register
        return self

    def __exit__(self, type, value, traceback):
        sleep(3)  # Wait for note off messages just in case
        print('exit')
        del self.port

    def play_note(self):
        print('play note')
        message = mido.Message('note_on', note=100, velocity=127, time=6.2)
        self.port.send(message)