class Mask:
    """
    Class responsible to make a masked query on a score.
    A Mask can check if a query is true on a given element (score, chord, note, melody)
    and give a subquery that can be used on a child of the element (Mask.child).
    It is used internally by the Transform, Filter classes to either apply a transformation
    on a filter of a score or filter a score directly.

    Examples
    --------

    A mask that checks if a chord has a tag "label"
    >>> from musiclang.library import *
    >>> from musiclang.transform import Mask
    >>> mask = Mask.Chord() > Mask.Has("label")
    >>> mask((I % I.M).add_tag('label'))
    True

    """
    def __call__(self, element, **kwargs):
        return True

    @classmethod
    def eval(cls, query):
        # Add to the namespace
        has = Mask.Has
        has_at_least = Mask.HasAtLeast
        instruments = Mask.InstrumentIn
        Score = Mask.Score()
        Melody = Mask.Melody()
        Note = Mask.Note()
        Chord = Mask.Chord()
        true = Mask.True_()
        false = Mask.False_()
        query = eval(query)
        return query

    def child(self, element, **kwargs):
        return self

    # Note masks

    @classmethod
    def NoteIn(cls, notes, ignore_octave=False, ignore_rythm=False):
        return cls.Note() > NoteInMask(notes, ignore_octave=ignore_octave, ignore_rythm=ignore_rythm)

    @classmethod
    def BeatIn(cls, beats):
        return cls.Note() > BeatInMask(beats)

    @classmethod
    def BeatPlayingIn(cls, beats):
        return cls.Note() > BeatPlayingInMask(beats)

    @classmethod
    def DurationIn(cls, durations):
        return cls.Note() > DurationInMask(durations)


    @classmethod
    def BeatBetween(cls, start, end):
        return cls.Note() > BeatBetweenMask(start, end)


    @classmethod
    def DurationBetween(cls, start, end):
        return cls.Note() > DurationBetweenMask(start, end)

    # Melodic masks

    @classmethod
    def InstrumentIn(cls, instruments):
        return cls.Melody() > InstrumentsMask(instruments)

    # Chord And Tonality masks

    @classmethod
    def ChordBeatIn(cls, beats):
        return cls.Chord() > ChordBeatInMask(beats)

    @classmethod
    def ChordBeatPlayingIn(cls, beats):
        return cls.Chord() > ChordBeatPlayingInMask(beats)

    @classmethod
    def ChordDurationIn(cls, durations):
        return cls.Chord() > ChordDurationInMask(durations)

    @classmethod
    def ChordBeatBetween(cls, start, end):
        return cls.Chord() > ChordBeatBetweenMask(start, end)

    @classmethod
    def ChordDurationBetween(cls, start, end):
        return cls.Chord() > ChordDurationBetweenMask(start, end)

    @classmethod
    def ModeIn(cls, modes):
        return cls.Chord() > ModeInMask(modes)

    @classmethod
    def ChordDegreeIn(cls, chord_degrees):
        return cls.Chord() > ChordDegreeInMask(chord_degrees)

    @classmethod
    def ChordExtensionIn(cls, chord_degrees):
        return cls.Chord() > ChordExtensionInMask(chord_degrees)

    @classmethod
    def TonalityDegreeIn(cls, tonality_degrees):
        return cls.Chord() > TonalityDegreeInMask(tonality_degrees)

    @classmethod
    def ChordIn(cls, chords, ignore_octave=False):
        return cls.Chord() > ChordInMask(chords, ignore_octave=ignore_octave)

    @classmethod
    def TonalityIn(cls, tonalities, ignore_octave=False):
        return cls.Chord() > TonalityInMask(tonalities, ignore_octave=ignore_octave)


    # First order logic masks

    @classmethod
    def HasAtLeast(cls, tags):
        """
        Check if an element has at least these tags

        Parameters
        ----------
        tags: iterable[str] or str

        """
        return HasAtLeastMask(tags)


    @classmethod
    def OriginateFrom(cls, tags):
        """
        Check if a chord originate from a set of given pipeline step or one pipeline step

        Parameters
        ----------
        tags: iterable[str] or str

        """

        return cls.Chord() > HasMask([f'step_{tag}' for tag in tags])

    @classmethod
    def Has(cls, tags):
        """
        Check if an element has these tags (all of them)

        Parameters
        ----------
        tags: iterable[str] or str

        """

        return HasMask(tags)

    @classmethod
    def And(cls, masks):
        """
        Logical and between masks. You can also use the "&" python operator between masks

        Parameters
        ----------
        masks: iterable[Mask]

        """

        return AndMask(masks)

    @classmethod
    def Bool(cls, bool):
        """
        A mask that always returns bool when called

        Parameters
        ----------
        bool: boolean

        """

        return BoolMask(bool)

    @classmethod
    def True_(cls):
        """
        A mask that always returns True when called
        """

        return BoolMask(True)

    @classmethod
    def False_(cls):
        """
        A mask that always returns False when called
        """
        return BoolMask(False)

    @classmethod
    def Or(cls, tags):
        """
        Logical or between masks. You can also use the "&" python operator between masks

        Parameters
        ----------
        masks: iterable[Mask]

        """
        return OrMask(tags)

    @classmethod
    def Score(cls):
        """
        A Mask that will only apply to score. Usually used with another mask with the ">" operator

        Examples
        --------
        >>> from musiclang.transform import Mask
        >>> mask = Mask.Score() > Mask.Has("label")
        """

        return ScoreMask()

    @classmethod
    def Melody(cls):
        """
        A Mask that will only apply to a melody. Usually used with another mask with the ">" operator

        Examples
        --------
        Check if tag label in this melody :

        >>> from musiclang.transform import Mask
        >>> mask = Mask.Melody() > Mask.Has("label")
        """
        return MelodyMask()

    @classmethod
    def Note(cls):
        """
        A Mask that will only apply to a note. Usually used with another mask with the ">" operator

        Examples
        --------
        Check if tag label in this note :

        >>> from musiclang.transform import Mask
        >>> mask = Mask.Note() > Mask.Has("label")
        """

        return NoteMask()

    @classmethod
    def Chord(cls):
        """
        A Mask that will only apply to a chord. Usually used with another mask with the ">" operator

        Examples
        --------
        Check if tag label in this Chord :

        >>> from musiclang.transform import Mask
        >>> mask = Mask.Chord() > Mask.Has("label")
        """

        return ChordMask()

    @classmethod
    def Func(cls, f):
        """
        A mask that will apply a custom function. The function should have signature (element, **kwargs) -> bool
        """

        return FuncMask(f)

    def __and__(self, other):
        return AndMask([self, other])

    def __or__(self, other):
        return OrMask([self, other])

    def __invert__(self):
        return NotMask(self)

    def __repr__(self):
        return 'true'



