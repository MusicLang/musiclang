
from musiclang.transform import NoteTransformer


class LimitRegister(NoteTransformer):
    """
    Limit octave and values of notes (In tonal values). Transpose the octave until the note fit the range

    Can be called with a note, a melody, a score or a chord.
    It will be applied for each note.

    Examples
    --------

    >>> from musiclang.transform.library import LimitRegister
    >>> from musiclang.library import *
    >>> melody = s0 + s1.o(1)
    >>> LimitRangeMelody(s0, s0.o(1))(melody)
    s0 + s1
    """
    def __init__(self, note_min, note_max):
        self.note_min = note_min
        self.note_max = note_max

        if self.pitch_max - self.pitch_min < 7:
            raise ValueError('There should be a span of at least one octave for the limiter')

    @property
    def pitch_min(self):
        return self.note_min.scale_pitch

    @property
    def pitch_max(self):
        return self.note_max.scale_pitch

    def limit(self, note):
        sp = note.scale_pitch
        if sp > self.pitch_max:
            return self.limit(note.o(-1))
        elif sp < self.pitch_min:
            return self.limit(note.o(1))
        else:
            return note.copy()

    def action(self, note, **kwargs):
        return self.limit(note)


class ApplySilence(NoteTransformer):
    """
    Transform all notes into a Silence

    """
    def action(self, element, **kwargs):
        from musiclang import Silence
        return Silence(element.duration)


class ApplyContinuation(NoteTransformer):
    def action(self, element, **kwargs):
        from musiclang import Continuation
        return Continuation(element.duration)


class Repeat(NoteTransformer):
    """
    Transform all notes into a Continuation
    """
    def __init__(self, n):
        self.n = n

    def action(self, note, **kwargs):
        return note * self.n


class TransposeDiatonic(NoteTransformer):
    """
    Transpose a note diatonically
    """
    def __init__(self, n, keep_mode=True, keep_accident=False):
        """

        Parameters
        ----------
        n: int
           Number of diatonic steps for transposition
        keep_mode: boolean, default=True
                   If false the transposed notes will lose it's mode
        keep_accident: boolean, default=False
                   If false the transposed notes will lose it's accident
        """
        self.n = n
        self.keep_mode = keep_mode
        self.keep_accident = keep_accident

    def action(self, note, chord=None, **kwargs):
        if note.type in ['s']:
            new_note = note.copy()
            new_note.type = 's'
            new_note.val += self.n
            if not self.keep_mode:
                new_note.mode = None
            elif not self.keep_accident:
                new_note.accident = None
            return new_note
        elif note.is_relative:
            return note.copy()

        elif note.type == 'h':
            from musiclang.write.constants import DEGREE_TO_SCALE_DEGREE
            new_val = DEGREE_TO_SCALE_DEGREE[note.val]
            new_note = note.copy()
            new_note.type = 's'
            new_note.val = new_val
            return new_note


class TransposeChromatic(NoteTransformer):
    """
    Transpose a note chromatically.
    Should be called on at least a chord
    """
    def __init__(self, n):
        self.n = n

    def action(self, note, chord=None, **kwargs):
        if note.is_relative:
            return note.copy()

        dict_pitches = chord.pitch_dict
        pitch = chord.to_pitch(note)
        ref_note = dict_pitches[(pitch + self.n) % 12].o((pitch + self.n)//12)
        new_note = note.copy()
        new_note.val = ref_note.val
        new_note.type = ref_note.type
        new_note.octave = ref_note.octave
        new_note.accident = None
        new_note.mode = None

        return new_note