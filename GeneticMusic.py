__author__ = 'TrevorKnight'

import music21

import ChordSequence
import MidiOutput
import MusicGenes
import Soloist


def play_score(music_score):
    mf = music21.midi.translate.streamToMidiFile(music_score)
    mf.open("midi.mid", 'wb')
    mf.write()
    mf.close()
    with MidiOutput.MidiOutput() as output:
        output.play_file("midi.mid")


def show_score(music_score):
    music_score.show('musicxml')
    music_score.show('text')


def main():
    chord_sequence = ChordSequence.ChordSequence()
    soloist = Soloist.Soloist(chord_sequence)
    population = MusicGenes.Population(soloist.get_chromosome(), 20)

    for genotype in population:
        print(genotype.fitness)
        s = soloist.create_score(genotype)
        show_score(s)
        play_score(s)

        have_fitness = False
        while not have_fitness:
            try:
                user_input = int(input('Enter fitness: '))
                have_fitness = True
            except ValueError:
                play_score(s)

        genotype.fitness = user_input

if __name__ == '__main__':
    main()