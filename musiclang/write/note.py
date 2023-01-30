"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .constants import *


class Note:
    """
    Represents a note in MusicLang.

    **The specificity of MusicLang is that notes are always represented relatively to a chord inside a tonality.**

    Usually you won't be instantiating notes yourself but use the builtin ``musiclang.write.library`` which already
    defines common symbols of musiclang. See the examples to get familiar with the notation library.


    .. warning:: Notes are 0-indexed relative to a scale, so for example ``s0`` is the first note of the scale.

    Note Value
    ----------

    There are different kinds of notes

    - Scale notes : ``s0, s1, s2, s3, s4, s5, s6`` : relative to 7 sounds scale of the chord inside a tonality
    - Chromatic notes : ``h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11`` : \
    relative to the 12 sounds of the chromatic scale associated with the chord/tonality
    - Relative up scale note, ``su0, su1, su2, su3, su4, su5, su6`` : Up relatively to the previous note of a melody
    - Relative down scale note, ``sd0, sd1, sd2, sd3, sd4, sd5, sd6`` : Down relatively to the previous note of a melody
    - Relative up chromatic note, ``hu0, hu1, hu2,  hu3, hu4, hu5, hu6, hu7, hu8, hu9, hu10, hu11`` : \
    Up relatively to the previous note of a melody
    - Relative down chromatic note, ``hd0, hd1, hd2,  hu3, hu4, hu5, hu6, hu7, hu8, hu9, hu10, hu11`` : \
     Down relatively to the previous note of a melody

    Octaves
    -------

    You can specify an octave using the :func:`~o` method of a note
    For example : ``s0.o(1)`` is ``s0`` up one octave, ``s0.o(-1)`` is ``s0`` down one octave

    Rhythm
    -------

    You can spcify a rhythm to a note using properties

    - ``h=half, w=whole, q=quarter, e=eight, s=sixteenth, t=thirty-seconds``
    - You can use n-uplet ``(3, 5, 7)`` : for example s0.e3 is s0 with a duration of a triolet etc ...
    - You can use dots with ``d`` : For example s0.qd has a dotter quarter duration. You can use double dots
    - You can use the :func:`~Note.augment` method if you want a custom duration that can't be notated easily. \
     For example ``s0.augment(8)`` for a duration of two whole notes)

    .. note:: You must use the builtin python `fractions.Fraction` object to create \
    duration otherwise you will get rounding errors when exporting to midi.

    Dynamics
    --------

    You can add dynamics to a note using ``ppp, pp, p, mf, f, ff, fff`` properties of the note
    Example : s0.fff is a note in triple forte

    Silences
    --------

    You can specify a silence using the ``r`` notation in the library, otherwise use the Silence class

    Continuation
    ------------
    You can specify a note continuation using the ``l`` notation in the library, otherwise use the Continuation class

    Mode
    ----

    You can force a mode on a note that bypass the mode of the chord scale.

    Accident
    ---------

    You can force an accident on a note choosing between : ['min', 'maj', 'dim', 'aug', 'natural']
    It is used to force a specific interval that is robust to transposition, but keeping a diatonic value.
    It is advised to be used in replacement of h-type notes because it is in general more compatible with transformations.

    Examples
    --------
    >>> from musiclang.library import s0, s1, s2, I

    You can learn what pitch is associated to a note in the context of a chord :

    >>> chord = (I % I.M) # C major chord (first degree of first major tonality relative to C)
    >>> note = s0
    >>> chord.to_pitch(s0)
    0

    >>> chord.to_pitch(s1)
    2

    >>> chord.to_pitch(s2)
    4

    0 is the note C5 in musiclang, so 2 is D5

    >>> (I % I.m).to_pitch(s2)
    3

    In minor s2 is eb (=3)



    """

    def __init__(self, type, val, octave, duration, mode=None, accident=None, amp=66, tags=None):
        self.type = type
        self.val = val
        self.octave = octave
        self.duration = duration
        self.amp = amp
        self.accident = accident
        self.mode = mode
        self.properties = self.init_properties()
        self.tags = tags if tags is not None else set()

    def has_tag(self, tag):
        """
        Check if the tag exists for this note
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        note: Note
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
        note: Note
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
        note: Note

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
        note: Note


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
        note: Note
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
        note: Note
        """
        cp = self.copy()
        cp.tags = set()
        return cp

    def __iter__(self):
        return [self].__iter__()

    def real_chord(self, chord):
        """

        If the note has a mode

        Parameters
        ----------
        chord :
            

        Returns
        -------

        """
        new_chord = chord.copy()
        if self.mode is None:
            return new_chord
        else:
            new_chord = new_chord.change_mode(self.mode)
            return new_chord

    def decompose_duration(self):
        """
        Decompose a note into note and continuations with existing figures.
        It tries to avoid that the string representation of a note contains any "augment" calls
        """

        def _recurse(note):
            """
            Recursive sub method to decompose a note into smaller values note and continuations
            Parameters
            ----------
            note : musiclang.Note

            Returns
            -------
            Note or Melody

            Examples
            --------

            >>> from musiclang.library import s0
            >>> from fractions import Fraction
            >>> s0.augment(Fraction(11, 8)).decompose_duration()
            s0 + l.s + l.t


            """
            from musiclang.write.constants import DURATION_TO_STR
            from fractions import Fraction as frac

            if note.duration in DURATION_TO_STR:
                return note

            duration = frac(note.duration)
            candidates = [frac(d) for d in DURATION_TO_STR.keys() if d != 0]
            candidates = [c for c in candidates if (duration / c).denominator == 1 and c < duration]
            if len(candidates) == 0:
                return note
            chosen_candidate = max(candidates)
            base_note = note.augment(chosen_candidate / duration)
            new_note = note.augment((duration - base_note.duration) / duration)
            return base_note + _recurse(Continuation(new_note.duration))

        result = _recurse(self)
        # Reverse the melody
        if len(result.notes) > 1:
            result = result[::-1]
            dur = result.notes[0].duration
            result.notes[0] = result.notes[-1].copy().augment(dur / result.notes[-1].duration)
            result.notes[-1] = Continuation(result.notes[-1].duration)
        return result

    def init_properties(self):
        """ """
        from .properties.note_properties import NoteProperties
        return NoteProperties(self)

    def copy(self):
        """ """
        return Note(self.type, self.val, self.octave, self.duration, mode=self.mode, accident=self.accident, amp=self.amp, tags=set(self.tags))

    def set_val(self, val):
        note = self.copy()
        note.val = val
        return note

    def set_duration(self, value):
        """
        Set the duration of a note
        Parameters
        ----------
        value :
            

        Returns
        -------

        """
        result = self.copy()
        result.duration = value
        return result

    def augment(self, value):
        """
        Returns a copy with augmented duration (multiply current duration by the value)

        Parameters
        ----------
        value : fractions.Fraction
                Fraction on which to multiply the current duration
            

        Returns
        -------
        note: Note
              New note with increased duration

        Examples
        --------

        >>> from musiclang.library import s0
        >>> from fractions import Fraction
        >>> s0.augment(Fraction(8, 9))
        s0.augment(frac(8, 9))

        """
        result = self.copy()
        result.duration *= value
        return result

    def change_type(self, new_type):
        """

        Parameters
        ----------
        new_type :
            

        Returns
        -------

        """
        c = self.copy()
        c.type = new_type
        return c

    def add_interval(self, note):
        """

        Parameters
        ----------
        note :
            

        Returns
        -------

        """
        if note.type[1] not in ['u', 'd']:
            raise Exception('note argument must be a relative type (*u, *d)')
        val = note.val if note.type[1] == 'u' else -note.val
        oct = note.octave
        return self.add_value(val, oct)

    def add_value(self, val, octave):
        """

        Parameters
        ----------
        val :
            
        octave :
            

        Returns
        -------

        """
        if self.type[0] in ['s', 'h', 'c']:
            if self.type[0] == 's':
                mod = 7

            elif self.type[0] == 'h':
                mod = 12

            elif self.type[0] == 'c':
                mod = 3

            new_note = self.copy()
            new_note.val += val
            new_note.octave += octave
            new_note.octave += new_note.val // mod
            new_note.val = new_note.val % mod
        else:
            return self.copy()

        return new_note

    def oabs(self, octave):
        """

        Parameters
        ----------
        octave :
            

        Returns
        -------

        """
        note = self.copy()
        note.octave += octave
        return note

    def o(self, octave):
        """
        Relative octave (change if definite absolute do not otherwise)

        Parameters
        ----------
        octave : int
            Number of octave (positive or negative) to transpose the current note


        Returns
        -------
        note: Note
            It will return a new note transposed

        """
        if self.type in ['s', 'h', 'c']:
            return self.oabs(octave)
        return self.copy()

    def duration_to_str(self):
        """ """
        return DURATION_TO_STR[self.duration]

    def to_code(self):
        """
        Represent a note as valid python code using standard musiclang library

        Parameters
        ----------

        Returns
        -------

        A string representation of the note valid using standard musiclang library

        """

        if self.is_note:
            result = f"{self.type}{self.val}"
        else:
            result = f"{self.type}"

        if self.duration != Q:
            if self.duration in DURATION_TO_STR:
                duration = DURATION_TO_STR[self.duration]
                result += f".{duration}"
            else:
                if isinstance(self.duration, int):
                    result += f".augment({self.duration}))"
                else:
                    result += f".augment(frac({self.duration.numerator}, {self.duration.denominator}))"

        if self.octave != 0 and self.is_note:
            result += f".o({self.octave})"
        if self.mode is not None and self.is_note:
            result += f".{self.mode}"
        if self.accident is not None and self.is_note:
            result += f".{self.accident}"
        if self.is_note:
            amp_figure = self.amp_figure
            if amp_figure != 'mf':
                result += f".{self.amp_figure}"

        return result


    def remove_accidents(self):
        new_note = self.copy()
        new_note.accident = None
        return new_note

    @property
    def has_accident(self):
        return self.accident is not None

    def to_sequence(self, chord, inst):
        """
        Helper function to generate an array of some specific property from a note
        .. warning:: Only used internally to generate a dataframe from a Score

        Transform in a list of [(start_time, end_time, pitch, self)]

        Parameters
        ----------
        chord : Chord
            Chord on which the note will be played

            
        inst : str
            Instrument on which the note will be played

        Returns
        -------
        A List of list with one element

        Examples
        --------

        >>> from musiclang.library import *
        >>> s0.to_sequence(I % I.M, 'piano__0')
        [[0,1,0,(I % I.M)(),'piano__0',s0]]
        """

        from .melody import Melody
        return Melody([self]).to_sequence(chord, inst)

    def to_melody(self):
        from .melody import Melody
        return Melody([self], tags=self.tags)

    def repr_mode(self):
        """ """
        if self.mode is not None:
            return f".{self.mode}"

        return ""

    def __repr__(self):
        return self.to_code()

    def __len__(self):
        return 1

    def __add__(self, other):
        """
        Create a melody from the note and other note or melody
        Parameters
        ----------
        other : Note or Melody

        Returns
        -------

        A melody with the concatenated notes

        """
        from .melody import Melody
        if other is None:
            return self.copy()
        if isinstance(other, Note):
            return Melody([self, other])
        if isinstance(other, Melody):
            return Melody([self] + other.notes)
        else:
            raise Exception('Cannot add if not instance of Note or melody')

    def __and__(self, n):
        """
        Transpose the value of the note by n

        Parameters
        ----------

        n : int
            Value to transpose the note

        Examples
        --------

        >>> from musiclang.library import *
        >>> s0 & 2
        s2
        """
        if self.type in ['s', 'c', 'h']:
            return self.add_value(n, 0)
        elif self.type in ['h']:
            return self.add_value((12 * n) // 7, 0)
        else:
            return self.copy()

    def __matmul__(self, other):
        """
        Apply a function to this note
        The function should have the signature ``f(note: Note) -> Note | Melody``

        Parameters
        ----------
        other : function
                Function to apply to this note

        Returns
        -------
        note: Note
              Note with applied function

        Examples
        --------

        >>> from musiclang.library import *
        >>> f = lambda note: note.fff
        >>> s0 @ f
        s0.fff


        """
        # Apply a function to each note
        return other(self.copy())

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        """
        Check if two notes are equals. To be equals note should have

        - Same type
        - Same value
        - Same duration
        - Same octave
        - Same mode

        Parameters
        ----------
        other : Other note to compare

        Returns
        -------
        is_equal: bool

        Examples
        --------

        >>> from musiclang.library import *
        >>> s0 == s1 & -1
        """
        if not isinstance(other, Note):
            return False
        else:
            return (self.type == other.type) and (self.val == other.val) and (self.duration == other.duration) and \
                   (self.octave == other.octave) and (self.mode == other.mode)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d

    def __getattr__(self, item):
        try:
            note = self.copy()
            note.duration *= STR_TO_DURATION[item]
            return note
        except KeyError:
            if hasattr(self.properties, item):
                return getattr(self.properties, item)
            else:
                raise AttributeError('Not existing properties of attribute {}'.format(item))

    def __mul__(self, other):
        """
        If other is Integer, repeat the note other times
        """
        from .melody import Melody
        if isinstance(other, int):
            return Melody([self.copy() for i in range(other)])
        else:
            raise Exception('Cannot multiply Note and ' + str(type(other)))

    def __radd__(self, other):
        from .melody import Melody
        if other is None:
            return Melody([self.copy()])
        else:
            raise Exception('Cannot add')


### DERIVED CLASSES OF NOTE

class Silence(Note):
    """
    Represents a silence in MusicLang.

    Only takes a duration as a parameter
    """

    def __init__(self, duration, tags=None):
        super().__init__("r", 0, 0, duration, tags=tags)

    def copy(self):
        """ """
        return Silence(self.duration, tags=set(self.tags))


class Continuation(Note):
    """
    Represents a continuation in MusicLang.

    Only takes a duration as a parameter
    """

    def __init__(self, duration, tags=None):
        super().__init__("l", 0, 0, duration, tags=tags)

    def copy(self):
        """ """
        return Continuation(self.duration, tags=set(self.tags))
