"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
from functools import cached_property

from .constants import *
from .chord import Chord
import re


class CustomChord(Chord):
    """
    Represents a custom chord in MusicLang.

    The custom chord is composed of :
        - One set of notes
        - One tonality itself composed of :
            - A degree in ``I, II, III, IV, V, VI, VII``
            - A mode in ``'M', 'm', 'mm', 'dorian, 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian'``
        - One score : A Dictionary where keys are part names, values are :func:`~musiclang.Melody`
        - One octave : An integer that specifies on which octave transpose the chord

    .. note:: In reality a chord in MusicLang is a "chord scale" because it always implies a tonality.

    Examples
    --------

    >>> from musiclang.library import *
    >>> custom_chord = I.M(s0, s2, s4)(piano__0=b0.h + b1.h)
    >>> custom_chord
    I.M(s0, s2, s4)(piano__0=b0.h + b1.h)
    """
    def __init__(self, notes, extension='', tonality=None, score=None, octave=0, tags=None, **kwargs):
        """

        Parameters
        ----------
        notes: List[int]
            Notes that compose the chord
        extension: int or str , optional
                 Represents the figured bass. Must be in ['','5','6','64','7','65','43','2','9','11','13']
        tonality: musiclang.Tonality, optional
                Represents the tonality of the chord
        score: dict, optional
               Represents the melodies and instruments played by this chord
        octave: int, optional
                Represents the base octave of the chord
        """
        super().__init__(0, extension=extension, tonality=tonality, score=score, octave=octave, tags=tags)
        self.notes = notes


    @property
    def possible_notes(self):
        """
        List the notes that belong to the chord (only the chord, not the scale)

        Returns
        -------
        notes: List[Note]
               The list of possible notes for a chord

        """
        return [n.copy() for n in self.notes]


    def tonality_to_str(self):
        """
        Convert the tonality of the chord to a string.

        Parameters
        ----------

        Returns
        -------

        """
        if self.tonality is None:
            return "I.M"

        return self.tonality.to_code()



    def copy(self):
        """
        Copy the current custom chord
        """
        return CustomChord(
                     notes=self.notes,
                     extension=self.extension,
                     tonality=self.tonality.copy() if self.tonality is not None else None,
                     score={k: s.copy() for k, s in self.score.items() if
                            s is not None} if self.score is not None else None,
                     octave=self.octave,
                     tags=set(self.tags)
                     )

    def __repr__(self):
        return f"{self.to_code()}({self.melody_to_str()})"


    @cached_property
    def chord_notes(self):
        return [c.copy() for c in self.notes]

    @cached_property
    def extension_notes(self):
        # Try a composite with a match
        return [c.copy() for c in self.notes]

    def notes_to_str(self):
        return  ",".join([str(c) for c in self.notes])

    def to_code(self):
        """Export the code as python interpretable str.
        It ignores the score
        :return:

        Parameters
        ----------

        Returns
        -------

        """
        chord_str = f"{self.tonality_to_str()}({self.notes_to_str()})"
        if self.octave != 0:
            chord_str = f"{chord_str}.o({self.octave})"

        return chord_str

