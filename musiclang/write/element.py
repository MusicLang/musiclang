"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .constants import SCALE_DEGREE

class Element:
    """
    An element represents the basis of numeral roman notation, it usually represents a degree.

    In the library elements are represented with roman notation ``I,II,III,IV,V,VI,VII``
    The first degree is indexed with a 0 value (I has a value of 0)
    It is an intermediary object destined to create chords or tonalities :
    - If you call or modulate this object you get a Chord
    - if you call a mode ``m,M,mm,dorian,phrygian,lydian,mixolydian,aeolian,locrian`` on this you get a Tonality

    Parameters
    ----------

    val: int,
         Degree
    """
    def __init__(self, val):
        self.val = val


    def __add__(self, other):
        from musiclang import Chord, Score
        if isinstance(other, int):
            return Element(self.val + other)
        if isinstance(other, Element):
            return self() + other()
        elif isinstance(Element, (Chord, Score)):
            return self() + other
        else:
            raise Exception('Cannot add if not type int or Element')

    def __repr__(self):
        from .chord import Chord
        return Chord(element=self.val).__repr__()

    def __getitem__(self, extension):
        from .chord import Chord
        return Chord(element=self.val)[extension]

    def __call__(self, *melodies, **named_melodies):
        from .chord import Chord
        return Chord(element=self.val)(*melodies, **named_melodies)


    def __mod__(self, other):
            from .chord import Chord
            return Chord(element=self.val) % other


    def copy(self):
        """ """
        return Element(self.val)

    def o(self, octave):
        """
        Create a new chord from this element octaved with given parameter
        Parameters
        ----------
        octave :
            

        Returns
        -------
        chord: Chord
               The result chord transpose by n octaves
        """
        from .chord import Chord
        return Chord(element=self.val, extension=5).o(octave)


    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d

    @property
    def pitch_set(self):
        """
        Returns chords.pitch_set

        Returns
        -------
         pitches: set
                  The pitches associated with this element
        """
        return self.o(0).pitch_set

    @property
    def scale_set(self):
        """ """
        return self.o(0).scale_set

    @property
    def scale_pitches(self):
        """ """
        return self.o(0).scale_pitches

    @property
    def element(self):
        """ """
        return self.val

    @property
    def tonality(self):
        """ """
        from .tonality import Tonality
        return Tonality(0)

    @property
    def octave(self):
        """ """
        return 0

    @property
    def b(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).b

    @property
    def s(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).s

    @property
    def m(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).m

    @property
    def M(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).M

    @property
    def mm(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).mm


    @property
    def dorian(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).dorian

    @property
    def phrygian(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).phrygian

    @property
    def lydian(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).lydian

    @property
    def mixolydian(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).mixolydian

    @property
    def aeolian(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).aeolian

    @property
    def locrian(self):
        """ """
        from .tonality import Tonality
        return Tonality(SCALE_DEGREE[self.val]).locrian

