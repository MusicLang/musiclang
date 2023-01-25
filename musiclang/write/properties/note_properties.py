"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

class NoteProperties:
    """ """

    def __init__(self, note):
        self.note = note


    @property
    def notes(self):
        """ """
        from ..melody import Melody
        return Melody([self.note], tags=self.note.tags).notes

    @property
    def scale_pitch(self):
        """ """
        if self.note.type == "s":
            return self.note.val + 7 * self.note.octave
        elif self.note.type == "h":
            return (7 * self.note.val//12) + 7 * self.note.octave
        else:
            raise Exception(f'Not well defined pitch for type {self.note.type}')

    @property
    def delta_value(self):
        """ """
        if self.note.type[1] == "u":
            return self.note.val
        elif self.note.type[1] == "d":
            return -self.note.val
        else:
            raise Exception(f'Not well defined delta value for type {self.note.type}')

    @property
    def ppp(self):
        """ """
        note = self.note.copy()
        note.amp = 20
        return note

    @property
    def pp(self):
        """ """
        note = self.note.copy()
        note.amp = 40
        return note

    @property
    def p(self):
        """ """
        note = self.note.copy()
        note.amp = 60
        return note

    @property
    def mf(self):
        """ """
        note = self.note.copy()
        note.amp = 80
        return note

    @property
    def f(self):
        """ """
        note = self.note.copy()
        note.amp = 100
        return note

    @property
    def ff(self):
        """ """
        note = self.note.copy()
        note.amp = 110
        return note

    @property
    def fff(self):
        """ """
        note = self.note.copy()
        note.amp = 120
        return note

    @property
    def amp_figure(self):
        """ """
        note = self.note.copy()
        if note.amp <= 20:
            return 'ppp'
        elif note.amp <= 40:
            return 'pp'
        elif note.amp <= 60:
            return 'p'
        elif note.amp <= 80:
            return 'mf'
        elif note.amp <= 100:
            return 'f'
        elif note.amp <= 110:
            return 'ff'
        else:
            return 'fff'


    @property
    def is_up(self):
        """ """
        return "u" in self.note.type

    @property
    def is_down(self):
        """ """
        return "d" in self.note.type

    @property
    def had_absolute_note(self):
        """ """
        return self.note.starts_with_absolute_note

    @property
    def is_relative(self):
        """ """
        return ("u" in self.note.type or "d" in self.note.type)

    @property
    def starts_with_relative(self):
        """ """
        return self.note.is_relative

    @property
    def starts_with_absolute_or_silence(self):
        """ """
        return self.note.type == "r" or self.note.starts_with_absolute_note

    @property
    def is_silence(self):
        """ """
        return self.note.type == "r"

    @property
    def is_pattern_note(self):
        """ """
        return "a" in self.note.type

    @property
    def is_chromatic_note(self):
        """ """
        return "h" in self.note.type

    @property
    def is_scale_note(self):
        """ """
        return "s" in self.note.type

    @property
    def is_chord_note(self):
        """ """
        return "c" in self.note.type

    @property
    def is_continuation(self):
        """ """
        return self.note.type == "l"

    @property
    def is_note(self):
        """ """
        return self.note.type not in ["r", "l"]

    @property
    def starts_with_note(self):
        """ """
        return self.note.type not in ["r", "l"]

    @property
    def starts_with_absolute_note(self):
        """ """
        return self.note.starts_with_note and not self.note.is_relative

    @property
    def M(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "M"
        return new_note

    @property
    def m(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "m"
        return new_note

    @property
    def mm(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "mm"
        return new_note

    @property
    def dorian(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "dorian"
        return new_note

    @property
    def phrygian(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "phrygian"
        return new_note

    @property
    def lydian(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "lydian"
        return new_note

    @property
    def mixolydian(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "mixolydian"
        return new_note

    @property
    def aeolian(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "aeolian"
        return new_note

    @property
    def locrian(self):
        """ """
        new_note = self.note.copy()
        new_note.mode = "locrian"
        return new_note

    @property
    def dim(self):
        """ """
        new_note = self.note.copy()
        new_note.accident = "dim"
        return new_note

    @property
    def min(self):
        """ """
        new_note = self.note.copy()
        new_note.accident = "dim"
        return new_note

    @property
    def natural(self):
        """ """
        new_note = self.note.copy()
        new_note.accident = "natural"
        return new_note

    @property
    def maj(self):
        """ """
        new_note = self.note.copy()
        new_note.accident = "maj"
        return new_note


    @property
    def aug(self):
        """ """
        new_note = self.note.copy()
        new_note.accident = "aug"
        return new_note