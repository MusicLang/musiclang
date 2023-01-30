"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .constants import *


class Chord:
    """
    Represents a chord in MusicLang.

    The chord is composed of :

        - One degree in ``I, II, III, IV, V, VI, VII``
        - One extension (optional) that represents figured bass in ``5,6,64,7,65,43,2,9,11,13``
        - One tonality itself composed of :

            - A degree in ``I, II, III, IV, V, VI, VII``
            - A mode in ``'M', 'm', 'mm', 'dorian, 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian'``
        - One score : A Dictionary where keys are part names, values are :func:`~musiclang.Melody`
        - One octave : An integer that specifies on which octave transpose the chord

    .. note:: In reality a chord in MusicLang is a "chord scale" because it always implies a tonality.

    Examples
    --------

    >>> from musiclang.library import *
    >>> score =  (I % I.M)(s0, s2)
    >>> score
    (I % I.M)(
        piano_0=s0,
        piano_1=s2)

    You can also pass a list of melodies to an instrument :

    >>> score =  (I % I.M)(violin=[s0, s2, s4.e + s2.e])
    >>> score
    (I % I.M)(
        violin__0=s0,
        violin__1=s2,
        violin__2=s4.e + s2.e)

    Finally can also pass a list of voices to an instrument :

    >>> score =  (I % I.M)(piano__0=s0 + s2, piano__2= s2 + s4)
    >>> score
     (I % I.M)(
         piano__0=s0 + s2,
         piano__2= s2 + s4)

    """

    EXCLUDED_ITEMS = ['__array_struct__']

    def __init__(self, element, extension='', tonality=None, score=None, octave=0, tags=None):
        """

        Parameters
        ----------
        element: int
        extension: int or str , optional
                 Represents the figured bass. Must be in ['','5','6','64','7','65','43','2','9','11','13']
        tonality: musiclang.Tonality, optional
                Represents the tonality of the chord
        score: dict, optional
               Represents the melodies and instruments played by this chord
        octave: int, optional
                Represents the base octave of the chord
        """
        self.element = element
        self.extension = extension
        self.tonality = tonality
        self.octave = octave
        self.score = {} if score is None else score
        self.tags = set(tags) if tags is not None else set()

    def has_tag(self, tag):
        """
        Check if the tag exists for this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        return tag in self.tags

    def add_tag(self, tag):
        """
        Add a tag to this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        cp = self.copy()
        cp.tags.add(tag)
        return cp

    def add_tags(self, tags):
        """
        Add several tags to the object.
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]
        tags to add

        Returns
        -------
        chord: Chord

        """
        cp = self.copy()
        cp.tags = cp.tags.union(set(tags))
        return cp

    def remove_tags(self, tags):
        """
        Remove several tags from the object.
        Returns a copy of the object

        Parameters
        ----------
        tags: List[str]

        Returns
        -------
        chord: Chord


        """
        cp = self.copy()
        cp.tags = cp.tags - set(tags)
        return cp

    def remove_tag(self, tag):
        """
        Remove a tag from this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        cp = self.copy()
        cp.tags.remove(tag)
        return cp

    def clear_tags(self):
        """
        Clear all tags from this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        chord: Chord
        """
        cp = self.copy()
        cp.tags = set()
        return cp

    def parse(self, pitch):
        """
        Parse an integer pitch (0=C5)
        Parameters
        ----------
        pitch :
            

        Returns
        -------

        """
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
        """ """
        return self(**{key: melody.decompose_duration() for key, melody in self.score.items()}, tags=self.tags)

    @property
    def degree(self):
        return self.element

    def get_note_degree_accident(self, note):
        from .constants import DEGREE_TO_SCALE_DEGREE
        if note.type == 's':
            return note.val
        elif note.type in ['l', 'r']:
            return (None, None)
        elif note.type == 'h':
            pass



    @property
    def mode(self):
        return self.tonality.mode

    def change_mode(self, mode):
        """

        Parameters
        ----------
        mode :
            

        Returns
        -------

        """
        new_chord = self.copy()
        new_chord.tonality = new_chord.tonality.change_mode(mode)
        return new_chord

    def to_pitch(self, note, last_pitch=None):
        """

        Parameters
        ----------
        note :
            
        last_pitch :
             (Default value = None)

        Returns
        -------

        """
        from .out.to_midi import note_to_pitch_result
        if not note.is_note:
            return None
        return note_to_pitch_result(note, self, last_pitch=last_pitch)

    def to_sequence(self):
        """
        See :func:`~Score.to_sequence()
        """
        sequence_dict = []
        for inst in self.instruments:
            sequence_dict += self.score[inst].to_sequence(self, inst)

        return sequence_dict

    def to_score(self):
        """ """
        from .score import Score
        return Score([self])

    def show(self, *args, **kwargs):
        """
        See :func:`~Score.show()
        """
        return self.to_score().show(*args, **kwargs)


    def to_musicxml(self, *args, **kwargs):
        return self.to_score().to_musicxml(*args, **kwargs)


    def to_music21(self, *args, **kwargs):
        return self.to_score().to_music21(*args, **kwargs)


    @property
    def scale_degree(self):
        """

        Returns
        -------

        """
        tonic = self.scale_pitches[0]
        return DEGREE_TO_SCALE_DEGREE[tonic % 12] + tonic // 12

    @property
    def pitch_set(self):
        """
        Get a frozenset of :func:`~Chord.chord_pitches`
        """
        return frozenset({s % 12 for s in self.chord_pitches})

    @property
    def pitch_dict(self):
        chromatic_dict = {self.to_pitch(note): note for note in self.chromatic_scale_notes}
        diatonic_dict = {self.to_pitch(note): note for note in self.scale_notes}

        return {**chromatic_dict, **diatonic_dict}


    @property
    def scale_set(self):
        """
        Get a frozenset of :func:`~Chord.scale_pitches`
        """
        return frozenset({s % 12 for s in self.scale_pitches})

    @property
    def chord_pitches(self):
        """
        Get the chord absolute pitches (integers) starting with the chord root.

        See Also
        --------
        :func:`~Tonality.scale_pitches`
        :func:`~Chord.to_pitch()`

        Returns
        -------
        res: List[int]

        Examples
        --------

        >>> from musiclang.library import *
        >>> (I % I.M).chord_pitches
        [0, 4, 7]

        """
        scale_pitches = self.scale_pitches
        max_res = [scale_pitches[i] for i in [0, 2, 4, 6, 1, 3, 5]]
        id = len(self.possible_notes)
        return max_res[:id]

    def remove_accidents(self):
        return Chord({key: val.remove_accidents() for key, val in self.score.items()}, tags=set(self.tags))


    @property
    def scale_pitches(self):
        """
        Get the scale absolute pitches (integers) starting with the chord root.

        See Also
        --------
        :func:`~Tonality.scale_pitches`
        :func:`~Chord.to_pitch()`

        Returns
        -------
        res: List[int]

        Examples
        --------

        >>> from musiclang.library import *
        >>> (I % I.M).scale_pitches
        [0, 2, 4, 5, 7, 9, 11]

        """
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
        """ """
        return [self.scale_pitches[0] + i for i in range(12)]

    @property
    def parts(self):
        """
        Get the list of all parts names
        Same as :func:`~Chord.instruments`
        """
        return list(self.score.keys())

    @property
    def instruments(self):
        """
        Get the list of all part names
        """
        return list(self.score.keys())

    def get_part(self, item):
        """
        Get the corresponding part of the chord score. Can be an integer (part index) or a string (part name)

        Parameters
        ----------
        item : str or int
               Part name or part index

        Returns
        -------
        melody: Melody
                The melody corresponding to the part

        """
        if isinstance(item, int):
            return self.score[self.parts[item]]
        else:
            return self.score[item]

    def score_equals(self, other):
        """
        Check if the parts of both chords are equal

        Parameters
        ----------
        other : Chord

        Returns
        -------
        res : bool

        """
        if not isinstance(other, Chord):
            return False
        return self.score == other.score

    def chord_equals(self, other):
        """
        Check if two chords are equal

        Parameters
        ----------
        other :
            

        Returns
        -------
        res: bool

        """
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

    def __and__(self, other):
        if isinstance(other, int):
            return self(**{part: melody & other for part, melody in self.score.items()})
        else:
            raise Exception(f'Not compatible type with & {other.__class__}')

    def __hash__(self):
        return hash(self.__repr__())

    @property
    def possible_notes(self):
        """
        List the notes that belong to the chord (only the chord, not the scale)

        Returns
        -------
        notes: List[Note]
               The list of possible notes for a chord

        """
        from .note import Note
        if self.extension in ['5', '', '6', '64']:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1)]
        elif self.extension in ['7', '65', '43', '2']:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1)]
        elif self.extension == '9':
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1), Note("s", 1, 1, 1)]
        elif self.extension == '11':
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1), Note("s", 1, 1, 1),
                    Note("s", 3, 1, 1)]
        elif self.extension == '13':
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1),
                    Note("s", 1, 1, 1), Note("s", 3, 1, 1), Note("s", 5, 1, 1)]
        else:
            raise Exception('Unknown extension : ' + self.extension)

    @property
    def scale_notes(self):
        """
        List the notes that belong to the chord scale

        Returns
        -------
        notes: List[Note]
               The list of possible notes for the chord scale
        """
        from .note import Note
        return [Note("s", i, 0, 1) for i in range(7)]

    @property
    def chromatic_scale_notes(self):
        """
        List the chromatic notes that belong to the chord scale

        Returns
        -------
        notes: List[Note]
               The list of possible chromatic notes for the chord scale
        """
        from .note import Note
        return [Note("h", i, 0, 1) for i in range(12)]

    @property
    def scale_dissonances(self):
        """
        Returns the notes that don't belong to the chord but belong to the chord scale

        Returns
        -------
        notes: List[Note]
               The list of possible notes for the chord scale
        """
        consonances = {(note.val % 7) for note in self.possible_notes}
        return [note for note in self.scale_notes if note.val not in consonances]

    def __getitem__(self, item):
        """
        Attach a figured bass to the chord (eg : 64)

        Parameters
        ----------

        item: int or str in ['5', '7', '9', '11', '13', '65', '43', '2', '6', '64', '']
              Extension of the chord

        Returns
        -------

        chord: Chord
               A new chord with the figured bass extension

        """
        item = str(item)
        res = self.copy()
        res.extension = str(item)
        possible_extensions = ['5', '7', '9', '11', '13', '65', '43', '2', '6', '64', '']
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

        Returns
        -------
        duration: fractions.Fraction or int
                  duration of the chord
        """
        if len(self.score.keys()) == 0:
            return 0
        return max([self.score[key].duration for key in self.score.keys()])

    def set_part(self, part, melody, inplace=False):
        """
        Set a part on the chord (inplace operation)
        Parameters
        ----------
        part : part name

        melody :  melody to apply to the part
        inplace: bool
                 If the operation is inplace

        Returns
        -------

        """

        if inplace:
            score = self
        else:
            score = self.copy()
        part_name = score.parts[part] if isinstance(part, int) else part
        score[part_name] = melody
        return score


    def has_score(self):
        """

        """
        return self.score is not None

    def to_chord(self):
        """
        Returns a copy of the chord without the chord score

        Returns
        -------
        chord: Chord
               Chord with empty score

        """
        result = self.copy()
        result.score = {}
        return result

    @property
    def chords(self):
        """
        Returns a Score object with this chord

        Returns
        -------
        score: Score
               The score with this chord as the only element

        """
        from .score import Score
        return Score([self]).chords

    def __mul__(self, other):
        """
        If other is Integer, repeat the note other times
        """
        from .score import Score
        if isinstance(other, int):
            return Score([self.copy() for i in range(other)])
        else:
            raise Exception('Cannot multiply Chord and ' + str(type(other)))

    def __mod__(self, other):
        """
        Modulate to another tonality relative to the current tonality

        Parameters
        ----------
        other: Tonality
            Tonality on which to modulate this chord
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
        """
        Modulate to another tonality relative to the current tonality

        Parameters
        ----------
        other: Tonality
            Tonality on which to modulate this chord
            

        Returns
        -------
        chord: Chord
               Modulated chord

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

    def __add__(self, other):
        """
        Add a new chord to this chord, it will returns a score

        Parameters
        ----------

        other: Chord or Score
               Create a new score concatenating this and the other object

        Examples
        ---------

        >>> from musiclang.library import *
        >>> chord1 = (I % I.M)(piano__0=s0)
        >>> chord2 = (V % I.M)(piano__0=s0)
        >>> chord + chord2
        (I % I.M)(piano__0=s0) + (V % I.M)(piano__0=s0)

        """

        from .score import Score
        if other is None:
            return self.copy()
        if isinstance(other, Chord):
            return Score([self.copy(), other.copy()])
        if isinstance(other, Score):
            return Score([self.copy()] + other.copy().chords)

    def __radd__(self, other):
        from .score import Score
        if other is None:
            return Score([self.copy()])

    def element_to_str(self):
        """
        Convert the element of the chord into a string

        Returns
        -------
        res: str

        """
        return ELEMENT_TO_STR[self.element]

    def extension_to_str(self):
        """
        Converts the extension of the chord into a string

        Returns
        -------
        res: str

        """
        if str(self.extension) == '5' or str(self.extension) == '':
            return ''
        else:
            return f"['{self.extension}']"


    def tonality_to_str(self):
        """
        Convert the tonality of the chord to a string.

        Parameters
        ----------

        Returns
        -------

        """
        if self.tonality is None:
            return ""

        return " % " + self.tonality.to_code()

    def d(self):
        """Chord up one octave (=o(-1))"""
        return self.o(-1)

    def u(self):
        """Chord down one octave (=o(-1))"""
        return self.o(1)

    def o_melody(self, octave):
        """Change the octave of the melody (not the chord)

        Parameters
        ----------
        octave : int,
                Number of octaves

        Returns
        -------
        chord : Chord

        """
        new_parts = {}
        for part in self.score.keys():
            new_parts[part] = self.score[part].o(octave)

        return self(**new_parts).add_tags(self.tags)

    def o(self, octave):
        """Chord up or down the amount of octave in parameter, it will change the chord octave, not the melody

        Parameters
        ----------
        octave :
            return:

        Returns
        -------

        """
        c = self.copy()
        c.octave += octave
        return c

    def get_chord_between(self, start, end):
        """

        Parameters
        ----------
        start :
            
        end :
            

        Returns
        -------

        """
        from .time_utils import get_chord_between
        return get_chord_between(self, start, end)

    def copy(self):
        """
        Copy the current chord
        """
        return Chord(element=self.element,
                     extension=self.extension,
                     tonality=self.tonality.copy() if self.tonality is not None else None,
                     score={k: s.copy() for k, s in self.score.items() if s is not None} if self.score is not None else None,
                     octave=self.octave,
                     tags=set(self.tags)
                     )

    @staticmethod
    def preparse_named_melodies(named_melodies):
        """
        Helper function to deal with dictionary of melodies that can contain a list of melodies for some parts

        Parameters
        ----------
        named_melodies : dict
                         The dictionary of named melodies
            

        Returns
        -------
        res: dict
             The

        Examples
        --------
        >>> from musiclang.library import *
        >>> from musiclang import Chord
        >>> D = {"piano":[s0, s2, s4.e + s2.e]}
        >>> Chord.preparse_named_melodies(D)
        {
            piano__0:s0,
            piano__1:s2,
            piano__2:s4.e + s2.e
            }

        """
        named_melodies_result = {}
        for key in named_melodies.keys():
            key_obj = key.split('__')
            if len(key_obj) == 1:
                key_obj = key_obj[0]
                number = 0
            else:
                key_obj, number = key_obj[0], key_obj[1]
                number = int(number)

            if (isinstance(named_melodies[key], list)):
                for idx, melody in enumerate(named_melodies[key]):
                    named_melodies_result[key_obj + '__' + str(number + idx)] = melody.to_melody()
            else:
                named_melodies_result[key_obj + '__' + str(number)] = named_melodies[key].to_melody()

        return named_melodies_result

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d

    def __getattr__(self, item):
        if len(self.parts) == 0:
            raise AttributeError()
        try:
            res = self(**{part: getattr(self.score[part], item) for part in self.parts}, tags=self.tags)
            return res
        except Exception:
            raise AttributeError(f"Not existing attribute {item}")

    def __call__(self, *melodies, tags=None, **named_melodies):
        """
        Method that allows to assign melodies and instruments to a chord

        Parameters
        ----------
        *melodies: List[Melody]
                   Melodies that will be assigned to default instrument (piano)
        **named_melodies: Dict[str, Melody]
                        Dictionary of named melodies that will be unpacked if necessary

        Returns
        -------

        Examples
        ________

        >>> from musiclang.library import *
        >>> score =  (I % I.M)(s0, s2)
        >>> score
        (I % I.M)(
            piano_0=s0,
            piano_1=s2)

        You can also pass a list of melodies to an instrument :

        >>> score =  (I % I.M)(violin=[s0, s2, s4.e + s2.e])
        >>> score
        (I % I.M)(
            violin__0=s0,
            violin__1=s2,
            violin__2=s4.e + s2.e)

        Finally can also pass a list of voices to an instrument :

        >>> score =  (I % I.M)(piano__0=s0 + s2, piano__2= s2 + s4)
        >>> score
         (I % I.M)(
             piano__0=s0 + s2,
             piano__2= s2 + s4)
        """
        chord = self.copy()
        if tags is not None:
            chord = chord.add_tags(tags)
        named_melodies_preparsed = self.preparse_named_melodies(named_melodies)
        chord.score = {**{f'piano__{i}': melody.to_melody() for i, melody in enumerate(melodies)}, **named_melodies_preparsed}
        return chord

    def melody_to_str(self):
        """
        Convert The chord score to its string representation

        Returns
        -------
        res: str

        """
        return '\n' + ', \n'.join([f"\t{k}=" + str(melody) for k, melody in self.score.items()])

    def __repr__(self):
        return f"{self.to_code()}({self.melody_to_str()})"

    def to_code(self):
        """Export the code as python interpretable str.
        It ignores the score
        :return:

        Parameters
        ----------

        Returns
        -------

        """
        chord_str = f"({self.element_to_str()}{self.extension_to_str()}{self.tonality_to_str()})"
        if self.octave != 0:
            chord_str = f"{chord_str}.o({self.octave})"

        return chord_str

    def to_midi(self, filepath, **kwargs):
        """
        Save the chord to midi

        See Also
        --------

        :func:`~Score.to_midi()`

        Parameters
        ----------
        filepath :
            
        **kwargs :
            

        Returns
        -------

        """
        from .score import Score
        return Score([self]).to_midi(filepath, **kwargs)
