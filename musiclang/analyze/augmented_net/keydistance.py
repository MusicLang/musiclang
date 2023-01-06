"""An auxiliary module to measure key distance."""

import music21
import numpy as np

# The diagonal of keys in the Weber tonal chart
# constrained to the range of keys between [Fb, G#]
WEBERDIAGONAL = [
    "B--",
    "c-",
    "F-",
    "g-",
    "C-",
    "d-",
    "G-",
    "a-",
    "D-",
    "e-",
    "A-",
    "b-",
    "E-",
    "f",
    "B-",
    "c",
    "F",
    "g",
    "C",
    "d",
    "G",
    "a",
    "D",
    "e",
    "A",
    "b",
    "E",
    "f#",
    "B",
    "c#",
    "F#",
    "g#",
    "C#",
    "d#",
    "G#",
    "a#",
    "D#",
    "e#",
    "A#",
    "b#",
]

# Adding this vector takes you to the next coordinates of a key
# in the Weber tonal chart, ascending from "flatness" to "sharpness"
TRANSPOSITION = np.array((2, 3))


def weberEuclidean(k1, k2):
    """A measurement of key distance based on the Weber tonal chart.

    Parameters
    ----------
    k1 :
        
    k2 :
        

    Returns
    -------

    """
    i1, i2 = WEBERDIAGONAL.index(k1), WEBERDIAGONAL.index(k2)
    flatterkey, sharperkey = sorted((i1, i2))
    coord1 = np.array((flatterkey, flatterkey))
    coord2 = np.array((sharperkey, sharperkey))
    smallerdistance = 1337
    for i in range(len(WEBERDIAGONAL) // 2):
        trans = TRANSPOSITION * i
        newcoord1 = trans + coord1
        distance = np.linalg.norm(coord2 - newcoord1)
        if distance < smallerdistance:
            smallerdistance = distance
    return smallerdistance


def getTonicizationScaleDegree(localKey, tonicizedKey):
    """

    Parameters
    ----------
    localKey :
        
    tonicizedKey :
        

    Returns
    -------
    type
        

    """
    tonic, _, third, _, fifth, _, _, _ = music21.key.Key(tonicizedKey).pitches
    c1 = music21.chord.Chord([tonic, third, fifth])
    # TODO: Use harmalysis to solve this problem, not romanNumeralFromChord
    degree = music21.roman.romanNumeralFromChord(c1, localKey).figure
    # TODO: This is a hack to workaround music21
    if localKey.islower() and degree == "bVI":
        degree = "VI"
    return degree
