"""Classes and data structures related to tonal features."""

import numpy as np

from .chord_vocabulary import frompcset

NOTENAMES = ("C", "D", "E", "F", "G", "A", "B")

NOTENAMES_LOWERCASE = [n.lower() for n in NOTENAMES]

PITCHCLASSES = list(range(12))

ACCIDENTALS = ("--", "-", "", "#", "##")

SPELLINGS = [
    f"{letter}{accidental}"
    for letter in NOTENAMES
    for accidental in ACCIDENTALS
]

INTERVALCLASSES = [
    f"{specific}{generic}"
    for generic in [2, 3, 6, 7]
    for specific in ["dd", "d", "m", "M", "A", "AA"]
] + [
    f"{specific}{generic}"
    for generic in [1, 4, 5]
    for specific in ["dd", "d", "P", "A", "AA"]
]

DEGREES = (
    "-1",
    "-2",
    "-3",
    "-4",
    "-5",
    "-6",
    "-7",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "#1",
    "#2",
    "#3",
    "#4",
    "#5",
    "#6",
    "#7",
    "None",
)

KEYS = tuple(sorted(set([key for keys in frompcset.values() for key in keys])))

# The keys used for transposition (data augmentation)
TRANSPOSITIONKEYS = tuple(KEYS)

CHORD_QUALITIES = tuple(
    sorted(
        set(
            [
                key["quality"]
                for keys in frompcset.values()
                for key in keys.values()
            ]
        )
    )
)

COMMON_ROMAN_NUMERALS = tuple(
    [
        # Cadentials are undistinguishable from a I chord in the vocabulary,
        # they are contextually (and explicitly) annotated by the analyst
        "Cad"
    ]
    + sorted(
        set(
            [key["rn"] for keys in frompcset.values() for key in keys.values()]
        )
    )
)

PCSETS = tuple(sorted(frompcset.keys()))

INTERVAL_ENHARMONICS = {
    "A1": "m2",
    "M2": "D3",
    "A2": "m3",
    "M3": "D4",
    "A3": "P4",
    "A4": "D5",
    "P5": "D6",
    "A5": "m6",
    "M6": "D7",
    "A6": "m7",
    "M7": "D8",
    "m2": "A1",
    "D3": "M2",
    "m3": "A2",
    "D4": "M3",
    "P4": "A3",
    "D5": "A4",
    "D6": "P5",
    "m6": "A5",
    "D7": "M6",
    "m7": "A6",
    "D8": "M7",
}

NOTEDURATIONS = [
    0,  # onset
    1,  # thirtysecond
    2,  # sixteenth
    3,  # eighth
    4,  # quarter
    5,  # half
    6,  # whole
]


class FeatureRepresentation(object):
    """ """
    features = 1

    def __init__(self, df):
        self.df = df
        self.frames = len(df.index)
        self.dtype = "i8"
        self.array = self.run()

    @property
    def shape(self):
        """ """
        return (self.frames, self.features)

    def run(self, tranposition=None):
        """

        Parameters
        ----------
        tranposition :
             (Default value = None)

        Returns
        -------

        """
        array = np.zeros(self.shape, dtype=self.dtype)
        return array

    def dataAugmentation(self, intervals):
        """

        Parameters
        ----------
        intervals :
            

        Returns
        -------

        """
        for interval in intervals:
            yield self.run(transposition=interval)
        return

    @classmethod
    def encodeManyHot(cls, array, timestep, index, value=1):
        """

        Parameters
        ----------
        array :
            
        timestep :
            
        index :
            
        value :
             (Default value = 1)

        Returns
        -------

        """
        if 0 <= index < cls.features:
            array[timestep, index] = value
        else:
            raise IndexError

    @classmethod
    def encodeCategorical(cls, array, timestep, classNumber):
        """

        Parameters
        ----------
        array :
            
        timestep :
            
        classNumber :
            

        Returns
        -------

        """
        if 0 <= classNumber < cls.features:
            array[timestep] = classNumber
        else:
            raise IndexError


class FeatureRepresentationTI(FeatureRepresentation):
    """TI stands for Transposition Invariant.
    
    If a representation is TI, dataAugmentation consists of

    Parameters
    ----------

    Returns
    -------
    type
        

    """

    def dataAugmentation(self, intervals):
        """

        Parameters
        ----------
        intervals :
            

        Returns
        -------

        """
        for _ in intervals:
            yield np.copy(self.array)
        return
