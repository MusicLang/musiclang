from musiclang.write.constants import *
from fractions import Fraction as frac
from .utils_metric import bjorklund_algorithm


class Metric:
    """
    A class to handle the metric of a song.
    It is composed of a binary array of 0 and 1, a signature, a tatum (smallest beat) and a number of bars
    The array specifies which tatum which be played in the specific metric

    Examples
    --------
    >>> from musiclang.library import Q, s0
    >>> metric = Metric([1, 0, 0, 1], signature=(4, 4), tatum=Q)
    >>> metric.apply_to_melody([s0, s1])
    s0.hd + s1
    """

    STRONG = "STRONG"
    WEAK = "WEAK"
    SYNCOPATION = "SYNCOPATION"
    SIGNATURES = [(4, 4), (3, 4), (2, 4), (6, 4), (3, 8), (6, 8), (9, 8), (12, 8), (2, 2)]

    def __init__(self, array, signature, tatum=S, nb_bars=1):

        if signature not in Metric.SIGNATURES:
            raise ValueError('Signature is not standard, please use a composite metric')

        self.signature = signature
        self.tatum = tatum
        if isinstance(self.tatum, (tuple, list)):
            self.tatum = frac(*self.tatum)
        self.nb_bars = nb_bars
        self.array = array
        if (self.duration / self.tatum) != len(array):
            raise ValueError('Array size is incompatible with signature and tatum')

    @property
    def nb_notes(self):
        return sum(self.array)

    @property
    def duration(self):
        nom, den = self.signature
        return self.nb_bars * nom * frac(4, den)

    @property
    def bar_duration(self):
        nom, den = self.signature
        return nom * frac(4, den)

    def get_beat_durations(self, array=None):
        if array is None:
            array = self.array
        first_has_note = array[0] == 1
        result = []
        curr_dur = self.tatum
        is_note = first_has_note
        for b in array[1:]:
            if b == 0:
                curr_dur += self.tatum
            elif b == 1:
                result.append((is_note, curr_dur))
                curr_dur = self.tatum
                is_note = True
            else:
                result.append((is_note, curr_dur))
                curr_dur = self.tatum
                is_note = False

        result.append((is_note, curr_dur))

        return result, first_has_note

    def beat_type(self, time):
        """
        Return "STRONG" if the beat is a strong beat
        "WEAK" if weak beat and "SYNCOPATION" otherwise

        Parameters
        ----------
        time

        Returns
        -------

        """
        time = time % self.bar_duration
        if time < 0 or time > self.duration:
            raise ValueError('Time should be between 0 and bar duration')

        if time / self.tatum != int(time / self.tatum):
            return Metric.SYNCOPATION

        if time == 0:
            return Metric.STRONG

        if self.signature in [(4, 4), (2, 2), (2, 4), (6, 4)]:
            return Metric.STRONG if (time % 2) == 0 else Metric.WEAK
        elif self.signature in [(3, 4), (3, 8)]:
            return Metric.STRONG if time == 0 else Metric.WEAK
        elif self.signature in [(3, 8), (2, 8), (1, 8)]:
            return Metric.WEAK
        elif self.signature in [(6, 8), (9, 8), (12, 8)]:
            return Metric.STRONG if (time % frac(3, 2)) == 0 else Metric.WEAK


    @classmethod
    def Euclidian(cls, pulses, signature, tatum, nb_bars=1):
        """
        Following this paper : The Euclidean Algorithm Generates Traditional Musical Rhythms
        http://cgm.cs.mcgill.ca/~godfried/publications/banff.pdf

        Parameters
        ----------
        pulses: Number of pulses in the bar
        signature:
        tatum:

        Returns
        -------
        metric: Metric
                Resulting metric of the song
        """

        steps = cls._nb_steps(signature, tatum, nb_bars)
        return Metric(bjorklund_algorithm(steps, pulses), signature, tatum, nb_bars=nb_bars)




    @classmethod
    def _nb_steps(self, signature, tatum, nb_bars):
        nb_base, den = signature
        base = frac(4, den)
        duration = nb_base * base
        steps = int(nb_bars * frac(duration, tatum))
        return steps

    def euclidian(self, pulses):
        """
        Change the array of this specific metric using Metric.Euclidian
        Following this paper : The Euclidean Algorithm Generates Traditional Musical Rhythms
        http://cgm.cs.mcgill.ca/~godfried/publications/banff.pdf

        Parameters
        ----------
        pulses: Number of pulses in the bar

        Returns
        -------
        metric: Metric

        """
        return Metric.Euclidian(pulses, signature=self.signature, tatum=self.tatum, nb_bars=self.nb_bars)

    @classmethod
    def Full(cls, signature, tatum, nb_bars=1):
        """
        Create a metric with a pulse on each tatum (An array full of 1)

        Parameters
        ----------
        signature: tuple (len == 2)
        tatum: Fraction

        Returns
        -------
        metric: Metric
                Resulting metric of the song
        """

        steps = cls._nb_steps(signature, tatum, nb_bars)
        return Metric([1 for _ in range(steps)], signature, tatum, nb_bars=nb_bars)

    def full(self):
        return Metric.Full(signature=self.signature, tatum=self.tatum, nb_bars=self.nb_bars)

    @classmethod
    def Alternating(cls, n, signature, tatum, nb_bars=1):
        """
        Create an alternating metric with a pulse each n tatum

        Parameters
        ----------
        signature: tuple (len == 2)
        tatum: Fraction

        Returns
        -------
        metric: Metric
                Resulting metric of the song
        """

        steps = cls._nb_steps(signature, tatum, nb_bars)
        return Metric([1 if (a % n) == 0 else 0 for a in range(steps)], signature, tatum, nb_bars=nb_bars)

    def alternating(self, n):
        return Metric.Alternating(n, signature=self.signature, tatum=self.tatum, nb_bars=self.nb_bars)

    def apply_to_score(self, score):
        """
        Apply the rythm to a given score
        Parameters
        ----------
        score

        Returns
        -------

        """
        pass


    def get_array_between(self, start, end):
        if start is None:
            start = 0
        if end is None:
            end = self.duration
        idx_start = start // self.tatum
        idx_end = end // self.tatum
        return [self.array[idx % len(self.array)] for idx in range(idx_start, idx_end)], start, end

    def apply_to_melody(self, melody, expand=True, start=None, end=None):
        """
        Apply the metric to a given melody.
        If expand is True, the notes of the melody will be used circularly until metric duration is satisfied
        Else if the melody has not enough notes it will add silences

        Parameters
        ----------
        melody: Melody
        expand: boolean, default = True

        Returns
        -------
        melody: Melody

        """
        from musiclang import Note, Melody, Silence
        if isinstance(melody, Note):
            notes = [melody.copy()]
        elif isinstance(melody, (list, tuple)):
            notes = melody
        else:
            notes = melody.notes

        array, start, end = self.get_array_between(start, end)
        if not expand and len(notes) < sum(array):
            notes += [Silence(1)] * (sum(array) - len(notes))

        beat_durations, first_has_note = self.get_beat_durations(array)
        result = self._apply_durations_to_melody(notes, beat_durations, first_has_note=first_has_note, expand=expand)
        if result.duration > (end - start):
            # It means the duration of the chord is not divisible by tatum, must shorter the last note
            delta_tatum = (end - start) % self.tatum
            before = result.copy()
            result.notes[-1] = result.notes[-1].set_duration(result.notes[-1].duration - delta_tatum)
            assert result.duration == (end - start), f'{result.duration} {end - start} {delta_tatum} {result} {before}'

        elif result.duration < (end - start):
            delta_tatum = (end - start) % self.tatum
            result.notes[-1] = result.notes[-1].set_duration(result.notes[-1].duration + delta_tatum)

        return result

    @classmethod
    def _apply_durations_to_melody(cls, notes, beat_durations, first_has_note=True, expand=True):
        from musiclang import Silence, Continuation
        melody = []
        for idx, (has_note, beat) in enumerate(beat_durations):
            if idx == 0 and not first_has_note:
                melody.append(Silence(1).set_duration(beat))
            elif not expand and idx > len(notes):
                break
            elif has_note:
                melody.append(notes[idx % len(notes)].set_duration(beat))
            else:
                melody.append(Silence(1).set_duration(beat))

        from musiclang import Melody
        return Melody(melody)

    def complementary(self):
        """
        Get the complementary rhythm of a given rhythm
        eg : Complementary of [1, 0, 0, 0] = [0, 1, 1, 1]
        Keep the same tatum, nb_bars and signature

        Returns
        -------
        metric: Metric
        """
        return Metric([1 - a for a in self.array], signature=self.signature, tatum=self.tatum, nb_bars=self.nb_bars)

    def reversed(self):
        """
        Get the reversed rhythm of a given rhythm
        eg : Reverse of [1, 0, 0, 0] = [0, 0, 0, 1]
        Keep the same tatum, nb_bars and signature

        Returns
        -------
        metric: Metric
        """
        return Metric(self.array[::-1], signature=self.signature, tatum=self.tatum, nb_bars=self.nb_bars)

    def circular_shift(self, n):
        """
        Get the shifted rhythm of a given rhythm by tatum value
        eg : circular_shift(2) of [1, 0, 0, 0] = [0, 0, 1, 0]
        Keep the same tatum, nb_bars and signature

        Returns
        -------
        metric: Metric
        """
        return Metric(self.array[(-n % len(self.array)):] + self.array[:(-n % len(self.array))],
                      signature=self.signature, tatum=self.tatum, nb_bars=self.nb_bars)

    def canon(self, n):
        """
        Get the shifted rhythm of a given rhythm by tatum value, cut the end to fit the metric.
        eg : canon(2) of [1, 0, 0, 0] = [0, 0, 1, 0]
        Keep the same tatum, nb_bars and signature

        Returns
        -------
        metric: Metric
        """
        array_mask = ([0] * n) + ([1] * (len(self.array) - n))
        return Metric(self.array[(n % len(self.array)):] + self.array[:(n % len(self.array))],
                      signature=self.signature, tatum=self.tatum, nb_bars=self.nb_bars).masked(array_mask)

    @classmethod
    def FromArray(cls, array, signature=(4, 4), tatum=None, nb_bars=1):
        """
        Get a metric from a binary array, if several bar we only support constant tatum
        between bar at the time being
        Parameters
        ----------
        array: list[int]
            List of binary
        signature
        tatum
        nb_bars

        Returns
        -------

        """
        if tatum is None:
            nb_notes = len(array)
            nom, den = signature
            duration = nb_bars * nom * frac(4, den)
            tatum = duration / nb_notes
        return Metric(array, signature=signature, tatum=tatum, nb_bars=nb_bars)


    @classmethod
    def FromMelody(cls, melody, signature=(4, 4), tatum=None, nb_bars=1):
        # Get tatum
        if tatum is None:
            tatum = min([note.duration for note in melody.notes])
        array = []
        for note in melody.notes:
            nb_tatums = note.duration / tatum
            if nb_tatums != int(nb_tatums):
                raise ValueError('Could not find a tatum to determine the metric, use a composite rhythm')
            nb_tatums = int(nb_tatums)

            if note.is_note:
                array += [1] + [0] * (nb_tatums - 1)
            else:
                array += [0] + [0] * (nb_tatums - 1)

        if len(array) // nb_bars != len(array) // nb_bars:
            raise ValueError('Nb bars does not divide the metric array')

        return Metric(array, signature=signature, tatum=tatum, nb_bars=nb_bars)

    def from_melody(self, melody):
        return Metric.FromMelody(melody, signature=self.signature, tatum=self.tatum, nb_bars=self.nb_bars)

    def is_note_playing(self, time):
        idx = time / self.tatum
        if idx != int(idx):
            return False
        else:
            return self.array[idx] == 1

    def project(self, melody):
        """
        Project a melody in the given metric

        Parameters
        ----------
        melody: Melody

        Returns
        -------
        melody: Melody
                Filtered melody

        """
        from musiclang import Note
        from musiclang.transform.composing.project import project_on_rhythm
        rhythm = self.apply_to_melody(Note(0, 0, 0, 1))
        projected_melody = project_on_rhythm(rhythm, melody)
        return projected_melody

    def masked(self, mask):
        """
        Get the masked rhythm of a given rhythm by tatum value
        eg : Mask of [1, 0, 1, 0] with [1, 0, 0, 0] is [1, 0, 0, 0]

        Parameters
        ---------
        mask : Metric | list[int]
               Mask to apply to the rhythm
        Returns
        -------
        metric: Metric
        """
        if isinstance(mask, Metric):
            mask = mask.array

        return Metric([e1 * e2 for e1, e2 in zip(self.array, mask)], signature=self.signature,
                      tatum=self.tatum, nb_bars=self.nb_bars)

    def add(self, mask):
        """
        Add to rhythm together
        eg : Mask of [1, 0, 1, 0] with [1, 0, 0, 0] is [1, 0, 0, 0]

        Parameters
        ---------
        mask : Metric | list[int]
               Mask to apply to the rhythm
        Returns
        -------
        metric: Metric
        """
        if isinstance(mask, Metric):
            mask = mask.array

        return Metric([max(e1, e2) for e1, e2 in zip(self.array, mask)], signature=self.signature,
                      tatum=self.tatum, nb_bars=self.nb_bars)


class CompositeMetric:

    def __init__(self, metrics):
        self.metrics = metrics

    def apply_to_melody(self, melody, expand=True):

        from musiclang import Note, Melody, Silence
        if isinstance(melody, Note):
            melody = Melody([melody.copy()])
        elif isinstance(melody, (list, tuple)):
            melody = Melody(melody).copy()

        notes = melody.notes
        durations = sum([m.get_beat_durations()[0] for m in self.metrics], [])
        return Metric.apply_durations_to_melody(notes, durations, expand=expand)

    def masked(self, masks):
        if isinstance(masks, Metric):
            masks = []
        return CompositeMetric([metric.masked(mask) for mask, metric in zip(masks, self.metrics)])

    def canon(self, masks):
        raise NotImplemented()