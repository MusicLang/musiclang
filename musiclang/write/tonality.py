"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .constants import *

class Tonality:
    """Represents a tonality.

    It can be applied with the ``%`` operator to a chord to modulate it on another tonality
    It encapsulates a degree, a mode, and an octave


    """
    def __init__(self, degree, mode="M", octave=0, tags=None):
        """
        Initialize the tonality.
        Usually you will use musiclang.library to instantiate the tonalities

        Parameters
        ----------

        degree: Degree
                Degree is absolute degree (between 0 and 12). For example 6 is f#, 11 is b

        mode: str in ["M", "m", "mm", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian"]

        octave: int, default=0
                Octave of the tonality, by default it will be 0 which represents the 5th octave on a piano.
        """
        self.degree = degree
        self.mode = mode
        self.octave = octave
        self.tags = set(tags) if tags is not None else set()


    @classmethod
    def from_str(cls, text):
        tab = 'CDEFGAB'
        notes = [0, 2, 4, 5, 7, 9, 11]
        note = text.replace(':', '').replace('#', '').replace('b', '').replace('-', '')
        tone = notes[tab.index(note.upper())]
        mode = 'M' if note.upper() == note else 'm'

        tone += text.count('#')
        tone += text.count('s')
        tone -= text.count('b')
        tone -= text.count('-')

        return cls(tone, mode)

    def __hash__(self):
        return hash(self.__repr__())


    def has_tag(self, tag):
        """
        Check if the tag exists for this object
        Returns a copy of the object
        Parameters
        ----------
        tag: str

        Returns
        -------
        tonality: Tonality
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
        tonality: Tonality
        """
        cp = self.copy()
        cp.tags.add(tag)
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
        tonality: Tonality
        """
        cp = self.copy()
        cp.tags.remove(tag)
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
        tonality: Tonality

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
        tonality: Tonality


        """
        cp = self.copy()
        cp.tags = cp.tags - set(tags)
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
        tonality: Tonality
        """
        cp = self.copy()
        cp.tags = set()
        return cp

    def change_mode(self, mode):
        """

        Parameters
        ----------
        mode :
            

        Returns
        -------

        """
        new_tonality = self.copy()
        new_tonality.mode = mode
        return new_tonality


    @property
    def scale_set(self):
        """ """
        return frozenset({s % 12 for s in self.scale_pitches})

    @property
    def scale_pitches(self):
        """
        Get the scale absolute pitches (integers)

        See Also
        --------
        :func:`~Chord.scale_pitches`
        :func:`~Chord.to_pitch()`

        Returns
        -------
        res: List[int]

        Examples
        --------

        >>> from musiclang.library import *
        >>> I.M.scale_pitches
        [0, 2, 4, 5, 7, 9, 11]

        """
        abs_degree = self.abs_degree
        mode = self.mode
        pitch_scale = [n + abs_degree for n in SCALES[mode]]
        return pitch_scale

    def _eq(self, other):
        """

        Parameters
        ----------
        other :
            

        Returns
        -------

        """
        return self.degree == other.degree and self.mode == other.mode and self.octave == other.octave

    def __eq__(self, other):
        if not isinstance(other, Tonality):
            return False
        # To get equalities between enharmonies we need to reformulate chord adding neutral modulation
        return (Tonality(0) + self )._eq(Tonality(0) + other )

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def copy(self):
        """
        Returns a copy of the tonality
        """
        return Tonality(self.degree, self.mode, self.octave, tags=set(self.tags))

    def __radd__(self, other):
        if other is None:
            return self
        else:
            raise Exception('Not valid addition of tonality')

    def add(self, other):
        """
        Add another tonality to this one
        - The degree is added (modulo 12 with octave)
        - The mode is the mode of the right tonality

        Parameters
        ----------
        other : Tonality
            

        Returns
        -------

        """
        new_abs_degree = self.degree + other.degree
        new_octave = self.octave + other.octave
        delta_octave = new_abs_degree // 12
        new_degree = new_abs_degree % 12
        new_mode = other.mode
        return Tonality(degree=new_degree, mode=new_mode, octave=new_octave + delta_octave, tags=self.tags.union(other.tags))

    @property
    def abs_degree(self):
        """ """
        return self.degree + 12 * self.octave

    def __add__(self, other):
        """
        Add another tonality
        :param other:
        :return:
        """
        if other is None:
            return self
        else:
            return self.add(other)

    def __sub__(self, other):
        """
        Find the relative tonality to go from other to self
        Parameters
        ----------
        other: Tonality

        Returns
        -------
        tonality: Tonality

        """
        new_abs_degree = self.degree - other.degree
        new_octave = self.octave - other.octave
        delta_octave = new_abs_degree // 12
        new_degree = new_abs_degree % 12
        new_mode = self.mode
        return Tonality(degree=new_degree, mode=new_mode, octave=new_octave + delta_octave,
                        tags=self.tags.union(other.tags))

    @property
    def b(self):
        """ """
        tone = self.copy()
        tone.degree -= 1
        if tone.degree == -1:
            tone.degree = 11
            tone.octave -= 1
        return tone

    @property
    def s(self):
        """ """
        tone = self.copy()
        tone.degree += 1
        if tone.degree == 12:
            tone.degree = 0
            tone.octave += 1
        return tone

    @property
    def m(self):
        """ """
        tone = self.copy()
        tone.mode = "m"
        return tone

    @property
    def M(self):
        """ """
        tone = self.copy()
        tone.mode = "M"
        return tone

    @property
    def mm(self):
        """ """
        tone = self.copy()
        tone.mode = "mm"
        return tone


    @property
    def dorian(self):
        """ """
        tone = self.copy()
        tone.mode = "dorian"
        return tone

    @property
    def phrygian(self):
        """ """
        tone = self.copy()
        tone.mode = "phrygian"
        return tone

    @property
    def lydian(self):
        """ """
        tone = self.copy()
        tone.mode = "lydian"
        return tone

    @property
    def mixolydian(self):
        """ """
        tone = self.copy()
        tone.mode = "mixolydian"
        return tone

    @property
    def aeolian(self):
        """ """
        tone = self.copy()
        tone.mode = "aeolian"
        return tone

    @property
    def locrian(self):
        """ """
        tone = self.copy()
        tone.mode = "locrian"
        return tone


    def d(self):
        """ """
        return self.o(-1)

    def o(self, octave):
        """
        Octave the tonality



        Parameters
        ----------
        octave : int
            

        Returns
        -------
        tonality: Tonality

        """
        tonality = self.copy()
        tonality.octave += octave
        return tonality

    def degree_to_str(self):
        """ """
        return DEGREE_TO_STR[self.degree]

    def __repr__(self):
        return self.to_code()

    def to_code(self):
        """
        Represent the tonality in valid Python code

        Returns
        -------
        tonality_code: str

        """
        result = f"{self.degree_to_str()}.{self.mode}"
        if self.octave != 0:
            result += f".o({self.octave})"

        return result

    def __call__(self, *notes, **kwargs):
        from .custom_chord import CustomChord
        return CustomChord(notes, tonality=self, **kwargs)


    def to_absolute_romantext(self):
        L = ['c', 'db', 'd', 'eb', 'e', 'f', 'f#', 'g', 'ab', 'a', 'bb', 'b']
        return L[self.degree].capitalize() if self.mode == 'M' else L[self.degree]

    def to_romantext(self, base_tonality):
        base_tone = base_tonality.degree
        tone = (self.degree - base_tone) % 12
        base_mode = base_tonality.mode
        mode = self.mode

        L = {
            ('m', 'm'): ['i', 'bii', 'ii', 'iii', '#iii', 'iv', '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii'],
            ('M', 'm'): ['I', 'bII', 'II', 'III', '#III', 'IV', '#IV', 'V', 'VI', '#VI', 'VII', '#VII'],
            ('m', 'M'): ['i', 'bii', 'ii', 'biii', 'iii', 'iv', '#iv', 'v', 'bvi', 'vi', 'bvii', 'vii'],
            ('M', 'M'): ['I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'vii'],
        }
        return L[(mode, base_mode)][tone]