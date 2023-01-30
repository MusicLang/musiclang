from musiclang import Melody
from musiclang.transform import MelodyTransformer
from musiclang.transform.composing.project import project_on_rhythm


class CircularPermutationMelody(MelodyTransformer):
    """
    Circular permut the melody by a factor n

    Can be called with a melody, a score or a chord

    Examples
    --------

    >>> from musiclang.transform.library import CircularPermutationMelody
    >>> from musiclang.library import *
    >>> melody = s0 + s1 + s2
    >>> CircularPermutationMelody(1)(melody)
    s1 + s2 + s0

    >>> from musiclang.transform.library import CircularPermutationMelody
    >>> from musiclang.library import *
    >>> melody = (I % I.M)(s0 + s1, s1 + s2)
    >>> CircularPermutationMelody(1)(melody)
    (I % I.M)(s1 + s0, s2 + s1)

    """
    def __init__(self, n, **kwargs):
        """

        :param n: Number of delays of
        :param kwargs:
        """
        self.n = n

    def action(self, melody: Melody, **kwargs):
        new_melody = melody.copy()
        notes = [melody.notes[(idx + self.n) % len(melody.notes)] for idx, note in enumerate(melody.notes)]
        new_melody.notes = notes

        return new_melody


class ReverseMelody(MelodyTransformer):
    """
    Reverse the current melody (first note is last etc ...)

    Can be called with a melody, a score or a chord.

    Examples
    --------

    >>> from musiclang.transform.library import ReverseMelody
    >>> from musiclang.library import *
    >>> melody = s0 + s1 + s2
    >>> ReverseMelody(1)(melody)
    s2 + s1 + s0

    >>> from musiclang.transform.library import ReverseMelody
    >>> from musiclang.library import *
    >>> melody = (I % I.M)(s0 + s1, s1 + s2)
    >>> ReverseMelody(1)(melody)
    (I % I.M)(s1 + s0, s2 + s1)


    """

    def action(self, melody, **kwargs):
        return Melody(melody.notes[::-1], tags=melody.tags)


class ReverseMelodyWithoutRhythm(MelodyTransformer):
    """
    Reverse the notes of a melody

    Can be called with a melody, a score or a chord.

    Examples
    --------

    >>> from musiclang.transform.library import ReverseMelodyWithoutRhythm
    >>> from musiclang.library import *
    >>> melody = s0 + s1 + s2.e
    >>> ReverseMelodyWithoutRythm()(melody)
    s2 + s1 + s0.e

    >>> from musiclang.transform.library import ReverseMelodyWithoutRhythm
    >>> from musiclang.library import *
    >>> melody = (I % I.M)(s0 + s1.e, s1 + s2.e)
    >>> ReverseMelodyWithoutRythm()(melody)
    (I % I.M)(s1 + s0.e, s2 + s1.e)
    """

    def action(self, melody, **kwargs):
        return project_on_rhythm(melody, Melody(melody.notes[::-1], tags=melody.tags))


class InvertMelody(MelodyTransformer):
    """
    Invert the melody from the first note of the melody

    Can be called with a melody, a score or a chord.

    Examples
    --------

    >>> from musiclang.transform.library import InvertMelody
    >>> from musiclang.library import *
    >>> melody = s0 + s1 + s2.e
    >>> InvertMelody()(melody)
    s2 + s6.o(-1) + s5.o(-1).e

    >>> from musiclang.transform.library import InvertMelody
    >>> from musiclang.library import *
    >>> melody = (I % I.M)(s0 + s1.e, s1 + s2.e)
    >>> InvertMelody()(melody)
    (I % I.M)(s0 + s6.o(-1).e, s1 + s0.e)
    """

    def action(self, melody, **kwargs):
        first_val = melody.notes[0].val
        return Melody([n.set_val(2 * first_val - n.val) for n in melody.notes], tags=melody.tags)


class SelectRangeMelody(MelodyTransformer):
    """
    Get the sub-melody from time start and time end.

    Can be called with a melody, a chord or a score (in which case it will be applied chord per chord).

    Examples
    --------

    >>> from musiclang.transform.library import SelectRangeMelody
    >>> from musiclang.library import *
    >>> melody = s0 + s1 + s2.e
    >>> SelectRangeMelody(0, 1)(melody)
    s0

    >>> from musiclang.transform.library import SelectRangeMelody
    >>> from musiclang.library import *
    >>> melody = (I % I.M)(s0 + s1.e + s2) + (I % I.M)(s0 + s1.e + s2)
    >>> SelectRangeMelody(0, 2)(melody)
    (I % I.M)(piano__0=s0 + s1.e + s2.e) + (I % I.M)(piano__0=s0 + s1.e + s2.e)
    """
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    def action(self, melody, **kwargs):
        from musiclang.write.time_utils import get_score_between
        from musiclang.library import I
        # Get melody between ...
        return get_score_between(None + (I % I.M)(piano__0=melody), start=self.start, end=self.end)[0].score['piano__0']