class NoteInMask(Mask):

    def __init__(self, notes, ignore_octave=False, ignore_rythm=False):
        from musiclang import Note
        if isinstance(notes, Note):
            notes = {notes}

        self.notes = set(notes)
        self.ignore_octave = ignore_octave
        self.ignore_rythm = ignore_rythm
        if self.ignore_octave:
            self.notes = [c.o(-c.octave) for c in self.notes]
        if self.ignore_rythm:
            self.notes = [c.set_duration(1) for c in self.notes]

    def __call__(self, note, **kwargs):
        n = note
        if self.ignore_octave:
            n = n.o(-note.octave)
        if self.ignore_rythm:
            n = n.set_duration(1)
        return n in self.notes

    def __repr__(self):
        return f'note_in({self.notes}, {self.ignore_octave}, {self.ignore_rythm})'


class BeatInMask(Mask):

    def __init__(self, beats):
        from fractions import Fraction
        if isinstance(beats, (int, Fraction)):
            beats = {beats}
        self.beats = set(beats)

    def __call__(self, note, beat=0, **kwargs):
        return beat in self.beats

    def __repr__(self):
        return f'beat_in({self.beats})'

class BeatPlayingInMask(Mask):

    def __init__(self, beats):
        from fractions import Fraction
        if isinstance(beats, (int, Fraction)):
            beats = {beats}
        self.beats = set(beats)

    def __call__(self, note, beat=0, **kwargs):
        end_beat = beat + note.duration
        return any([beat <= b < end_beat for b in self.beats])

    def __repr__(self):
        return f'beat_in({self.beats})'

class DurationInMask(Mask):

    def __init__(self, durations):
        from fractions import Fraction
        if isinstance(durations, (int, Fraction)):
            durations = {durations}
        self.durations = set(durations)

    def __call__(self, note, beat=0, **kwargs):
        return note.duration in self.durations

    def __repr__(self):
        return f'duration_in({self.durations})'


class DurationBetweenMask(Mask):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, note, beat=0, **kwargs):
        return self.start <= note.duration < self.end

    def __repr__(self):
        return f'duration_between({self.start}, {self.end})'


