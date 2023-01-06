"""Tonal representations used as inputs to the network."""

import numpy as np
import re

from .cache import (
    TransposePitch,
    m21Pitch,
    m21IntervalStr,
)
from .feature_representation import (
    INTERVALCLASSES,
    NOTEDURATIONS,
    NOTENAMES,
    PITCHCLASSES,
    SPELLINGS,
    FeatureRepresentation,
    FeatureRepresentationTI,
)


class MeasureOnset7(FeatureRepresentationTI):
    """ """
    features = len(NOTEDURATIONS)
    pattern = [list(reversed(f"{x:06b}0")) for x in range(64)]
    pattern = [[int(n) for n in arr] for arr in pattern]
    pattern[0][0] = 1

    def run(self, transposition=None):
        """

        Parameters
        ----------
        transposition :
             (Default value = None)

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        prev_measure = -1
        idx = 0
        for frame, measure in enumerate(self.df.s_measure):
            if measure != prev_measure:
                idx = 0
                prev_measure = measure
            pattern = self.pattern[idx]
            array[frame] = pattern
            idx = min(idx + 1, len(self.pattern) - 1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            measureOnset = [NOTEDURATIONS[x] for x in np.nonzero(manyhot)[0]]
            ret.append(measureOnset)
        return ret


class NoteOnset7(MeasureOnset7):
    """ """
    def run(self, transposition=None):
        """

        Parameters
        ----------
        transposition :
             (Default value = None)

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        idx = 0
        for frame, onset in enumerate(self.df.s_isOnset):
            if sum(onset) > 0:
                idx = 0
            pattern = self.pattern[idx]
            array[frame] = pattern
            idx = min(idx + 1, len(self.pattern) - 1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            noteOnset = [NOTEDURATIONS[x] for x in np.nonzero(manyhot)[0]]
            ret.append(noteOnset)
        return ret


class MeasureNoteOnset14(FeatureRepresentationTI):
    """ """
    features = MeasureOnset7.features + NoteOnset7.features
    pattern = MeasureOnset7.pattern

    def run(self, transposition=None):
        """

        Parameters
        ----------
        transposition :
             (Default value = None)

        Returns
        -------

        """
        self.measure7 = MeasureOnset7(self.df).run(transposition)
        self.note7 = NoteOnset7(self.df).run(transposition)
        array = np.concatenate((self.measure7, self.note7), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        measure7 = MeasureOnset7.decode(array[:, : MeasureOnset7.features])
        note7 = NoteOnset7.decode(array[:, MeasureOnset7.features :])
        return [(tuple(mm), tuple(n)) for mm, n in zip(measure7, note7)]


class Bass12(FeatureRepresentation):
    """ """
    features = len(PITCHCLASSES)

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            bass = notes[0]
            transposed = TransposePitch(bass, transposition)
            pitchObj = m21Pitch(transposed)
            pitchClass = pitchObj.pitchClass
            array[frame, pitchClass] = 1
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            bassPitchClass = np.argmax(manyhot)
            ret.append(bassPitchClass)
        return ret


class Bass7(FeatureRepresentation):
    """ """
    features = len(NOTENAMES)

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            bass = notes[0]
            transposed = TransposePitch(bass, transposition)
            pitchObj = m21Pitch(transposed)
            pitchLetter = pitchObj.step
            pitchLetterIndex = NOTENAMES.index(pitchLetter)
            array[frame, pitchLetterIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            bassPitchName = NOTENAMES[np.argmax(manyhot)]
            ret.append(bassPitchName)
        return ret


class Bass19(FeatureRepresentation):
    """ """
    features = Bass12.features + Bass7.features

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        self.letter = Bass7(self.df).run(transposition)
        self.pc = Bass12(self.df).run(transposition)
        array = np.concatenate((self.letter, self.pc), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        letters = Bass7.decode(array[:, : Bass7.features])
        pcs = Bass12.decode(array[:, Bass7.features :])
        return [(l, pc) for l, pc in zip(letters, pcs)]


class Chromagram12(FeatureRepresentation):
    """ """
    features = len(PITCHCLASSES)

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            for note in notes:
                transposedNote = TransposePitch(note, transposition)
                pitchObj = m21Pitch(transposedNote)
                pitchClass = pitchObj.pitchClass
                array[frame, pitchClass] = 1
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            chromagramPitchClasses = np.nonzero(manyhot)[0].tolist()
            ret.append(tuple(chromagramPitchClasses))
        return ret


class Chromagram7(FeatureRepresentation):
    """ """
    features = len(NOTENAMES)

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            for note in notes:
                transposedNote = TransposePitch(note, transposition)
                pitchObj = m21Pitch(transposedNote)
                pitchLetter = pitchObj.step
                pitchLetterIndex = NOTENAMES.index(pitchLetter)
                array[frame, pitchLetterIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            pitchNames = [NOTENAMES[x] for x in np.nonzero(manyhot)[0]]
            ret.append(tuple(pitchNames))
        return ret


class Chromagram19(FeatureRepresentation):
    """ """
    features = Chromagram12.features + Chromagram7.features

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        self.letter = Chromagram7(self.df).run(transposition)
        self.pc = Chromagram12(self.df).run(transposition)
        array = np.concatenate((self.letter, self.pc), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        letters = Chromagram7.decode(array[:, : Chromagram7.features])
        pcs = Chromagram12.decode(array[:, Chromagram7.features :])
        return [(l, pc) for l, pc in zip(letters, pcs)]


class Intervals19(FeatureRepresentationTI):
    """ """
    features = len(NOTENAMES) + len(PITCHCLASSES)

    def run(self):
        """ """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, intervals in enumerate(self.df.s_intervals):
            for interval in intervals:
                intervalObj = m21IntervalStr(interval)
                chromatic = intervalObj.chromatic.mod12
                genericClass = intervalObj.generic.simpleUndirected - 1
                array[frame, genericClass] = 1
                array[frame, chromatic + len(NOTENAMES)] = 1
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            generics = (np.nonzero(manyhot[:7])[0] + 1).tolist()
            chromatics = np.nonzero(manyhot[7:])[0].tolist()
            ret.append((tuple(generics), tuple(chromatics)))
        return ret


class Intervals39(FeatureRepresentationTI):
    """ """
    features = len(INTERVALCLASSES)

    def run(self):
        """ """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, intervals in enumerate(self.df.s_intervals):
            for interval in intervals:
                intervalIndex = INTERVALCLASSES.index(interval)
                array[frame, intervalIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != cls.features:
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            intervals = [INTERVALCLASSES[x] for x in np.nonzero(manyhot)[0]]
            ret.append(tuple(intervals))
        return ret


class Bass35(FeatureRepresentation):
    """ """
    features = len(SPELLINGS)

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            bass = re.sub(r"\d", "", notes[0])
            transposed = TransposePitch(bass, transposition)
            if transposed in SPELLINGS:
                spellingIndex = SPELLINGS.index(transposed)
                array[frame, spellingIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != len(SPELLINGS):
            raise IndexError("Strange array shape.")
        return [SPELLINGS[np.argmax(onehot)] for onehot in array]


class Chromagram35(FeatureRepresentation):
    """ """
    features = len(SPELLINGS)

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, notes in enumerate(self.df.s_notes):
            notes = [re.sub(r"\d", "", n) for n in notes]
            for note in notes:
                transposed = TransposePitch(note, transposition)
                if transposed in SPELLINGS:
                    spellingIndex = SPELLINGS.index(transposed)
                    array[frame, spellingIndex] = 1
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != len(SPELLINGS):
            raise IndexError("Strange array shape.")
        ret = []
        for manyhot in array:
            notes = [SPELLINGS[x] for x in np.nonzero(manyhot)[0]]
            ret.append(tuple(notes))
        return ret


class BassChromagram70(FeatureRepresentation):
    """ """
    features = Bass35.features + Chromagram35.features

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        self.bass35 = Bass35(self.df).run(transposition)
        self.chromagram35 = Chromagram35(self.df).run(transposition)
        array = np.concatenate((self.bass35, self.chromagram35), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        bass35 = Bass35.decode(array[:, : Bass35.features])
        chromagram35 = Chromagram35.decode(array[:, Bass35.features :])
        return [(b, ch) for b, ch in zip(bass35, chromagram35)]


class BassChromagram38(FeatureRepresentation):
    """ """
    features = Bass19.features + Chromagram19.features

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        # super().__init__(df)
        self.bass19 = Bass19(self.df).run(transposition)
        self.chromagram19 = Chromagram19(self.df).run(transposition)
        array = np.concatenate((self.bass19, self.chromagram19), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        bass19 = Bass19.decode(array[:, : Bass19.features])
        chromagram19 = Chromagram19.decode(array[:, Bass19.features :])
        return [(b[0], b[1], c[0], c[1]) for b, c in zip(bass19, chromagram19)]


class BassIntervals58(FeatureRepresentation):
    """ """
    features = Bass19.features + Intervals39.features

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        self.bass19 = Bass19(self.df).run(transposition)
        self.intervals39 = Intervals39(self.df).run()
        array = np.concatenate((self.bass19, self.intervals39), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        bass19 = Bass19.decode(array[:, : Bass19.features])
        intervals39 = Intervals39.decode(array[:, Bass19.features :])
        return [(b[0], b[1], i) for b, i in zip(bass19, intervals39)]


class BassChromagramIntervals77(FeatureRepresentation):
    """ """
    features = BassChromagram38.features + Intervals39.features

    def run(self, transposition="P1"):
        """

        Parameters
        ----------
        transposition :
             (Default value = "P1")

        Returns
        -------

        """
        self.bassChroma38 = BassChromagram38(self.df).run(transposition)
        self.intervals39 = Intervals39(self.df).run()
        array = np.concatenate((self.bassChroma38, self.intervals39), axis=1)
        return array

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        bassChroma38 = BassChromagram38.decode(
            array[:, : BassChromagram38.features]
        )
        intervals39 = Intervals39.decode(array[:, BassChromagram38.features :])
        return [
            (bc[0], bc[1], bc[2], bc[3], i)
            for bc, i in zip(bassChroma38, intervals39)
        ]


available_representations = {
    "Bass7": Bass7,
    "Bass12": Bass12,
    "Bass19": Bass19,
    "Bass35": Bass35,
    "Chromagram7": Chromagram7,
    "Chromagram12": Chromagram12,
    "Chromagram19": Chromagram19,
    "Chromagram35": Chromagram35,
    "MeasureOnset7": MeasureOnset7,
    "NoteOnset7": NoteOnset7,
    "MeasureNoteOnset14": MeasureNoteOnset14,
    "Intervals39": Intervals39,
    "Intervals19": Intervals19,
    "BassChromagram38": BassChromagram38,
    "BassChromagram70": BassChromagram70,
    "BassIntervals58": BassIntervals58,
    "BassChromagramIntervals77": BassChromagramIntervals77,
}
