from .constants import *


class Score:
    def __init__(self, chords=None):
        self.chords = chords
        if self.chords is None:
            self.chords = []

    def to_chords(self):
        res = [chord.to_chord() for chord in self.chords]
        return res

    def copy(self):
        return Score([c.copy() for c in self.chords])

    def __add__(self, other):
        from .chord import Chord
        if isinstance(other, Chord):
            return Score(self.copy().chords + [other])
        if isinstance(other, Score):
            return Score(self.copy().chords + other.copy().chords)
        else:
            raise Exception('Cannot add to Score if not Chord or Score')

    def __getattr__(self, item):
        chords = self.copy()
        chords.chords = [getattr(s, item) for s in self.chords]
        return chords

    def __mod__(self, other):
        from .tonality import Tonality
        if isinstance(other, Tonality):
            return Score([c % other for c in self.chords])
        else:
            raise Exception('Following % should be a Tonality')

    def __radd__(self, other):
        if other is None:
            return self.copy()

    def __repr__(self):
        return ' \n'.join([str(chord) for chord in self.chords])


    def to_code(self, **kwargs):
        """
        Export the chord serie as a string representing valid python code that recreates the score
        :return:
        """
        from .out.to_code import chord_serie_to_code

        code = chord_serie_to_code(self, **kwargs)
        return code

    def to_code_file(self, filepath, **kwargs):
        """
        Export the chord serie as a file representing valid python code that recreates the score
        :param filepath:
        :return:
        """
        code = self.to_code(**kwargs)
        with open(filepath, 'w') as f:
            f.write(code)


    def to_midi(self, filepath, **kwargs):
        # Convert score to midi
        from .out.to_midi import score_to_midi

        return score_to_midi(self, filepath, **kwargs)

