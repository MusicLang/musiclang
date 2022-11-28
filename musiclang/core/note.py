from .constants import *

class Note:
    """
    Represents a note
    """
    def __init__(self, type, val, octave, duration, mode=None, amp=120):
        self.type = type
        self.val = val
        self.octave = octave
        self.duration = duration
        self.amp = amp
        self.mode = mode
        self.properties = self.init_properties()


    def __iter__(self):
        return [self].__iter__()

    def real_chord(self, chord):
        new_chord = chord.copy()
        if self.mode is None:
            return new_chord
        else:
            new_chord = new_chord.change_mode(self.mode)
            return new_chord



    def init_properties(self):
        from .properties.note_properties import NoteProperties
        return NoteProperties(self)

    def copy(self):
        return Note(self.type, self.val, self.octave, self.duration, mode=self.mode, amp=self.amp)

    def set_duration(self, value):
        result = self.copy()
        result.duration = value
        return result

    def augment(self, value):
        result = self.copy()
        result.duration *= value
        return result

    def change_type(self, new_type):
        c = self.copy()
        c.type = new_type
        return c

    def add_interval(self, note):
        if note.type[1] not in ['u', 'd']:
            raise Exception('note argument must be a relative type (*u, *d)')
        val = note.val if note.type[1] == 'u' else -note.val
        oct = note.octave
        return self.add_value(val, oct)

    def add_value(self, val, octave):
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
        note = self.copy()
        note.octave += octave
        return note

    def o(self, octave):
        """
        Relative octave (change if definite absolute do not otherwise)
        :param octave:
        :return:
        """
        if self.type in ['s', 'h', 'c']:
            return self.oabs(octave)
        return self.copy()

    def duration_to_str(self):
        return DURATION_TO_STR[self.duration]

    def fix_continuation(self):
        durations_candidates = [d for d in list(DURATION_TO_STR.keys()) if d < self.duration]
        nearest_duration = min(durations_candidates, key=lambda x: abs(x - self.duration))
        remaining_duration = self.duration - nearest_duration
        # Add continuations if necessary
        n1 = self.copy()
        n1.duration = nearest_duration
        n2 = Continuation(remaining_duration)
        return n1 + n2

    def to_code(self):
        """
        Represent a note as valid python code using standard musiclang library
        :return:
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

        if self.octave != 0:
            result += f".o({self.octave})"
        if self.mode is not None:
            result += f".{self.mode}"
        if self.amp <= 110:
            result += f".{self.amp_figure}"

        return result


    ### OPERATORS

    def repr_mode(self):
        if self.mode is not None:
            return f".{self.mode}"

        return ""

    def __repr__(self):
        return self.to_code()
        # try:
        #     return f"{self.type}{self.val}.o{self.octave}.{self.duration_to_str()}{self.repr_mode()}"
        # except KeyError:
        #     notes = self.fix_continuation()
        #     return notes.__repr__()

    def __len__(self):
        return 1

    def __add__(self, other):
        """
        Create a melody from the note and other note or melody
        :param other:
        :return:
        """
        from .melody import Melody
        if isinstance(other, Note):
            return Melody([self, other])
        if isinstance(other, Melody):
            return Melody([self] + other.notes)
        else:
            raise Exception('Cannot add if not instance of Note or melody')

    def __and__(self, n):
        """
        Transpose by n
        :param n:
        :return:
        """
        if self.type in ['s', 'c', 'h']:
            return self.add_value(n, 0)
        else:
            return self.copy()

    def __matmul__(self, other):
        # Apply a function to each note
        return other(self.copy())

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
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
        If other is note, create a vertical melody
        If other is melody append note to vertical melody
        :param other:
        :return:
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
    def __init__(self, duration):
        super().__init__("r", 0, 0, duration)

    def copy(self):
        return Silence(self.duration)

    def __repr__(self):
        try:
            return f"r.{self.duration_to_str()}"
        except KeyError:
            notes = self.fix_continuation()
            return notes.__repr__()

class Continuation(Note):
    def __init__(self, duration):
        super().__init__("l", 0, 0, duration)

    def copy(self):
        return Continuation(self.duration)

    def __repr__(self):
        try:
            return f"l.{self.duration_to_str()}"
        except KeyError:
            notes = self.fix_continuation()
            return notes.__repr__()