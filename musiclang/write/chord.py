"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .constants import *
import re

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
        self.extension = str(extension)
        self.extension = self.normalize_extension()
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

    def clear_note_tags(self):
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
        for k, v in cp.score.items():
            cp.score[k] = v.clear_note_tags()
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

    def has_pitch(self, pitch):
        """
        Check whether the pitch belong to the chord or not

        Parameters
        ----------
        pitch: int
        Pitch to check

        Returns
        -------
        result: boolean
            True if the chord has this pitch

        """
        return (pitch % 12) in [p % 12 for p in self.chord_pitches]

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

    def project_on_score(self, score2, **kwargs):
        """
        Transform chord into a score and apply Score.project_on_score
        Parameters
        ----------
        score2: other score on which to project
        voice_leading:
        kwargs
        Returns
        -------
        """
        return self.to_score().project_on_score(score2, **kwargs)

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


    def realize_tags(self, last_note=None, final_note=None):
        new_chord_dict = {}
        last_note = last_note or {}
        final_note = final_note or {}
        for key, melody in self.score.items():
            new_chord_dict[key] = melody.realize_tags(last_note.get(key, None), final_note.get(key, None))
        return self(**new_chord_dict)


    def correct_chord_octave(self):
        """
        Correct chord octaves to minimize distance with central C

        Returns
        -------
        score: Score
        """
        from musiclang.analyze import inverse_recursive_correct_octave
        return inverse_recursive_correct_octave(self)

    def split(self, max_length):
        """
        Split the chords that are too long into smaller chords
        Parameters
        ----------
        max_length: fraction
           The maximum length of a chord

        Returns
        -------
        score: Score
           The score with shorter chords

        """
        score = None
        if self.duration <= max_length:
            return self
        nb_chords = 1 + (self.duration // max_length)
        remaining_duration = self.duration % max_length
        from musiclang.library import s0
        chords = [self(s0.augment(max_length)) for i in range(nb_chords)]
        if remaining_duration > 0:
            chords[-1].score['piano__0'] = chords[-1].score['piano__0'].set_duration(remaining_duration)
        else:
            chords = chords[:-1]
        chords = sum(chords, None)
        return self.project_on_score(chords)


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

    @property
    def pedal(self):
        """
        Apply pedal on first note and release on last
        """
        return self(**{key: item.to_melody().pedal for key, item in self.score.items()}, tags=set(self.tags))

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
        if note.is_continuation:
            return last_pitch

        if not note.is_note:
            return None
        return note_to_pitch_result(note, self, last_pitch=last_pitch)

    def to_absolute_note(self):
        return self(**{part: melody.to_absolute_note(self) for part, melody in self.score.items()})

    @property
    def bass_pitch(self):
        return self.chord_extension_pitches[0]

    def to_sequence(self):
        """
        See :func:`~Score.to_sequence()
        """
        sequence_dict = []
        for inst in self.instruments:
            sequence_dict += self.score[inst].to_sequence(self, inst)

        return sequence_dict

    def to_score(self, copy=True):
        """ """
        from .score import Score
        chord = self if not copy else self.copy()
        return Score([chord])

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
        :func:`~Tonality.chord_extension_pitches`
        :func:`~Chord.to_pitch()`

        Returns
        -------
        res: List[int]

        Examples
        --------

        >>> from musiclang.library import *
        >>> (I % I.M).chord_pitches
        [0, 4, 7]

        >>> from musiclang.library import *
        >>> (I % I.M)['6'].chord_pitches
        [0, 4, 7]
        """
        notes = self.chord_notes
        return [self.to_pitch(n) for n in notes]

    def remove_accidents(self):
        return Chord(**{key: val.remove_accidents() for key, val in self.score.items()}, tags=set(self.tags))

    def predict_score(self, **kwargs):
        """
        Predict the continuation of the chord/score with a LLM model.
        See :func:`~Score.predict_score()`
        """
        return self.to_score().predict_score(**kwargs)

    def apply_pattern(self, chords, instruments=None, voicing=None, restart_each_chord=False,
                      fixed_bass=True, voice_leading=True, amp='mf'):
        """
        Apply a chord progression to a pattern
        Parameters
        ----------
        pattern: Score or Chord
            Pattern to use
        chords: Score or list or Chord
            Chord progression to use
        instruments: list[str] or None
            Instruments to use, by default use only piano
        voicing: list[Note] or None
            Voicing to use in the pattern. By default, spread the voicing between root -2 octave and fifth +1 octave
        restart_each_chord: bool
            If True, the pattern will be restarted at each chord
        fixed_bass: bool
            If True, the bass will be fixed in the voice leading
        voice_leading: bool
            If True, the voice leading optimizer will be applied
        amp: str
            Amplitude of the pattern (in ppp, pp, p, mp, mf, f, ff, fff)

        Returns
        -------
        Score

        """
        from musiclang.predict.composer import apply_pattern
        return apply_pattern(self, chords, instruments=instruments, voicing=voicing, restart_each_chord=restart_each_chord,
                      fixed_bass=fixed_bass, voice_leading=voice_leading, amp=amp)

    def normalize_chord_duration(self):
        """
        Normalize the duration of the chord (project on the melody with the shortest duration)
        See :func:`~Score.normalize_chord_duration()`
        """
        min_duration = min([melody.duration for melody in self.score.values()])
        base_chord = self.to_chord().set_duration(min_duration)
        return self.project_on_score(base_chord).chords[0]

    def get_scale_from_type(self, type):
        if type == "h":
            return self.chromatic_pitches
        elif type == "s":
            return self.scale_pitches
        elif type == "b":
            return self.chord_extension_pitches
        elif type == "c":
            return self.chord_pitches
        else:
            raise ValueError("This type is not associated to a scale")
    @property
    def chromatic_pitches(self):
        return [self.scale_pitches[0] + i for i in range(12)]
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
    def chord_extension_pitches(self):
        """
        Get the chord absolute pitches (integers) starting with the chord bass as indicated by the extension.

        See Also
        --------
        :func:`~Tonality.chord_pitches`
        :func:`~Chord.to_pitch()`

        Returns
        -------
        res: List[int]

        Examples
        --------

        >>> from musiclang.library import *
        >>> (I % I.M)['6'].chord_extension_pitches
        [4, 7, 12]

        >>> from musiclang.library import *
        >>> (I % I.M)['2[add6]'].chord_extension_pitches
        [-1, 0, 2, 4, 9]
        """

        notes = self.extension_notes
        return [self.to_pitch(n) for n in notes]

    @property
    def chord_extension_pitch_classes(self):
        return [i % 12 for i in self.chord_extension_pitches]
    @property
    def parts(self):
        """
        Get the list of all parts names
        Same as :func:`~Chord.instruments`
        """
        return list(self.score.keys())

    def to_drum(self):
        return self(**{key: val.to_drum() if key.startswith('drum') else val for key, val in self.items()})

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
        try:
            n = res.extension_notes
        except Exception as e:
            raise e
            #raise ValueError(f'Could not parse extension : {item} {e}')
        res.extension = res.normalize_extension()

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

    def set_amp(self, amp):
        return self(**{key: val.set_amp(amp) for key, val in self.items()}, tags=set(self.tags))

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

    def to_extension_note(self):
        return self(**{key: val.to_extension_note(self) for key, val in self.items()}, tags=set(self.tags))

    def to_chord_note(self):
        return self(**{key: val.to_chord_note(self) for key, val in self.items()}, tags=set(self.tags))

    def to_standard_note(self):
        return self(**{key: val.to_standard_note(self) for key, val in self.items()}, tags=set(self.tags))


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

    def patternize(self,
                 nb_excluded_instruments=0,
                 fixed_bass=True,
                 voice_leading=True,
                 melody=False,
                 instruments=None,
                 voicing=None,
                 add_metadata=True,
                   max_duration=16,
                   **kwargs):
        """
        Extract the pattern from the chord

        Parameters
        ----------
        nb_excluded_instruments: int (Default value = 0)
            Number of instruments to exclude from the pattern
        fixed_bass: bool (Default value = True)
            If True, the bass will be fixed in the pattern response
        voice_leading: bool (Default value = True)
            If True, the voice leading will be applied in the pattern response
        melody: bool (Default value = False)
            Do you want to extract a melody or an accompaniment pattern
        instruments: list[str] (Default value = None)
            List of instruments to use for the pattern
        voicing: list[Note] or None (Default value = None)
            Voicing to use for the pattern, otherwise extract the good one
        add_metadata: bool (Default value = True)
            If True, add metadata and features to the pattern
        Returns
        -------
        score_pattern: Chord
            Patternized chord or score
        pattern: dict
            Pattern data of the score

        """
        from musiclang.analyze.pattern_analyzer import PatternExtractor
        if self.duration > max_duration:
            raise Exception(f'Patternize only works on chords with duration <= {max_duration} increase the max_duration parameter if you want to use it on longer chords')

        dict_pattern = PatternExtractor(
                 nb_excluded_instruments=nb_excluded_instruments,
                 fixed_bass=fixed_bass,
                 voice_leading=voice_leading,
                 melody=melody,
                 instruments=instruments,
                 voicing=voicing
                 ).extract(self)

        pattern = dict_pattern['orchestra']['pattern']
        if add_metadata:
            from musiclang.analyze.pattern_analyzer import PatternFeatureExtractor
            dict_pattern = PatternFeatureExtractor().extract(dict_pattern,
                                                             self,
                                                             melody=melody,
                                                             nb_excluded_instruments=nb_excluded_instruments,
                                                             )
        return dict_pattern, pattern

    def project_pattern(self, score, restart_each_chord=False):
        return self.to_score().project_pattern(score, restart_each_chord=restart_each_chord)

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




    def preparse_named_melodies(self, named_melodies):
        """
        Helper function to deal with dictionary of melodies that can contain a list of melodies for some parts.
        It will automatically convert drums melodies to drums track

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
        from musiclang import Melody

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
                    mel = melody.to_melody()
                    if key_obj.startswith('drums'):
                        new_mel = None
                        for n in mel.notes:
                            new_mel += n.convert_to_drum_note(self)
                        mel = new_mel
                    named_melodies_result[key_obj + '__' + str(number + idx)] = mel
            else:
                mel = named_melodies[key].to_melody()
                if key_obj.startswith('drums'):
                    new_mel = None
                    for n in mel.notes:
                        new_mel += n.convert_to_drum_note(self)
                    mel = new_mel
                named_melodies_result[key_obj + '__' + str(number)] = mel

        return named_melodies_result

    def items(self):
        return self.score.items()

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d

    def augment(self, duration):
        from musiclang import Silence
        if self.empty_score:
            silence = Silence(duration)
            return self(silence)
        else:
            return self(**{part: melody.augment(duration) for part, melody in self.score.items()}, tags=self.tags)

    def set_duration(self, duration):
        from musiclang import Silence
        if self.empty_score:
            if isinstance(duration, float):
                duration = frac(duration).limit_denominator(8)
            silence = Silence(duration)
            return self(silence)
        else:
            return self(**{part: melody.set_duration(duration) for part, melody in self.score.items()}, tags=self.tags)

    def __getattr__(self, item):
        if item in STR_TO_DURATION.keys() and self.empty_score:
            from musiclang import Silence
            duration = STR_TO_DURATION[item]
            silence = Silence(duration)
            return self(silence)

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

    @property
    def full_octave(self):
        return self.octave + self.tonality.octave

    def replace_instruments(self, **instruments_dict):
        """
        Replace any instrument with another (use full part name (eg: piano__0)

        Parameters
        ----------
        instruments_dict: dict[str, str]
            Dictionary of parts name to replace

        Returns
        -------
        chord: Chord

        """
        instruments_dict = {key: instruments_dict[key] if key in instruments_dict.keys() else key for key in self.parts}
        new_chord_dict = {}
        for ins_name, new_ins_name in instruments_dict.items():
            if ins_name in self.score.keys():
                new_chord_dict[new_ins_name] = self.score[ins_name]

        return self(**new_chord_dict)


    def normalize_extension(self):
        extension, replacements, additions, removals = self.get_extension_properties()
        replacements = ''.join([f'({r})' for r in replacements])
        additions = ''.join([f'[{a}]' for a in additions])
        removals = ''.join(['{' + r + '}' for r in removals])
        return extension + replacements + additions + removals

    def get_extension_properties(self):
        extension = self.extension.split('|')[0]
        replacements = sorted(re.findall(r'\((.*?)\)', extension))
        additions = sorted(re.findall(r'\[(.*?)\]', extension))
        removals = sorted(re.findall(r'\{(.*?)\}', extension))
        ext = extension
        for r in replacements + additions + removals:
            ext = ext.replace(r, '')
        ext = ext.replace('()', '').replace('[]', '').replace('{}', '')
        extension = ext
        return extension, replacements, additions, removals


    def _chord_notes_calc(self, extension, replacements, additions, removals):
        from .library import BASE_EXTENSION_DICT, \
            DICT_REPLACEMENT, DICT_ADDITION, DICT_REMOVAL
        notes = BASE_EXTENSION_DICT[extension][:]
        notes_without_octave = [n.o(-n.octave) for n in notes]

        dict_replaced = {}
        for replacement in replacements:
            note_replaced, new_note = DICT_REPLACEMENT[replacement]
            if note_replaced not in notes_without_octave:
                additions.append(replacement)
            else:
                idx = notes_without_octave.index(note_replaced)
                notes[idx] = new_note.o(notes[idx].octave)
                notes_without_octave[idx] = new_note.o(-new_note.octave)
                dict_replaced[note_replaced] = notes_without_octave[idx]

        for addition in additions:
            note_after, new_note = DICT_ADDITION[addition]
            if note_after in dict_replaced.keys():
                query_note = dict_replaced[note_after]
            else:
                query_note = note_after
            idx = notes_without_octave.index(query_note) + 1
            new_note = new_note.o(note_after.octave)
            notes.insert(idx, new_note)
            notes_without_octave.insert(idx, new_note.o(-new_note.octave))

        for removal in removals:
            note_removed = DICT_REMOVAL[removal]
            idx = len(notes) - notes_without_octave[::-1].index(note_removed) - 1
            notes.pop(idx)
            notes_without_octave.pop(idx)
        # Sort per pitch
        notes = list(sorted(notes, key=lambda x: self.to_pitch(x)))
        return notes

    @property
    def chord_notes(self):
        extension, replacements, additions, removals = self.get_extension_properties()
        new_extension = ''
        if extension in ['2', '65', '43', '7']:
            new_extension = '7'
        elif extension == '9':
            new_extension = '9'
        elif extension == '11':
            new_extension = '11'
        elif extension == '13':
            new_extension = '13'

        return self._chord_notes_calc(new_extension, replacements, additions, removals)

    @property
    def extension_notes(self):
        # Try a composite with a match
        extension, replacements, additions, removals = self.get_extension_properties()
        return self._chord_notes_calc(extension, replacements, additions, removals)


    def to_voicing(self, nb_voices=4, instruments=None):
        """Convert score to a four voice voicing using the extensions provided in the chord.

        It will remove the existing scores of each chord and create the associated voicings

        Parameters
        ----------
        instruments : None or List[str] (Default value = ['piano__0', 'piano__1', 'piano__2', 'piano__3'])
                      The list of instruments used to create the voicings.

        Returns
        -------

        score: Score
               The score with voicings corresponding to chords

        """

        if instruments is None:
            instruments = [f'piano__{i}' for i in range(nb_voices)]

        notes = self.extension_notes[:nb_voices]
        if not self.empty_score:
            notes = [n.set_duration(self.duration) for n in notes]
        if len(notes) < nb_voices:
            # Add to match octaves
            for i in range(len(notes), nb_voices):
                n = notes[i % len(notes)].copy()
                oct = (i // len(notes))
                n.octave += oct
                notes.append(n)
        chord = self(**{ins: notes[i].copy() for i, ins in enumerate(instruments)})

        return chord


    @property
    def empty_score(self):
        return len(self.score.keys()) == 0

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
