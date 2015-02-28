__author__ = 'TrevorKnight'

import MusicGenes
import MidiOutput
import music21
import SimpleChordChromosome

chromo = SimpleChordChromosome.define_chromosome()

pop = MusicGenes.Population(chromo, 10)
for genotype in pop:
    print(genotype.fitness)
    s = SimpleChordChromosome.render_music(genotype)
    s.show('text')
    s.show('musicxml')
    mf = music21.midi.translate.streamToMidiFile(s)
    mf.open("midi.mid", 'wb')
    mf.write()
    mf.close()
    with MidiOutput.MidiOutput() as output:
        output.play_file("midi.mid")
    score = int(input('Enter fitness: '))
    genotype.fitness = score