class BeatBetweenMask(Mask):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, note, beat=0, **kwargs):
        return self.start <= beat < self.end

    def __repr__(self):
        return f'beat_between({self.start}, {self.end})'


# Melodic



class InstrumentsMask(Mask):

    def __init__(self, instruments):
        if isinstance(instruments, str):
            instruments = {instruments}

        self.instruments = set(instruments)

    def __call__(self, element, chord=None, instrument=None, **kwargs):
        return instrument in self.instruments

    def __repr__(self):
        return f"instruments({self.instruments})"


# Chords


class ChordBeatInMask(Mask):

    def __init__(self, beats):
        from fractions import Fraction
        if isinstance(beats, (int, Fraction)):
            beats = {beats}
        self.beats = set(beats)

    def __call__(self, chord, chord_beat=0, **kwargs):
        return chord_beat in self.beats

    def __repr__(self):
        return f'chord_beat_in({self.beats})'


class ChordBeatPlayingInMask(Mask):

    def __init__(self, beats):
        from fractions import Fraction
        if isinstance(beats, (int, Fraction)):
            beats = {beats}
        self.beats = set(beats)

    def __call__(self, chord, chord_beat=0, **kwargs):
        end_beat = chord_beat + chord.duration
        return any([chord_beat <= b < end_beat for b in self.beats])

    def __repr__(self):
        return f'chord_beat_in({self.beats})'


class ChordDurationInMask(Mask):

    def __init__(self, durations):
        from fractions import Fraction
        if isinstance(durations, (int, Fraction)):
            durations = {durations}
        self.durations = set(durations)

    def __call__(self, chord, chord_beat=0, **kwargs):
        return chord.duration in self.durations

    def __repr__(self):
        return f'chord_duration_in({self.durations})'


class ChordDurationBetweenMask(Mask):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, chord, chord_beat=0, **kwargs):
        return self.start <= chord.duration < self.end

    def __repr__(self):
        return f'chord_duration_between({self.start}, {self.end})'


class ChordBeatBetweenMask(Mask):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __call__(self, chord, chord_beat=0, **kwargs):
        return self.start <= chord_beat < self.end

    def __repr__(self):
        return f'chord_beat_between({self.start}, {self.end})'


class ModeInMask(Mask):

    def __init__(self, modes):
        if isinstance(modes, str):
            modes = {modes}
        self.modes = set(modes)

    def __call__(self, element, **kwargs):
        return element.tonality.mode in self.modes

    def __repr__(self):
        return f"mode_in({self.modes})"


class ChordInMask(Mask):

    def __init__(self, chords, ignore_octave=False):
        from musiclang import Chord
        if isinstance(chords, Chord):
            chords = {chords}
        self.chords = set(chords)
        self.ignore_octave = ignore_octave
        if self.ignore_octave:
            self.chords = [c.o(-c.octave) for c in self.chords]

    def __call__(self, element, **kwargs):
        if self.ignore_octave:
            return element.o(-element.octave) in self.chords
        else:
            return element in self.chords

    def __repr__(self):
        return f"chord_in({self.chords},ignore_octave={self.ignore_octave})"


class TonalityInMask(Mask):

    def __init__(self, tonalities, ignore_octave=False):
        from musiclang import Tonality
        if isinstance(tonalities, Tonality):
            tonalities = {tonalities}
        self.tonalities = set(tonalities)
        self.ignore_octave = ignore_octave
        if self.ignore_octave:
            self.tonalities = [c.o(-c.octave) for c in self.tonalities]

    def __call__(self, element, **kwargs):
        if self.ignore_octave:
            return element.tonality.o(element.tonality.octave) in self.tonalities
        else:
            return element.tonality in self.tonalities

    def __repr__(self):
        return f"tonality_in({self.tonalities},ignore_octave={self.ignore_octave})"


class ChordDegreeInMask(Mask):

    def __init__(self, degrees):
        if isinstance(degrees, int):
            degrees = {degrees}
        self.degrees = set(degrees)

    def __call__(self, element, **kwargs):
        return element.degree in self.degrees

    def __repr__(self):
        return f"chord_degree_in({self.degrees})"


class ChordExtensionInMask(Mask):
    def __init__(self, extensions):
        if isinstance(extensions, str):
            extensions = {extensions}
        self.extensions = set(extensions)

    def __call__(self, element, **kwargs):
        return element.extension in self.extensions

    def __repr__(self):
        return f"chord_extension_in({self.extensions})"


