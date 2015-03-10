__author__ = 'TrevorKnight'

import MidiOutput
import music21
import SimpleChordChromosome

simpleMelodyGenerator = SimpleChordChromosome.SimpleMelodyGenerator(20)


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

for genotype in simpleMelodyGenerator.population:
    print(genotype.fitness)
    s = simpleMelodyGenerator.render_music(genotype)
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

