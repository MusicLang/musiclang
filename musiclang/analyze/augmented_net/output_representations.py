"""The output tonal representations learned through multitask learning."""

import numpy as np

from .cache import (
    TransposeKey,
    TransposePcSet,
    TransposePitch,
)
from .feature_representation import (
    FeatureRepresentation,
    FeatureRepresentationTI,
    CHORD_QUALITIES,
    COMMON_ROMAN_NUMERALS,
    DEGREES,
    NOTEDURATIONS,
    KEYS,
    PCSETS,
    SPELLINGS,
)


class OutputRepresentation(FeatureRepresentation):
    """Output representations are all one-hot encoded (no many-hots).
    
    That makes them easier to template.

    Parameters
    ----------

    Returns
    -------

    """

    classList = []
    dfFeature = ""
    transpositionFn = None

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
        for frame, dfFeature in enumerate(self.df[self.dfFeature]):
            transposed = self.transpositionFn(dfFeature, transposition)
            rnIndex = self.classList.index(transposed)
            array[frame] = rnIndex
        return array

    @classmethod
    def classesNumber(cls):
        """ """
        return len(cls.classList)

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        return [cls.classList[index] for index in array.reshape(-1)]

    @classmethod
    def decodeOneHot(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != len(cls.classList):
            raise IndexError("Strange array shape.")
        return [cls.classList[np.argmax(onehot)] for onehot in array]


class OutputRepresentationTI(FeatureRepresentationTI):
    """Output representations are all one-hot encoded (no many-hots).
    
    That makes them easier to template.

    Parameters
    ----------

    Returns
    -------

    """

    classList = []
    dfFeature = ""

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
        for frame, dfFeature in enumerate(self.df[self.dfFeature]):
            rnIndex = self.classList.index(dfFeature)
            array[frame] = rnIndex
        return array

    @classmethod
    def classesNumber(cls):
        """ """
        return len(cls.classList)

    @classmethod
    def decode(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        return [cls.classList[index] for index in array.reshape(-1)]

    @classmethod
    def decodeOneHot(cls, array):
        """

        Parameters
        ----------
        array :
            

        Returns
        -------

        """
        if len(array.shape) != 2 or array.shape[1] != len(cls.classList):
            raise IndexError("Strange array shape.")
        return [cls.classList[np.argmax(onehot)] for onehot in array]


class Bass35(OutputRepresentation):
    """ """
    classList = SPELLINGS
    dfFeature = "a_bass"
    transpositionFn = staticmethod(TransposePitch)


class Tenor35(OutputRepresentation):
    """ """
    classList = SPELLINGS
    dfFeature = "a_tenor"
    transpositionFn = staticmethod(TransposePitch)


class Alto35(OutputRepresentation):
    """ """
    classList = SPELLINGS
    dfFeature = "a_alto"
    transpositionFn = staticmethod(TransposePitch)


class Soprano35(OutputRepresentation):
    """ """
    classList = SPELLINGS
    dfFeature = "a_soprano"
    transpositionFn = staticmethod(TransposePitch)


class Inversion4(OutputRepresentationTI):
    """ """
    classList = list(range(4))
    dfFeature = "a_inversion"

    def run(self):
        """ """
        array = np.zeros(self.shape, dtype=self.dtype)
        for frame, inversion in enumerate(self.df[self.dfFeature]):
            if inversion > 3:
                # Any chord beyond sevenths is encoded as "root" position
                inversion = 0
            array[frame] = int(inversion)
        return array


class HarmonicRhythm7(OutputRepresentationTI):
    """ """
    classList = NOTEDURATIONS
    dfFeature = "a_harmonicRhythm"


class RomanNumeral31(OutputRepresentationTI):
    """ """
    classList = COMMON_ROMAN_NUMERALS
    dfFeature = "a_romanNumeral"


class PrimaryDegree22(OutputRepresentationTI):
    """ """
    classList = DEGREES
    dfFeature = "a_degree1"


class SecondaryDegree22(OutputRepresentationTI):
    """ """
    classList = DEGREES
    dfFeature = "a_degree2"


class LocalKey38(OutputRepresentation):
    """ """
    classList = KEYS
    dfFeature = "a_localKey"
    transpositionFn = staticmethod(TransposeKey)


class TonicizedKey38(OutputRepresentation):
    """ """
    classList = KEYS
    dfFeature = "a_tonicizedKey"
    transpositionFn = staticmethod(TransposeKey)


class ChordRoot35(OutputRepresentation):
    """ """
    classList = SPELLINGS
    dfFeature = "a_root"
    transpositionFn = staticmethod(TransposePitch)


class ChordQuality11(OutputRepresentationTI):
    """ """
    classList = CHORD_QUALITIES
    dfFeature = "a_quality"


class PitchClassSet121(OutputRepresentation):
    """ """
    classList = PCSETS
    dfFeature = "a_pcset"
    transpositionFn = staticmethod(TransposePcSet)


available_representations = {
    "Bass35": Bass35,
    "Tenor35": Tenor35,
    "Alto35": Alto35,
    "Soprano35": Soprano35,
    "ChordQuality11": ChordQuality11,
    "ChordRoot35": ChordRoot35,
    "HarmonicRhythm7": HarmonicRhythm7,
    "Inversion4": Inversion4,
    "LocalKey38": LocalKey38,
    "PitchClassSet121": PitchClassSet121,
    "PrimaryDegree22": PrimaryDegree22,
    "RomanNumeral31": RomanNumeral31,
    "SecondaryDegree22": SecondaryDegree22,
    "TonicizedKey38": TonicizedKey38,
}