class TonalityDegreeInMask(Mask):

    def __init__(self, degrees):
        if isinstance(degrees, int):
            degrees = {degrees}
        self.degrees = set(degrees)

    def __call__(self, element, **kwargs):
        return element.tonality.degree in self.degrees

    def __repr__(self):
        return f"tonality_degree_in({self.degrees})"




class FuncMask(Mask):

    def __init__(self, f):
        self.f = f

    def __call__(self, element, **kwargs):
        return self.f(element, **kwargs)

    def __repr__(self):
        return 'funcMask'


class HasAtLeastMask(Mask):
    def __init__(self, tags):
        if isinstance(tags, str):
            tags = {tags}
        self.tags = set(tags)

    def __call__(self, element, **kwargs):
        return len(element.tags.intersection(self.tags)) > 0

    def __repr__(self):
        return f"has_at_least({self.tags})"


class NotMask(Mask):
    def __init__(self, other):
        self.other = other

    def __call__(self, element, **kwargs):
        return not self.other(element, **kwargs)

    def __repr__(self):
        return f"~ ({self.other})"


class HasMask(Mask):
    def __init__(self, tags):
        if isinstance(tags, str):
            tags = {tags}
        self.tags = set(tags)

    def __call__(self, element, **kwargs):
        return element.tags.issuperset(self.tags)

    def __repr__(self):
        return f"has({self.tags})"

    def __invert__(self):
        return NotMask(self)


class AndMask(Mask):
    def __init__(self, terms):
        self.terms = terms

    def child(self, element, **kwargs):
        return self.__class__([t.child(element, **kwargs) for t in self.terms])

    def __call__(self, element, **kwargs):
        return all((t(element, **kwargs) for t in self.terms))

    def __repr__(self):
        return " & ".join([f"({term})" for term in self.terms])

    def __invert__(self):
        return OrMask([~m for m in self.terms])


class OrMask(Mask):
    def __init__(self, terms):
        self.terms = terms

    def child(self, element, **kwargs):
        return self.__class__([t.child(element, **kwargs) for t in self.terms])

    def __call__(self, element, **kwargs):
        return any((t(element, **kwargs) for t in self.terms))

    def __repr__(self):
        return " | ".join([f"({term})" for term in self.terms])

    def __invert__(self):
        return AndMask([~m for m in self.terms])


class BoolMask(Mask):

    def __init__(self, bool):
        self.bool = bool

    def __repr__(self):
        return f"{str(self.bool).lower()}"

    def __call__(self, element, **kwargs):
        return self.bool

    def __invert__(self):
        return BoolMask(not self.bool)


class FalseMask(Mask):

    def __call__(self, element, **kwargs):
        return False

    def __repr__(self):
        return "false"

    def __invert__(self):
        return BoolMask(True)


class TrueMask(Mask):

    def __call__(self, element, **kwargs):
        return True

    def __repr__(self):
        return "true"

    def __invert__(self):
        return BoolMask(False)


class GtMask(Mask):

    def __init__(self, terms):
        self.terms = terms

    def child(self, element, **kwargs):
        return self if self.terms[0](element, **kwargs) else BoolMask(self(element, **kwargs))

    def __call__(self, element, **kwargs):
        return self.terms[0](element, **kwargs) or self.terms[1](element, **kwargs)

    def __repr__(self):
        return " > ".join([f"({term})" for term in self.terms])

    def __invert__(self):
        return GtMask([self.terms[0], ~self.terms[1]])


class TypeMask(Mask):

    def __gt__(self, other):
        return GtMask([self, other])


class ScoreMask(TypeMask):

    def __call__(self, element, **kwargs):
        from musiclang import Score
        return not isinstance(element, Score)

    def __repr__(self):
        return "Score"

    def __invert__(self):
        return self


class MelodyMask(TypeMask):

    def __call__(self, element, **kwargs):
        from musiclang import Melody
        return not isinstance(element, Melody)

    def __repr__(self):
        return "Melody"

    def __invert__(self):
        return self


class ChordMask(TypeMask):
    def __call__(self, element, **kwargs):
        from musiclang import Chord
        return not isinstance(element, Chord)

    def __repr__(self):
        return "Chord"

    def __invert__(self):
        return self


class NoteMask(TypeMask):
    def __call__(self, element, **kwargs):
        from musiclang import Note
        return not isinstance(element, Note)

    def __repr__(self):
        return "Note"

    def __invert__(self):
        return self


