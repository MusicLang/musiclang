"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .constants import *

class Chord:

    EXCLUDED_ITEMS = ['__array_struct__']
    def __init__(self, element, extension='5', tonality=None, score=None, octave=0):
        self.element = element
        self.extension = extension
        self.tonality = tonality
        self.octave = octave
        self.score = {} if score is None else score


    def parse(self, pitch):
        from .note import Note
        if pitch % 12 in self.scale_set:
            scale = self.scale_pitches
            type = 's'
        else:
            scale = self.chromatic_scale_pitches
            type = 'h'

        scale_mod = [s % 12 for s in scale]
        idx = scale_mod.index(pitch % 12)
        oct = (pitch - scale[0]) // 12
        return Note(type, idx, oct, 1)

    def decompose_duration(self):
        return self(**{key: melody.decompose_duration() for key, melody in self.score.items()})

    def change_mode(self, mode):
        new_chord = self.copy()
        new_chord.tonality = new_chord.tonality.change_mode(mode)
        return new_chord

    def to_pitch(self, note, last_pitch=None):
        from .out.to_midi import note_to_pitch_result
        if not note.is_note:
            return None
        return note_to_pitch_result(note, self, last_pitch=last_pitch)

    def to_sequence(self):
        sequence_dict = []
        for inst in self.instruments:
            sequence_dict += self.score[inst].to_sequence(self, inst)

        return sequence_dict

    def to_score(self):
        from .score import Score
        return Score([self])

    def show(self, *args, **kwargs):
        return self.to_score().show(*args, **kwargs)

    @property
    def scale_degree(self):
        tonic = self.scale_pitches[0]
        return DEGREE_TO_SCALE_DEGREE[tonic % 12] + tonic // 12

    @property
    def pitch_set(self):
        return frozenset({s % 12 for s in self.chord_pitches})

    @property
    def scale_set(self):
        return frozenset({s % 12 for s in self.scale_pitches})

    @property
    def chord_pitches(self):
        scale_pitches = self.scale_pitches
        max_res = [scale_pitches[i] for i in [0, 2, 4, 6, 1, 3, 5]]
        id = len(self.possible_notes)
        return max_res[:id]

    @property
    def scale_pitches(self):
        from .tonality import Tonality
        if self.tonality is None:
            return (self % Tonality(0)).scale_pitches
        tonality_scale_pitches = self.tonality.scale_pitches
        start_idx = self.element
        scale_pitches = tonality_scale_pitches[start_idx:] + [t + 12 for t in tonality_scale_pitches[:start_idx]]
        scale_pitches = [n + 12 * self.octave for n in scale_pitches]
        return scale_pitches

    @property
    def chromatic_scale_pitches(self):
        return [self.scale_pitches[0] + i for i in range(12)]


    @property
    def parts(self):
        return list(self.score.keys())

    @property
    def instruments(self):
        return list(self.score.keys())

    def get_part(self, item):
        if isinstance(item, int):
            return self.score[self.parts[item]]
        else:
            return self.score[item]


    def score_equals(self, other):
        if not isinstance(other, Chord):
            return False
        return self.score == other.score

    def chord_equals(self, other):
        if not isinstance(other, Chord):
            return False
        return self.element == other.element and self.extension == other.extension and self.tonality == other.tonality and self.octave == other.octave

    def __eq__(self, other):
        from .score import Score
        if isinstance(other, Score):
            return Score([self]) == other
        if not isinstance(other, Chord):
            return False
        return self.chord_equals(other) and self.score_equals(other)

    def __hash__(self):
        return hash( self.__repr__())

    @property
    def possible_notes(self):
        from .note import Note
        if self.extension in ['5', '', '6', '64']:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1)]
        elif self.extension in ['7', '65', '43', '2']:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1)]
        elif self.extension == '9':
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1), Note("s", 1, 1, 1)]
        elif self.extension == '11':
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1), Note("s", 1, 1, 1), Note("s", 3, 1, 1)]
        elif self.extension == '13':
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1),
                    Note("s", 1, 1, 1), Note("s", 3, 1, 1), Note("s", 5, 1, 1)]
        else:
            raise Exception('Unknown extension : ' + self.extension)

    @property
    def scale_notes(self):
        from .note import Note
        return [Note("s", i, 0, 1) for i in range(7)]

    @property
    def scale_dissonances(self):
        consonances = {(note.val % 7) for note in self.possible_notes}
        return [note for note in self.scale_notes if note.val not in consonances]


    def __getitem__(self, item):
        """
        Assign a figured bass to the chord (eg : 64)
        :param item:
        :return:
        """
        item = str(item)
        res = self.copy()
        res.extension = str(item)
        possible_extensions = ['5', '7', '9', '11', '13', '65', '43', '2', '6', '64']
        if item not in possible_extensions:
            raise Exception(f'Not valid chord extension : {item}, possible are : {possible_extensions}')
        return res
    #
    # def __getattr__(self, item):
    #     chord = self.copy()
    #     chord.score = {k: getattr(s, item) for k, s in self.score.items()}
    #     return chord

    @property
    def duration(self):
        """
        Get the chord duration as the max duration of the melodies contained in the chords
        :return:
        """
        if len(self.score.keys()) == 0:
            return 0
        return max([self.score[key].duration for key in self.score.keys()])

    def set_part(self, item, part):
        part_name = self.parts[item] if isinstance(item, int) else item
        self.score[part_name] = part

    def has_score(self):
        return self.score is not None

    def to_chord(self):
        result = self.copy()
        result.score = {}
        return result



    @property
    def chords(self):
        from .score import Score
        return Score([self]).chords

    def __mod__(self, other):
        """
        Modulate to another tonality relative to the current tonality
        :param other:
        :return:
        """
        from .tonality import Tonality
        if isinstance(other, Tonality):
            chord = self.copy()
            # Tonality is always referenced from base tonality which is the most outside tonality
            other = other.copy()
            other.octave += self.octave
            chord.tonality = chord.tonality + other
            chord.octave = 0
            return chord
        else:
            raise Exception('Following % should be a Tonality')


    def modulate(self, other):
        from .tonality import Tonality
        if isinstance(other, Tonality):
            chord = self.copy()
            # Tonality is always referenced from base tonality which is the most outside tonality
            other = other.copy()
            other.octave += self.octave
            chord.tonality = chord.tonality + other
            chord.octave = 0
            return chord
        else:
            raise Exception('Following % should be a Tonality')

    def __add__(self, other):
        """
        Add a new chord to this chord, it will returns a score
        :param other:
        :return: Score
        """
        from .score import Score
        if isinstance(other, Chord):
            return Score([self.copy(), other.copy()])
        if isinstance(other, Score):
            return Score([self.copy()] + other.copy().chords)



    def __radd__(self, other):
        from .score import Score
        if other is None:
            return Score([self.copy()])

    def element_to_str(self):
        return ELEMENT_TO_STR[self.element]

    def extension_to_str(self):
        if str(self.extension) == '5' or str(self.extension) == '':
            return ''
        else:
            return f"['{self.extension}']"



    def tonality_to_str(self, sep="/"):
        if self.tonality is None:
            return ""
        else:
            return f"{sep}" + str(self.tonality)

    def tonality_to_code(self):
        if self.tonality is None:
            return ""

        return " % " + self.tonality.to_code()

    def d(self):
        """
        Chord up one octave (=o(-1))
        """
        return self.o(-1)

    def u(self):
        """
        Chord down one octave (=o(-1))
        """
        return self.o(1)

    def o_melody(self, octave):
        """
        Change the octave of the melody (not the chord)
        :param octave:
        :return:
        """
        new_parts = {}
        for part in self.score:
            new_parts[part] = self.score[part].o(octave)

        return self(**new_parts)

    def o(self, octave):
        """
        Chord up or down the amount of octave in parameter, it will change the chord octave, not the melody
        :param octave:
        :return:
        """
        c = self.copy()
        c.octave += octave
        return c

    def get_chord_between(self, start, end):
        from .time_utils import get_chord_between
        return get_chord_between(self, start, end)

    def copy(self):
        return Chord(element=self.element,
                     extension=self.extension,
                     tonality=self.tonality.copy() if self.tonality is not None else None,
                     score={k: s.copy() for k, s in self.score.items()} if self.score is not None else None,
                     octave=self.octave
                     )

    def preparse_named_melodies(self, named_melodies):
        named_melodies_result = {}
        for key in named_melodies.keys():
            key_obj = key.split('__')
            if len(key_obj) == 1:
                key_obj = key_obj[0]
                number = 0
            else:
                key_obj, number = key_obj[0], key_obj[1]
                number = int(number)

            if(isinstance(named_melodies[key], list)):
                for idx, melody in enumerate(named_melodies[key]):
                    named_melodies_result[key_obj + '__' + str(number + idx)] = melody
            else:
                named_melodies_result[key_obj + '__' + str(number)] = named_melodies[key]

        return named_melodies_result

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d



    def __getattr__(self, item):
        if len(self.parts) == 0:
            raise AttributeError()
        try:
            res = self(**{part: getattr(self.score[part], item) for part in self.parts})
            return res
        except Exception:
            raise AttributeError("Not existing attribute")

    def __call__(self, *melodies, **named_melodies):
        chord = self.copy()
        named_melodies_preparsed = self.preparse_named_melodies(named_melodies)
        chord.score = {**{i: melody for i, melody in enumerate(melodies)}, **named_melodies_preparsed}
        return chord

    def melody_to_str(self):
        return '\n' + ', \n'.join([f"\t{k}=" + str(melody) for k, melody in self.score.items()])

    def __repr__(self):
        return f"{self.to_code()}({self.melody_to_str()})"

    def to_code(self):
        """
        Export the code as python interpretable str.
        It ignores the score
        :return:
        """
        chord_str = f"({self.element_to_str()}{self.extension_to_str()}{self.tonality_to_code()})"
        if self.octave != 0:
            chord_str = f"{chord_str}.o({self.octave})"

        return chord_str

    def to_midi(self, filepath, **kwargs):
        from .score import Score
        return Score([self]).to_midi(filepath, **kwargs)
