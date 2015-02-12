__author__ = 'TrevorKnight'

from time import sleep
import rtmidi

class MidiOutput:
    def __init__(self):
        self.midi_output = rtmidi.MidiOut();
        self.output_port = self.midi_output.open_virtual_port("GeneticMusicOutVirtualPort")


    def play_note(self):
        note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
        note_off = [0x80, 60, 0]
        self.midi_output.send_message(note_on)
        sleep(0.5)
        self.midi_output.send_message(note_off)

        del self.midi_output