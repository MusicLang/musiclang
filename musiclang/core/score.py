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

    def __iter__(self):
        return self.chords.__iter__()

    @property
    def instruments(self):
        """
        Return the list of all voices used in the score
        :return:
        """
        result = []
        for chord in self:
            insts = list(chord.score.keys())
            result += insts
            result = list(set(result))

        return list(sorted(result, key=lambda x: (x.split('__')[0], int(x.split('__')[1]))))


    def __getitem__(self, item):
        """
        If str return a score with only this voice
        Else returns item getter of the list of chords and convert it back to a score
        """
        from .note import Silence
        from .chord import Chord
        if isinstance(item, str):
            new_score = None
            for chord in self:
                if item in chord.score.keys():
                    new_score += chord(**{item: chord.score[item]})
                else:
                    new_score += chord(**{item: Silence(chord.duration)})
            return new_score
        else:
            chords = self.chords.__getitem__(item)
            if isinstance(chords, Chord):
                return (None + chords)
            return sum(chords, None)


    def get_time_measures(self, start=None, end=None):
        time = 0
        start = start if start is not None else 0
        end = end if end is not None else self.duration

        new_score = None
        for chord in self:
            if time >= start:
                new_score += chord.copy()
            if time > end:
                break
            time += chord.duration

        return new_score


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

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d


    @property
    def duration(self):
        return sum([c.duration for c in self.chords])

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

