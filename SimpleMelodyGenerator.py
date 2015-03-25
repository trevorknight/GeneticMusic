__author__ = 'Trevor Knight'

import MusicGenes
import music21

class SimpleMelodyGenerator:

    def _define_chromosome(self):
        scale = [0, 2, 4, 5, 7, 9, 11]
        subdivisions = [1, 2, 3]
        return {"pitches": MusicGenes.SetOfWeightedPossibilitiesGene(scale, 0, 100),\
                "subdivisions": MusicGenes.SetOfWeightedPossibilitiesGene(subdivisions, 0, 100)}

    @staticmethod
    def _insert_major_chord(stream, root, offset):
        n1 = music21.note.Note(root)
        n1.quarterLength = 4

        n2 = music21.note.Note(root + 4)
        n2.quarterLength = 4

        n3 = music21.note.Note(root + 7)
        n3.quarterLength = 4

        stream.insert(offset + 0, n1)
        stream.insert(offset + 0, n2)
        stream.insert(offset + 0, n3)

    def __init__(self, population_size):
        self._chromosome = self._define_chromosome()
        self.population = MusicGenes.Population(self._chromosome, population_size=population_size)

    def render_music(self, genotype):
        s = music21.stream.Stream()
        for measure in range(0, 4):
            root = 60
            if measure % 2:
                root = 67
            self._insert_major_chord(s, root, 4 * measure)

            for beat in range(0, 4):
                number_notes = self._chromosome["subdivisions"]\
                    .get_a_value_based_on_current_weights(genotype["subdivisions"])

                new_note_duration = music21.duration.Duration(1.0 / number_notes)

                for i in range(0, number_notes):
                    new_note_pitch = self._chromosome["pitches"]\
                        .get_a_value_based_on_current_weights(genotype["pitches"])
                    new_note = music21.note.Note(new_note_pitch)
                    new_note._setDuration(new_note_duration)
                    s.insert(4 * measure + beat + i * new_note_duration.quarterLength, new_note)
        return s