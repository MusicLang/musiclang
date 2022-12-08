from .constants import *


class Score:
    def __init__(self, chords=None, config=None):
        self.chords = chords
        self.config = config
        if self.chords is None:
            self.chords = []
        if self.config is None:
            self.config = {'annotation': "", "tempo": 120}


    def to_chords(self):
        res = [chord.to_chord() for chord in self.chords]
        return res

    def copy(self):
        return Score([c.copy() for c in self.chords], config=self.config.copy())

    def o(self, val):
        return Score([c.o_melody(val) for c in self], config=self.config.copy())

    def __add__(self, other):
        from .chord import Chord
        if isinstance(other, Chord):
            return Score(self.copy().chords + [other], config=self.config.copy())
        if isinstance(other, Score):
            return Score(self.copy().chords + other.copy().chords, config=self.config.copy())
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


    def show(self, *args, **kwargs):
        """
        Wrapper to the music21 show method
        :return:
        """
        import music21
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as di:
            midi_file = os.path.join(di, 'data.mid')
            self.to_midi(midi_file, **kwargs)
            score = music21.converter.parse(midi_file)
            return score.show(*args)


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
        elif isinstance(item, list):
            new_score = None
            for chord in self:
                chord_score = {}
                for it in item:
                    if it in chord.score.keys():
                        chord_score[it] = chord.score[it]
                    else:
                        chord_score[it] = Silence(chord.duration)
                new_score += chord(**chord_score)

            return new_score
        else:
            chords = self.chords.__getitem__(item)
            if isinstance(chords, Chord):
                return chords
            return sum(chords, None)

    def put_on_same_chord(self):
        """
        Take the first chord as reference,
        Put everything into this chord (It will of course change the harmony)
        :return:
        """
        from .time_utils import put_on_same_chord
        return put_on_same_chord(self)

    def project_on_score(self, score2, keep_score=False):
        """
        Project harmonically the score onto the score2
        :param score2: Score that contains the harmony
        :param keep_score: Keep the voice of score2 ?
        :return:
        """
        # Algo : For each chord of score2 : get chords that belongs to score1 and reproject on chord of score2
        from .time_utils import project_on_score
        return project_on_score(self.copy(), score2.copy(), keep_score=keep_score)


    def get_chord_between(self, chord, start, end):
        from .time_utils import get_chord_between
        return get_chord_between(chord, start, end)


    def get_score_between(self, start=None, end=None):
        from .time_utils import get_score_between
        return get_score_between(self, start, end)

    def reduce(self, n_voices=4, start_low=False, instruments=None):
        from .arrange_utils import reduce
        return reduce(self, n_voices=n_voices, start_low=start_low, instruments=instruments)

    def to_pickle(self, filepath):
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def from_midi(cls, filename):
        from musiclang.parser.analytical import parse_to_musiclang
        score, config = parse_to_musiclang(filename)
        score.config = config
        return score

    @classmethod
    def from_xml(cls, filename):
        from musiclang.parser.analytical import parse_to_musiclang
        score, config = parse_to_musiclang(filename)
        score.config = config
        return score


    @classmethod
    def from_sequence(cls, sequence, **kwargs):
        from .sequence.sequence import sequence_to_score
        return sequence_to_score(sequence, **kwargs)

    def to_sequence(self, **kwargs):
        from .sequence.sequence import score_to_sequence
        return score_to_sequence(self, **kwargs)


    @classmethod
    def from_pickle(cls, filepath):
        import pickle
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        return data

    def __eq__(self, other):
        from .chord import Chord
        if isinstance(other, Chord):
            return self == Score([other], config=self.config.copy())
        if not isinstance(other, Score):
            return False
        elif len(other.chords) != len(self.chords):
            return False
        else:
            return all([c1 == c2 for c1, c2 in zip(self.chords, other.chords)])

    def __getattr__(self, item):
        chords = self.copy()
        chords.chords = [getattr(s, item) for s in self.chords]
        return chords

    def __mod__(self, other):
        from .tonality import Tonality
        if isinstance(other, Tonality):
            return Score([c % other for c in self.chords], config=self.config.copy())
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

