"""The vocabulary of all valid chords and their chord representations."""

from cmath import cos
import numpy as np
from numpy import dot
from numpy.linalg import norm


def cosineSimilarity(v1, v2):
    """

    Parameters
    ----------
    v1 :
        
    v2 :
        

    Returns
    -------

    """
    return dot(v1, v2) / (norm(v1) * norm(v2))


def closestPcSet(pcset):
    """Get the closest matching pcset from the vocabulary.
    
    Uses cosine similarity to measure the distance between
    the given pcset and all pcsets in the vocabulary.

    Parameters
    ----------
    pcset :
        

    Returns
    -------

    """
    v1 = np.zeros(12)
    for pc in pcset:
        v1[pc] = 1
    mostSimilarScore = -2
    closestPcSet = []
    for pcs in frompcset:
        v2 = np.zeros(12)
        for p in pcs:
            v2[p] = 1
        similarity = cosineSimilarity(v1, v2)
        if similarity > mostSimilarScore:
            closestPcSet = pcs
            mostSimilarScore = similarity
    return closestPcSet


frompcset = {
    (0, 1, 5, 8): {
        "A-": {
            "chord": ["D-", "F", "A-", "C"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "C#": {
            "chord": ["C#", "E#", "G#", "B#"],
            "quality": "maj7",
            "rn": "I7",
        },
        "D-": {"chord": ["D-", "F", "A-", "C"], "quality": "maj7", "rn": "I7"},
        "G#": {
            "chord": ["C#", "E#", "G#", "B#"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "e#": {
            "chord": ["C#", "E#", "G#", "B#"],
            "quality": "maj7",
            "rn": "VI7",
        },
        "f": {"chord": ["D-", "F", "A-", "C"], "quality": "maj7", "rn": "VI7"},
    },
    (0, 1, 5, 9): {
        "a#": {
            "chord": ["C#", "E#", "G##", "B#"],
            "quality": "aug7",
            "rn": "III+7",
        },
        "b-": {
            "chord": ["D-", "F", "A", "C"],
            "quality": "aug7",
            "rn": "III+7",
        },
    },
    (0, 2, 5, 8): {
        "D#": {
            "chord": ["C##", "E#", "G#", "B#"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "E-": {
            "chord": ["D", "F", "A-", "C"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "b#": {
            "chord": ["C##", "E#", "G#", "B#"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
        "c": {
            "chord": ["D", "F", "A-", "C"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (0, 2, 5, 9): {
        "B-": {"chord": ["D", "F", "A", "C"], "quality": "min7", "rn": "iii7"},
        "C": {"chord": ["D", "F", "A", "C"], "quality": "min7", "rn": "ii7"},
        "F": {"chord": ["D", "F", "A", "C"], "quality": "min7", "rn": "vi7"},
        "a": {"chord": ["D", "F", "A", "C"], "quality": "min7", "rn": "iv7"},
        "d": {"chord": ["D", "F", "A", "C"], "quality": "min7", "rn": "i7"},
    },
    (0, 2, 6): {
        "F#": {"chord": ["B#", "D", "F#"], "quality": "aug6", "rn": "It"},
        "G-": {"chord": ["C", "E--", "G-"], "quality": "aug6", "rn": "It"},
        "f#": {"chord": ["B#", "D", "F#"], "quality": "aug6", "rn": "It"},
        "g-": {"chord": ["C", "E--", "G-"], "quality": "aug6", "rn": "It"},
    },
    (0, 2, 6, 8): {
        "C": {"chord": ["D", "F#", "A-", "C"], "quality": "aug6", "rn": "Fr7"},
        "F#": {
            "chord": ["G#", "B#", "D", "F#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "G-": {
            "chord": ["A-", "C", "E--", "G-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "b#": {
            "chord": ["C##", "E##", "G#", "B#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "c": {"chord": ["D", "F#", "A-", "C"], "quality": "aug6", "rn": "Fr7"},
        "f#": {
            "chord": ["G#", "B#", "D", "F#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "g-": {
            "chord": ["A-", "C", "E--", "G-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
    },
    (0, 2, 6, 9): {
        "F#": {
            "chord": ["B#", "D", "F#", "A"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "G": {"chord": ["D", "F#", "A", "C"], "quality": "7", "rn": "V7"},
        "G-": {
            "chord": ["C", "E--", "G-", "B--"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "f#": {
            "chord": ["B#", "D", "F#", "A"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "g": {"chord": ["D", "F#", "A", "C"], "quality": "7", "rn": "V7"},
        "g-": {
            "chord": ["C", "E--", "G-", "B--"],
            "quality": "aug6",
            "rn": "Ger7",
        },
    },
    (0, 3, 4, 8): {
        "c#": {
            "chord": ["E", "G#", "B#", "D#"],
            "quality": "aug7",
            "rn": "III+7",
        },
        "d-": {
            "chord": ["F-", "A-", "C", "E-"],
            "quality": "aug7",
            "rn": "III+7",
        },
    },
    (0, 3, 5, 8): {
        "A-": {
            "chord": ["F", "A-", "C", "E-"],
            "quality": "min7",
            "rn": "vi7",
        },
        "C#": {
            "chord": ["E#", "G#", "B#", "D#"],
            "quality": "min7",
            "rn": "iii7",
        },
        "D#": {
            "chord": ["E#", "G#", "B#", "D#"],
            "quality": "min7",
            "rn": "ii7",
        },
        "D-": {
            "chord": ["F", "A-", "C", "E-"],
            "quality": "min7",
            "rn": "iii7",
        },
        "E-": {
            "chord": ["F", "A-", "C", "E-"],
            "quality": "min7",
            "rn": "ii7",
        },
        "G#": {
            "chord": ["E#", "G#", "B#", "D#"],
            "quality": "min7",
            "rn": "vi7",
        },
        "b#": {
            "chord": ["E#", "G#", "B#", "D#"],
            "quality": "min7",
            "rn": "iv7",
        },
        "c": {"chord": ["F", "A-", "C", "E-"], "quality": "min7", "rn": "iv7"},
        "e#": {
            "chord": ["E#", "G#", "B#", "D#"],
            "quality": "min7",
            "rn": "i7",
        },
        "f": {"chord": ["F", "A-", "C", "E-"], "quality": "min7", "rn": "i7"},
    },
    (0, 3, 5, 9): {
        "A": {"chord": ["D#", "F", "A", "C"], "quality": "aug6", "rn": "Ger7"},
        "B-": {"chord": ["F", "A", "C", "E-"], "quality": "7", "rn": "V7"},
        "B--": {
            "chord": ["E-", "G--", "B--", "D--"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "a": {"chord": ["D#", "F", "A", "C"], "quality": "aug6", "rn": "Ger7"},
        "a#": {"chord": ["E#", "G##", "B#", "D#"], "quality": "7", "rn": "V7"},
        "b-": {"chord": ["F", "A", "C", "E-"], "quality": "7", "rn": "V7"},
    },
    (0, 3, 6): {
        "C#": {"chord": ["B#", "D#", "F#"], "quality": "dim", "rn": "viio"},
        "D-": {"chord": ["C", "E-", "G-"], "quality": "dim", "rn": "viio"},
        "a#": {"chord": ["B#", "D#", "F#"], "quality": "dim", "rn": "iio"},
        "b-": {"chord": ["C", "E-", "G-"], "quality": "dim", "rn": "iio"},
        "c#": {"chord": ["B#", "D#", "F#"], "quality": "dim", "rn": "viio"},
        "d-": {"chord": ["C", "E-", "G-"], "quality": "dim", "rn": "viio"},
    },
    (0, 3, 6, 8): {
        "C": {
            "chord": ["F#", "A-", "C", "E-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "C#": {"chord": ["G#", "B#", "D#", "F#"], "quality": "7", "rn": "V7"},
        "D-": {"chord": ["A-", "C", "E-", "G-"], "quality": "7", "rn": "V7"},
        "b#": {
            "chord": ["E##", "G#", "B#", "D#"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "c": {
            "chord": ["F#", "A-", "C", "E-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "c#": {"chord": ["G#", "B#", "D#", "F#"], "quality": "7", "rn": "V7"},
        "d-": {"chord": ["A-", "C", "E-", "G-"], "quality": "7", "rn": "V7"},
    },
    (0, 3, 6, 9): {
        "a#": {
            "chord": ["G##", "B#", "D#", "F#"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "b-": {
            "chord": ["A", "C", "E-", "G-"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "c#": {
            "chord": ["B#", "D#", "F#", "A"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "d-": {
            "chord": ["C", "E-", "G-", "B--"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "e": {
            "chord": ["D#", "F#", "A", "C"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "g": {
            "chord": ["F#", "A", "C", "E-"],
            "quality": "dim7",
            "rn": "viio7",
        },
    },
    (0, 3, 6, 10): {
        "C#": {
            "chord": ["B#", "D#", "F#", "A#"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "D-": {
            "chord": ["C", "E-", "G-", "B-"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "a#": {
            "chord": ["B#", "D#", "F#", "A#"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
        "b-": {
            "chord": ["C", "E-", "G-", "B-"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (0, 3, 7): {
        "A-": {"chord": ["C", "E-", "G"], "quality": "min", "rn": "iii"},
        "B-": {"chord": ["C", "E-", "G"], "quality": "min", "rn": "ii"},
        "D#": {"chord": ["B#", "D#", "F##"], "quality": "min", "rn": "vi"},
        "E-": {"chord": ["C", "E-", "G"], "quality": "min", "rn": "vi"},
        "G#": {"chord": ["B#", "D#", "F##"], "quality": "min", "rn": "iii"},
        "b#": {"chord": ["B#", "D#", "F##"], "quality": "min", "rn": "i"},
        "c": {"chord": ["C", "E-", "G"], "quality": "min", "rn": "i"},
        "g": {"chord": ["C", "E-", "G"], "quality": "min", "rn": "iv"},
    },
    (0, 3, 7, 8): {
        "A-": {"chord": ["A-", "C", "E-", "G"], "quality": "maj7", "rn": "I7"},
        "D#": {
            "chord": ["G#", "B#", "D#", "F##"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "E-": {
            "chord": ["A-", "C", "E-", "G"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "G#": {
            "chord": ["G#", "B#", "D#", "F##"],
            "quality": "maj7",
            "rn": "I7",
        },
        "b#": {
            "chord": ["G#", "B#", "D#", "F##"],
            "quality": "maj7",
            "rn": "VI7",
        },
        "c": {"chord": ["A-", "C", "E-", "G"], "quality": "maj7", "rn": "VI7"},
    },
    (0, 3, 7, 9): {
        "B-": {
            "chord": ["A", "C", "E-", "G"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "g": {
            "chord": ["A", "C", "E-", "G"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (0, 3, 7, 10): {
        "A-": {
            "chord": ["C", "E-", "G", "B-"],
            "quality": "min7",
            "rn": "iii7",
        },
        "B-": {
            "chord": ["C", "E-", "G", "B-"],
            "quality": "min7",
            "rn": "ii7",
        },
        "D#": {
            "chord": ["B#", "D#", "F##", "A#"],
            "quality": "min7",
            "rn": "vi7",
        },
        "E-": {
            "chord": ["C", "E-", "G", "B-"],
            "quality": "min7",
            "rn": "vi7",
        },
        "G#": {
            "chord": ["B#", "D#", "F##", "A#"],
            "quality": "min7",
            "rn": "iii7",
        },
        "b#": {
            "chord": ["B#", "D#", "F##", "A#"],
            "quality": "min7",
            "rn": "i7",
        },
        "c": {"chord": ["C", "E-", "G", "B-"], "quality": "min7", "rn": "i7"},
        "g": {"chord": ["C", "E-", "G", "B-"], "quality": "min7", "rn": "iv7"},
    },
    (0, 3, 8): {
        "A-": {"chord": ["A-", "C", "E-"], "quality": "maj", "rn": "I"},
        "C#": {"chord": ["G#", "B#", "D#"], "quality": "maj", "rn": "V"},
        "D#": {"chord": ["G#", "B#", "D#"], "quality": "maj", "rn": "IV"},
        "D-": {"chord": ["A-", "C", "E-"], "quality": "maj", "rn": "V"},
        "E-": {"chord": ["A-", "C", "E-"], "quality": "maj", "rn": "IV"},
        "G": {"chord": ["A-", "C", "E-"], "quality": "maj", "rn": "N"},
        "G#": {"chord": ["G#", "B#", "D#"], "quality": "maj", "rn": "I"},
        "b#": {"chord": ["G#", "B#", "D#"], "quality": "maj", "rn": "VI"},
        "c": {"chord": ["A-", "C", "E-"], "quality": "maj", "rn": "VI"},
        "c#": {"chord": ["G#", "B#", "D#"], "quality": "maj", "rn": "V"},
        "d-": {"chord": ["A-", "C", "E-"], "quality": "maj", "rn": "V"},
        "g": {"chord": ["A-", "C", "E-"], "quality": "maj", "rn": "N"},
    },
    (0, 3, 9): {
        "B-": {"chord": ["A", "C", "E-"], "quality": "dim", "rn": "viio"},
        "a#": {"chord": ["G##", "B#", "D#"], "quality": "dim", "rn": "viio"},
        "b-": {"chord": ["A", "C", "E-"], "quality": "dim", "rn": "viio"},
        "g": {"chord": ["A", "C", "E-"], "quality": "dim", "rn": "iio"},
    },
    (0, 4, 5, 9): {
        "C": {"chord": ["F", "A", "C", "E"], "quality": "maj7", "rn": "IV7"},
        "F": {"chord": ["F", "A", "C", "E"], "quality": "maj7", "rn": "I7"},
        "a": {"chord": ["F", "A", "C", "E"], "quality": "maj7", "rn": "VI7"},
    },
    (0, 4, 6, 9): {
        "G": {
            "chord": ["F#", "A", "C", "E"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "e": {
            "chord": ["F#", "A", "C", "E"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (0, 4, 6, 10): {
        "B-": {
            "chord": ["C", "E", "G-", "B-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "E": {"chord": ["F#", "A#", "C", "E"], "quality": "aug6", "rn": "Fr7"},
        "F-": {
            "chord": ["G-", "B-", "D--", "F-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "a#": {
            "chord": ["B#", "D##", "F#", "A#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "b-": {
            "chord": ["C", "E", "G-", "B-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "e": {"chord": ["F#", "A#", "C", "E"], "quality": "aug6", "rn": "Fr7"},
    },
    (0, 4, 7): {
        "B": {"chord": ["C", "E", "G"], "quality": "maj", "rn": "N"},
        "C": {"chord": ["C", "E", "G"], "quality": "maj", "rn": "I"},
        "C-": {"chord": ["D--", "F-", "A--"], "quality": "maj", "rn": "N"},
        "F": {"chord": ["C", "E", "G"], "quality": "maj", "rn": "V"},
        "G": {"chord": ["C", "E", "G"], "quality": "maj", "rn": "IV"},
        "b": {"chord": ["C", "E", "G"], "quality": "maj", "rn": "N"},
        "e": {"chord": ["C", "E", "G"], "quality": "maj", "rn": "VI"},
        "e#": {"chord": ["B#", "D##", "F##"], "quality": "maj", "rn": "V"},
        "f": {"chord": ["C", "E", "G"], "quality": "maj", "rn": "V"},
    },
    (0, 4, 7, 8): {
        "e#": {
            "chord": ["G#", "B#", "D##", "F##"],
            "quality": "aug7",
            "rn": "III+7",
        },
        "f": {
            "chord": ["A-", "C", "E", "G"],
            "quality": "aug7",
            "rn": "III+7",
        },
    },
    (0, 4, 7, 9): {
        "C": {"chord": ["A", "C", "E", "G"], "quality": "min7", "rn": "vi7"},
        "F": {"chord": ["A", "C", "E", "G"], "quality": "min7", "rn": "iii7"},
        "G": {"chord": ["A", "C", "E", "G"], "quality": "min7", "rn": "ii7"},
        "a": {"chord": ["A", "C", "E", "G"], "quality": "min7", "rn": "i7"},
        "e": {"chord": ["A", "C", "E", "G"], "quality": "min7", "rn": "iv7"},
    },
    (0, 4, 7, 10): {
        "E": {"chord": ["A#", "C", "E", "G"], "quality": "aug6", "rn": "Ger7"},
        "F": {"chord": ["C", "E", "G", "B-"], "quality": "7", "rn": "V7"},
        "F-": {
            "chord": ["B-", "D--", "F-", "A--"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "e": {"chord": ["A#", "C", "E", "G"], "quality": "aug6", "rn": "Ger7"},
        "e#": {
            "chord": ["B#", "D##", "F##", "A#"],
            "quality": "7",
            "rn": "V7",
        },
        "f": {"chord": ["C", "E", "G", "B-"], "quality": "7", "rn": "V7"},
    },
    (0, 4, 7, 11): {
        "C": {"chord": ["C", "E", "G", "B"], "quality": "maj7", "rn": "I7"},
        "G": {"chord": ["C", "E", "G", "B"], "quality": "maj7", "rn": "IV7"},
        "e": {"chord": ["C", "E", "G", "B"], "quality": "maj7", "rn": "VI7"},
    },
    (0, 4, 8): {
        "A": {"chord": ["E", "G#", "B#"], "quality": "aug", "rn": "V+"},
        "B--": {"chord": ["F-", "A-", "C"], "quality": "aug", "rn": "V+"},
        "C#": {"chord": ["G#", "B#", "D##"], "quality": "aug", "rn": "V+"},
        "D-": {"chord": ["A-", "C", "E"], "quality": "aug", "rn": "V+"},
        "F": {"chord": ["C", "E", "G#"], "quality": "aug", "rn": "V+"},
        "a": {"chord": ["C", "E", "G#"], "quality": "aug", "rn": "III+"},
        "c#": {"chord": ["E", "G#", "B#"], "quality": "aug", "rn": "III+"},
        "d-": {"chord": ["F-", "A-", "C"], "quality": "aug", "rn": "III+"},
        "e#": {"chord": ["G#", "B#", "D##"], "quality": "aug", "rn": "III+"},
        "f": {"chord": ["A-", "C", "E"], "quality": "aug", "rn": "III+"},
    },
    (0, 4, 8, 11): {
        "a": {"chord": ["C", "E", "G#", "B"], "quality": "aug7", "rn": "III+7"}
    },
    (0, 4, 9): {
        "C": {"chord": ["A", "C", "E"], "quality": "min", "rn": "vi"},
        "F": {"chord": ["A", "C", "E"], "quality": "min", "rn": "iii"},
        "G": {"chord": ["A", "C", "E"], "quality": "min", "rn": "ii"},
        "a": {"chord": ["A", "C", "E"], "quality": "min", "rn": "i"},
        "e": {"chord": ["A", "C", "E"], "quality": "min", "rn": "iv"},
    },
    (0, 4, 10): {
        "E": {"chord": ["A#", "C", "E"], "quality": "aug6", "rn": "It"},
        "F-": {"chord": ["B-", "D--", "F-"], "quality": "aug6", "rn": "It"},
        "e": {"chord": ["A#", "C", "E"], "quality": "aug6", "rn": "It"},
    },
    (0, 5, 8): {
        "A-": {"chord": ["F", "A-", "C"], "quality": "min", "rn": "vi"},
        "C#": {"chord": ["E#", "G#", "B#"], "quality": "min", "rn": "iii"},
        "D#": {"chord": ["E#", "G#", "B#"], "quality": "min", "rn": "ii"},
        "D-": {"chord": ["F", "A-", "C"], "quality": "min", "rn": "iii"},
        "E-": {"chord": ["F", "A-", "C"], "quality": "min", "rn": "ii"},
        "G#": {"chord": ["E#", "G#", "B#"], "quality": "min", "rn": "vi"},
        "b#": {"chord": ["E#", "G#", "B#"], "quality": "min", "rn": "iv"},
        "c": {"chord": ["F", "A-", "C"], "quality": "min", "rn": "iv"},
        "e#": {"chord": ["E#", "G#", "B#"], "quality": "min", "rn": "i"},
        "f": {"chord": ["F", "A-", "C"], "quality": "min", "rn": "i"},
    },
    (0, 5, 9): {
        "B-": {"chord": ["F", "A", "C"], "quality": "maj", "rn": "V"},
        "C": {"chord": ["F", "A", "C"], "quality": "maj", "rn": "IV"},
        "E": {"chord": ["F", "A", "C"], "quality": "maj", "rn": "N"},
        "F": {"chord": ["F", "A", "C"], "quality": "maj", "rn": "I"},
        "F-": {"chord": ["G--", "B--", "D--"], "quality": "maj", "rn": "N"},
        "a": {"chord": ["F", "A", "C"], "quality": "maj", "rn": "VI"},
        "a#": {"chord": ["E#", "G##", "B#"], "quality": "maj", "rn": "V"},
        "b-": {"chord": ["F", "A", "C"], "quality": "maj", "rn": "V"},
        "e": {"chord": ["F", "A", "C"], "quality": "maj", "rn": "N"},
    },
    (0, 6, 8): {
        "C": {"chord": ["F#", "A-", "C"], "quality": "aug6", "rn": "It"},
        "b#": {"chord": ["E##", "G#", "B#"], "quality": "aug6", "rn": "It"},
        "c": {"chord": ["F#", "A-", "C"], "quality": "aug6", "rn": "It"},
    },
    (0, 6, 9): {
        "G": {"chord": ["F#", "A", "C"], "quality": "dim", "rn": "viio"},
        "e": {"chord": ["F#", "A", "C"], "quality": "dim", "rn": "iio"},
        "g": {"chord": ["F#", "A", "C"], "quality": "dim", "rn": "viio"},
    },
    (1, 2, 6, 9): {
        "A": {"chord": ["D", "F#", "A", "C#"], "quality": "maj7", "rn": "IV7"},
        "B--": {
            "chord": ["E--", "G-", "B--", "D-"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "D": {"chord": ["D", "F#", "A", "C#"], "quality": "maj7", "rn": "I7"},
        "f#": {
            "chord": ["D", "F#", "A", "C#"],
            "quality": "maj7",
            "rn": "VI7",
        },
        "g-": {
            "chord": ["E--", "G-", "B--", "D-"],
            "quality": "maj7",
            "rn": "VI7",
        },
    },
    (1, 2, 6, 10): {
        "b": {
            "chord": ["D", "F#", "A#", "C#"],
            "quality": "aug7",
            "rn": "III+7",
        }
    },
    (1, 3, 6, 9): {
        "E": {
            "chord": ["D#", "F#", "A", "C#"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "F-": {
            "chord": ["E-", "G-", "B--", "D-"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "c#": {
            "chord": ["D#", "F#", "A", "C#"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
        "d-": {
            "chord": ["E-", "G-", "B--", "D-"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (1, 3, 6, 10): {
        "B": {
            "chord": ["D#", "F#", "A#", "C#"],
            "quality": "min7",
            "rn": "iii7",
        },
        "C#": {
            "chord": ["D#", "F#", "A#", "C#"],
            "quality": "min7",
            "rn": "ii7",
        },
        "C-": {
            "chord": ["E-", "G-", "B-", "D-"],
            "quality": "min7",
            "rn": "iii7",
        },
        "D-": {
            "chord": ["E-", "G-", "B-", "D-"],
            "quality": "min7",
            "rn": "ii7",
        },
        "F#": {
            "chord": ["D#", "F#", "A#", "C#"],
            "quality": "min7",
            "rn": "vi7",
        },
        "G-": {
            "chord": ["E-", "G-", "B-", "D-"],
            "quality": "min7",
            "rn": "vi7",
        },
        "a#": {
            "chord": ["D#", "F#", "A#", "C#"],
            "quality": "min7",
            "rn": "iv7",
        },
        "b-": {
            "chord": ["E-", "G-", "B-", "D-"],
            "quality": "min7",
            "rn": "iv7",
        },
        "d#": {
            "chord": ["D#", "F#", "A#", "C#"],
            "quality": "min7",
            "rn": "i7",
        },
        "e-": {
            "chord": ["E-", "G-", "B-", "D-"],
            "quality": "min7",
            "rn": "i7",
        },
    },
    (1, 3, 7): {
        "G": {"chord": ["C#", "E-", "G"], "quality": "aug6", "rn": "It"},
        "g": {"chord": ["C#", "E-", "G"], "quality": "aug6", "rn": "It"},
    },
    (1, 3, 7, 9): {
        "C#": {
            "chord": ["D#", "F##", "A", "C#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "D-": {
            "chord": ["E-", "G", "B--", "D-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "G": {"chord": ["A", "C#", "E-", "G"], "quality": "aug6", "rn": "Fr7"},
        "c#": {
            "chord": ["D#", "F##", "A", "C#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "d-": {
            "chord": ["E-", "G", "B--", "D-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "g": {"chord": ["A", "C#", "E-", "G"], "quality": "aug6", "rn": "Fr7"},
    },
    (1, 3, 7, 10): {
        "A-": {"chord": ["E-", "G", "B-", "D-"], "quality": "7", "rn": "V7"},
        "G": {
            "chord": ["C#", "E-", "G", "B-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "G#": {"chord": ["D#", "F##", "A#", "C#"], "quality": "7", "rn": "V7"},
        "a-": {"chord": ["E-", "G", "B-", "D-"], "quality": "7", "rn": "V7"},
        "g": {
            "chord": ["C#", "E-", "G", "B-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "g#": {"chord": ["D#", "F##", "A#", "C#"], "quality": "7", "rn": "V7"},
    },
    (1, 4, 5, 9): {
        "d": {"chord": ["F", "A", "C#", "E"], "quality": "aug7", "rn": "III+7"}
    },
    (1, 4, 6, 9): {
        "A": {"chord": ["F#", "A", "C#", "E"], "quality": "min7", "rn": "vi7"},
        "B--": {
            "chord": ["G-", "B--", "D-", "F-"],
            "quality": "min7",
            "rn": "vi7",
        },
        "D": {
            "chord": ["F#", "A", "C#", "E"],
            "quality": "min7",
            "rn": "iii7",
        },
        "E": {"chord": ["F#", "A", "C#", "E"], "quality": "min7", "rn": "ii7"},
        "F-": {
            "chord": ["G-", "B--", "D-", "F-"],
            "quality": "min7",
            "rn": "ii7",
        },
        "c#": {
            "chord": ["F#", "A", "C#", "E"],
            "quality": "min7",
            "rn": "iv7",
        },
        "d-": {
            "chord": ["G-", "B--", "D-", "F-"],
            "quality": "min7",
            "rn": "iv7",
        },
        "f#": {"chord": ["F#", "A", "C#", "E"], "quality": "min7", "rn": "i7"},
        "g-": {
            "chord": ["G-", "B--", "D-", "F-"],
            "quality": "min7",
            "rn": "i7",
        },
    },
    (1, 4, 6, 10): {
        "B": {"chord": ["F#", "A#", "C#", "E"], "quality": "7", "rn": "V7"},
        "B-": {
            "chord": ["E", "G-", "B-", "D-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "C-": {"chord": ["G-", "B-", "D-", "F-"], "quality": "7", "rn": "V7"},
        "a#": {
            "chord": ["D##", "F#", "A#", "C#"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "b": {"chord": ["F#", "A#", "C#", "E"], "quality": "7", "rn": "V7"},
        "b-": {
            "chord": ["E", "G-", "B-", "D-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
    },
    (1, 4, 7): {
        "D": {"chord": ["C#", "E", "G"], "quality": "dim", "rn": "viio"},
        "b": {"chord": ["C#", "E", "G"], "quality": "dim", "rn": "iio"},
        "d": {"chord": ["C#", "E", "G"], "quality": "dim", "rn": "viio"},
    },
    (1, 4, 7, 9): {
        "C#": {
            "chord": ["F##", "A", "C#", "E"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "D": {"chord": ["A", "C#", "E", "G"], "quality": "7", "rn": "V7"},
        "D-": {
            "chord": ["G", "B--", "D-", "F-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "c#": {
            "chord": ["F##", "A", "C#", "E"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "d": {"chord": ["A", "C#", "E", "G"], "quality": "7", "rn": "V7"},
        "d-": {
            "chord": ["G", "B--", "D-", "F-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
    },
    (1, 4, 7, 10): {
        "a-": {
            "chord": ["G", "B-", "D-", "F-"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "b": {
            "chord": ["A#", "C#", "E", "G"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "d": {
            "chord": ["C#", "E", "G", "B-"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "e#": {
            "chord": ["D##", "F##", "A#", "C#"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "f": {
            "chord": ["E", "G", "B-", "D-"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "g#": {
            "chord": ["F##", "A#", "C#", "E"],
            "quality": "dim7",
            "rn": "viio7",
        },
    },
    (1, 4, 7, 11): {
        "D": {
            "chord": ["C#", "E", "G", "B"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "b": {
            "chord": ["C#", "E", "G", "B"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (1, 4, 8): {
        "A": {"chord": ["C#", "E", "G#"], "quality": "min", "rn": "iii"},
        "B": {"chord": ["C#", "E", "G#"], "quality": "min", "rn": "ii"},
        "B--": {"chord": ["D-", "F-", "A-"], "quality": "min", "rn": "iii"},
        "C-": {"chord": ["D-", "F-", "A-"], "quality": "min", "rn": "ii"},
        "E": {"chord": ["C#", "E", "G#"], "quality": "min", "rn": "vi"},
        "F-": {"chord": ["D-", "F-", "A-"], "quality": "min", "rn": "vi"},
        "a-": {"chord": ["D-", "F-", "A-"], "quality": "min", "rn": "iv"},
        "c#": {"chord": ["C#", "E", "G#"], "quality": "min", "rn": "i"},
        "d-": {"chord": ["D-", "F-", "A-"], "quality": "min", "rn": "i"},
        "g#": {"chord": ["C#", "E", "G#"], "quality": "min", "rn": "iv"},
    },
    (1, 4, 8, 9): {
        "A": {"chord": ["A", "C#", "E", "G#"], "quality": "maj7", "rn": "I7"},
        "B--": {
            "chord": ["B--", "D-", "F-", "A-"],
            "quality": "maj7",
            "rn": "I7",
        },
        "E": {"chord": ["A", "C#", "E", "G#"], "quality": "maj7", "rn": "IV7"},
        "F-": {
            "chord": ["B--", "D-", "F-", "A-"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "c#": {
            "chord": ["A", "C#", "E", "G#"],
            "quality": "maj7",
            "rn": "VI7",
        },
        "d-": {
            "chord": ["B--", "D-", "F-", "A-"],
            "quality": "maj7",
            "rn": "VI7",
        },
    },
    (1, 4, 8, 10): {
        "B": {
            "chord": ["A#", "C#", "E", "G#"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "C-": {
            "chord": ["B-", "D-", "F-", "A-"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "a-": {
            "chord": ["B-", "D-", "F-", "A-"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
        "g#": {
            "chord": ["A#", "C#", "E", "G#"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (1, 4, 8, 11): {
        "A": {
            "chord": ["C#", "E", "G#", "B"],
            "quality": "min7",
            "rn": "iii7",
        },
        "B": {"chord": ["C#", "E", "G#", "B"], "quality": "min7", "rn": "ii7"},
        "B--": {
            "chord": ["D-", "F-", "A-", "C-"],
            "quality": "min7",
            "rn": "iii7",
        },
        "C-": {
            "chord": ["D-", "F-", "A-", "C-"],
            "quality": "min7",
            "rn": "ii7",
        },
        "E": {"chord": ["C#", "E", "G#", "B"], "quality": "min7", "rn": "vi7"},
        "F-": {
            "chord": ["D-", "F-", "A-", "C-"],
            "quality": "min7",
            "rn": "vi7",
        },
        "a-": {
            "chord": ["D-", "F-", "A-", "C-"],
            "quality": "min7",
            "rn": "iv7",
        },
        "c#": {"chord": ["C#", "E", "G#", "B"], "quality": "min7", "rn": "i7"},
        "d-": {
            "chord": ["D-", "F-", "A-", "C-"],
            "quality": "min7",
            "rn": "i7",
        },
        "g#": {
            "chord": ["C#", "E", "G#", "B"],
            "quality": "min7",
            "rn": "iv7",
        },
    },
    (1, 4, 9): {
        "A": {"chord": ["A", "C#", "E"], "quality": "maj", "rn": "I"},
        "A-": {"chord": ["B--", "D-", "F-"], "quality": "maj", "rn": "N"},
        "B--": {"chord": ["B--", "D-", "F-"], "quality": "maj", "rn": "I"},
        "D": {"chord": ["A", "C#", "E"], "quality": "maj", "rn": "V"},
        "E": {"chord": ["A", "C#", "E"], "quality": "maj", "rn": "IV"},
        "F-": {"chord": ["B--", "D-", "F-"], "quality": "maj", "rn": "IV"},
        "G#": {"chord": ["A", "C#", "E"], "quality": "maj", "rn": "N"},
        "a-": {"chord": ["B--", "D-", "F-"], "quality": "maj", "rn": "N"},
        "c#": {"chord": ["A", "C#", "E"], "quality": "maj", "rn": "VI"},
        "d": {"chord": ["A", "C#", "E"], "quality": "maj", "rn": "V"},
        "d-": {"chord": ["B--", "D-", "F-"], "quality": "maj", "rn": "VI"},
        "g#": {"chord": ["A", "C#", "E"], "quality": "maj", "rn": "N"},
    },
    (1, 4, 10): {
        "B": {"chord": ["A#", "C#", "E"], "quality": "dim", "rn": "viio"},
        "C-": {"chord": ["B-", "D-", "F-"], "quality": "dim", "rn": "viio"},
        "a-": {"chord": ["B-", "D-", "F-"], "quality": "dim", "rn": "iio"},
        "b": {"chord": ["A#", "C#", "E"], "quality": "dim", "rn": "viio"},
        "g#": {"chord": ["A#", "C#", "E"], "quality": "dim", "rn": "iio"},
    },
    (1, 5, 6, 10): {
        "C#": {
            "chord": ["F#", "A#", "C#", "E#"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "D-": {
            "chord": ["G-", "B-", "D-", "F"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "F#": {
            "chord": ["F#", "A#", "C#", "E#"],
            "quality": "maj7",
            "rn": "I7",
        },
        "G-": {
            "chord": ["G-", "B-", "D-", "F"],
            "quality": "maj7",
            "rn": "I7",
        },
        "a#": {
            "chord": ["F#", "A#", "C#", "E#"],
            "quality": "maj7",
            "rn": "VI7",
        },
        "b-": {
            "chord": ["G-", "B-", "D-", "F"],
            "quality": "maj7",
            "rn": "VI7",
        },
    },
    (1, 5, 7, 10): {
        "A-": {
            "chord": ["G", "B-", "D-", "F"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "G#": {
            "chord": ["F##", "A#", "C#", "E#"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "e#": {
            "chord": ["F##", "A#", "C#", "E#"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
        "f": {
            "chord": ["G", "B-", "D-", "F"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (1, 5, 7, 11): {
        "B": {"chord": ["C#", "E#", "G", "B"], "quality": "aug6", "rn": "Fr7"},
        "C-": {
            "chord": ["D-", "F", "A--", "C-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "F": {"chord": ["G", "B", "D-", "F"], "quality": "aug6", "rn": "Fr7"},
        "b": {"chord": ["C#", "E#", "G", "B"], "quality": "aug6", "rn": "Fr7"},
        "e#": {
            "chord": ["F##", "A##", "C#", "E#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "f": {"chord": ["G", "B", "D-", "F"], "quality": "aug6", "rn": "Fr7"},
    },
    (1, 5, 8): {
        "A-": {"chord": ["D-", "F", "A-"], "quality": "maj", "rn": "IV"},
        "C": {"chord": ["D-", "F", "A-"], "quality": "maj", "rn": "N"},
        "C#": {"chord": ["C#", "E#", "G#"], "quality": "maj", "rn": "I"},
        "D-": {"chord": ["D-", "F", "A-"], "quality": "maj", "rn": "I"},
        "F#": {"chord": ["C#", "E#", "G#"], "quality": "maj", "rn": "V"},
        "G#": {"chord": ["C#", "E#", "G#"], "quality": "maj", "rn": "IV"},
        "G-": {"chord": ["D-", "F", "A-"], "quality": "maj", "rn": "V"},
        "b#": {"chord": ["C#", "E#", "G#"], "quality": "maj", "rn": "N"},
        "c": {"chord": ["D-", "F", "A-"], "quality": "maj", "rn": "N"},
        "e#": {"chord": ["C#", "E#", "G#"], "quality": "maj", "rn": "VI"},
        "f": {"chord": ["D-", "F", "A-"], "quality": "maj", "rn": "VI"},
        "f#": {"chord": ["C#", "E#", "G#"], "quality": "maj", "rn": "V"},
        "g-": {"chord": ["D-", "F", "A-"], "quality": "maj", "rn": "V"},
    },
    (1, 5, 8, 9): {
        "f#": {
            "chord": ["A", "C#", "E#", "G#"],
            "quality": "aug7",
            "rn": "III+7",
        },
        "g-": {
            "chord": ["B--", "D-", "F", "A-"],
            "quality": "aug7",
            "rn": "III+7",
        },
    },
    (1, 5, 8, 10): {
        "A-": {
            "chord": ["B-", "D-", "F", "A-"],
            "quality": "min7",
            "rn": "ii7",
        },
        "C#": {
            "chord": ["A#", "C#", "E#", "G#"],
            "quality": "min7",
            "rn": "vi7",
        },
        "D-": {
            "chord": ["B-", "D-", "F", "A-"],
            "quality": "min7",
            "rn": "vi7",
        },
        "F#": {
            "chord": ["A#", "C#", "E#", "G#"],
            "quality": "min7",
            "rn": "iii7",
        },
        "G#": {
            "chord": ["A#", "C#", "E#", "G#"],
            "quality": "min7",
            "rn": "ii7",
        },
        "G-": {
            "chord": ["B-", "D-", "F", "A-"],
            "quality": "min7",
            "rn": "iii7",
        },
        "a#": {
            "chord": ["A#", "C#", "E#", "G#"],
            "quality": "min7",
            "rn": "i7",
        },
        "b-": {
            "chord": ["B-", "D-", "F", "A-"],
            "quality": "min7",
            "rn": "i7",
        },
        "e#": {
            "chord": ["A#", "C#", "E#", "G#"],
            "quality": "min7",
            "rn": "iv7",
        },
        "f": {
            "chord": ["B-", "D-", "F", "A-"],
            "quality": "min7",
            "rn": "iv7",
        },
    },
    (1, 5, 8, 11): {
        "F": {
            "chord": ["B", "D-", "F", "A-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "F#": {"chord": ["C#", "E#", "G#", "B"], "quality": "7", "rn": "V7"},
        "G-": {"chord": ["D-", "F", "A-", "C-"], "quality": "7", "rn": "V7"},
        "e#": {
            "chord": ["A##", "C#", "E#", "G#"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "f": {
            "chord": ["B", "D-", "F", "A-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "f#": {"chord": ["C#", "E#", "G#", "B"], "quality": "7", "rn": "V7"},
        "g-": {"chord": ["D-", "F", "A-", "C-"], "quality": "7", "rn": "V7"},
    },
    (1, 5, 9): {
        "B-": {"chord": ["F", "A", "C#"], "quality": "aug", "rn": "V+"},
        "D": {"chord": ["A", "C#", "E#"], "quality": "aug", "rn": "V+"},
        "F#": {"chord": ["C#", "E#", "G##"], "quality": "aug", "rn": "V+"},
        "G-": {"chord": ["D-", "F", "A"], "quality": "aug", "rn": "V+"},
        "a#": {"chord": ["C#", "E#", "G##"], "quality": "aug", "rn": "III+"},
        "b-": {"chord": ["D-", "F", "A"], "quality": "aug", "rn": "III+"},
        "d": {"chord": ["F", "A", "C#"], "quality": "aug", "rn": "III+"},
        "f#": {"chord": ["A", "C#", "E#"], "quality": "aug", "rn": "III+"},
        "g-": {"chord": ["B--", "D-", "F"], "quality": "aug", "rn": "III+"},
    },
    (1, 5, 10): {
        "A-": {"chord": ["B-", "D-", "F"], "quality": "min", "rn": "ii"},
        "C#": {"chord": ["A#", "C#", "E#"], "quality": "min", "rn": "vi"},
        "D-": {"chord": ["B-", "D-", "F"], "quality": "min", "rn": "vi"},
        "F#": {"chord": ["A#", "C#", "E#"], "quality": "min", "rn": "iii"},
        "G#": {"chord": ["A#", "C#", "E#"], "quality": "min", "rn": "ii"},
        "G-": {"chord": ["B-", "D-", "F"], "quality": "min", "rn": "iii"},
        "a#": {"chord": ["A#", "C#", "E#"], "quality": "min", "rn": "i"},
        "b-": {"chord": ["B-", "D-", "F"], "quality": "min", "rn": "i"},
        "e#": {"chord": ["A#", "C#", "E#"], "quality": "min", "rn": "iv"},
        "f": {"chord": ["B-", "D-", "F"], "quality": "min", "rn": "iv"},
    },
    (1, 5, 11): {
        "F": {"chord": ["B", "D-", "F"], "quality": "aug6", "rn": "It"},
        "e#": {"chord": ["A##", "C#", "E#"], "quality": "aug6", "rn": "It"},
        "f": {"chord": ["B", "D-", "F"], "quality": "aug6", "rn": "It"},
    },
    (1, 6, 9): {
        "A": {"chord": ["F#", "A", "C#"], "quality": "min", "rn": "vi"},
        "B--": {"chord": ["G-", "B--", "D-"], "quality": "min", "rn": "vi"},
        "D": {"chord": ["F#", "A", "C#"], "quality": "min", "rn": "iii"},
        "E": {"chord": ["F#", "A", "C#"], "quality": "min", "rn": "ii"},
        "F-": {"chord": ["G-", "B--", "D-"], "quality": "min", "rn": "ii"},
        "c#": {"chord": ["F#", "A", "C#"], "quality": "min", "rn": "iv"},
        "d-": {"chord": ["G-", "B--", "D-"], "quality": "min", "rn": "iv"},
        "f#": {"chord": ["F#", "A", "C#"], "quality": "min", "rn": "i"},
        "g-": {"chord": ["G-", "B--", "D-"], "quality": "min", "rn": "i"},
    },
    (1, 6, 10): {
        "B": {"chord": ["F#", "A#", "C#"], "quality": "maj", "rn": "V"},
        "C#": {"chord": ["F#", "A#", "C#"], "quality": "maj", "rn": "IV"},
        "C-": {"chord": ["G-", "B-", "D-"], "quality": "maj", "rn": "V"},
        "D-": {"chord": ["G-", "B-", "D-"], "quality": "maj", "rn": "IV"},
        "F": {"chord": ["G-", "B-", "D-"], "quality": "maj", "rn": "N"},
        "F#": {"chord": ["F#", "A#", "C#"], "quality": "maj", "rn": "I"},
        "G-": {"chord": ["G-", "B-", "D-"], "quality": "maj", "rn": "I"},
        "a#": {"chord": ["F#", "A#", "C#"], "quality": "maj", "rn": "VI"},
        "b": {"chord": ["F#", "A#", "C#"], "quality": "maj", "rn": "V"},
        "b-": {"chord": ["G-", "B-", "D-"], "quality": "maj", "rn": "VI"},
        "e#": {"chord": ["F#", "A#", "C#"], "quality": "maj", "rn": "N"},
        "f": {"chord": ["G-", "B-", "D-"], "quality": "maj", "rn": "N"},
    },
    (1, 7, 9): {
        "C#": {"chord": ["F##", "A", "C#"], "quality": "aug6", "rn": "It"},
        "D-": {"chord": ["G", "B--", "D-"], "quality": "aug6", "rn": "It"},
        "c#": {"chord": ["F##", "A", "C#"], "quality": "aug6", "rn": "It"},
        "d-": {"chord": ["G", "B--", "D-"], "quality": "aug6", "rn": "It"},
    },
    (1, 7, 10): {
        "A-": {"chord": ["G", "B-", "D-"], "quality": "dim", "rn": "viio"},
        "G#": {"chord": ["F##", "A#", "C#"], "quality": "dim", "rn": "viio"},
        "a-": {"chord": ["G", "B-", "D-"], "quality": "dim", "rn": "viio"},
        "e#": {"chord": ["F##", "A#", "C#"], "quality": "dim", "rn": "iio"},
        "f": {"chord": ["G", "B-", "D-"], "quality": "dim", "rn": "iio"},
        "g#": {"chord": ["F##", "A#", "C#"], "quality": "dim", "rn": "viio"},
    },
    (2, 3, 7, 10): {
        "B-": {
            "chord": ["E-", "G", "B-", "D"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "D#": {
            "chord": ["D#", "F##", "A#", "C##"],
            "quality": "maj7",
            "rn": "I7",
        },
        "E-": {"chord": ["E-", "G", "B-", "D"], "quality": "maj7", "rn": "I7"},
        "g": {"chord": ["E-", "G", "B-", "D"], "quality": "maj7", "rn": "VI7"},
    },
    (2, 3, 7, 11): {
        "b#": {
            "chord": ["D#", "F##", "A##", "C##"],
            "quality": "aug7",
            "rn": "III+7",
        },
        "c": {
            "chord": ["E-", "G", "B", "D"],
            "quality": "aug7",
            "rn": "III+7",
        },
    },
    (2, 4, 7, 10): {
        "F": {
            "chord": ["E", "G", "B-", "D"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "d": {
            "chord": ["E", "G", "B-", "D"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (2, 4, 7, 11): {
        "C": {"chord": ["E", "G", "B", "D"], "quality": "min7", "rn": "iii7"},
        "D": {"chord": ["E", "G", "B", "D"], "quality": "min7", "rn": "ii7"},
        "G": {"chord": ["E", "G", "B", "D"], "quality": "min7", "rn": "vi7"},
        "b": {"chord": ["E", "G", "B", "D"], "quality": "min7", "rn": "iv7"},
        "e": {"chord": ["E", "G", "B", "D"], "quality": "min7", "rn": "i7"},
    },
    (2, 4, 8): {
        "A-": {"chord": ["D", "F-", "A-"], "quality": "aug6", "rn": "It"},
        "G#": {"chord": ["C##", "E", "G#"], "quality": "aug6", "rn": "It"},
        "a-": {"chord": ["D", "F-", "A-"], "quality": "aug6", "rn": "It"},
        "g#": {"chord": ["C##", "E", "G#"], "quality": "aug6", "rn": "It"},
    },
    (2, 4, 8, 10): {
        "A-": {
            "chord": ["B-", "D", "F-", "A-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "D": {"chord": ["E", "G#", "B-", "D"], "quality": "aug6", "rn": "Fr7"},
        "G#": {
            "chord": ["A#", "C##", "E", "G#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "a-": {
            "chord": ["B-", "D", "F-", "A-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "d": {"chord": ["E", "G#", "B-", "D"], "quality": "aug6", "rn": "Fr7"},
        "g#": {
            "chord": ["A#", "C##", "E", "G#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
    },
    (2, 4, 8, 11): {
        "A": {"chord": ["E", "G#", "B", "D"], "quality": "7", "rn": "V7"},
        "A-": {
            "chord": ["D", "F-", "A-", "C-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "B--": {
            "chord": ["F-", "A-", "C-", "E--"],
            "quality": "7",
            "rn": "V7",
        },
        "G#": {
            "chord": ["C##", "E", "G#", "B"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "a": {"chord": ["E", "G#", "B", "D"], "quality": "7", "rn": "V7"},
        "a-": {
            "chord": ["D", "F-", "A-", "C-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "g#": {
            "chord": ["C##", "E", "G#", "B"],
            "quality": "aug6",
            "rn": "Ger7",
        },
    },
    (2, 5, 6, 10): {
        "d#": {
            "chord": ["F#", "A#", "C##", "E#"],
            "quality": "aug7",
            "rn": "III+7",
        },
        "e-": {
            "chord": ["G-", "B-", "D", "F"],
            "quality": "aug7",
            "rn": "III+7",
        },
    },
    (2, 5, 7, 10): {
        "B-": {"chord": ["G", "B-", "D", "F"], "quality": "min7", "rn": "vi7"},
        "D#": {
            "chord": ["F##", "A#", "C##", "E#"],
            "quality": "min7",
            "rn": "iii7",
        },
        "E-": {
            "chord": ["G", "B-", "D", "F"],
            "quality": "min7",
            "rn": "iii7",
        },
        "F": {"chord": ["G", "B-", "D", "F"], "quality": "min7", "rn": "ii7"},
        "d": {"chord": ["G", "B-", "D", "F"], "quality": "min7", "rn": "iv7"},
        "g": {"chord": ["G", "B-", "D", "F"], "quality": "min7", "rn": "i7"},
    },
    (2, 5, 7, 11): {
        "B": {"chord": ["E#", "G", "B", "D"], "quality": "aug6", "rn": "Ger7"},
        "C": {"chord": ["G", "B", "D", "F"], "quality": "7", "rn": "V7"},
        "C-": {
            "chord": ["F", "A--", "C-", "E--"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "b": {"chord": ["E#", "G", "B", "D"], "quality": "aug6", "rn": "Ger7"},
        "b#": {
            "chord": ["F##", "A##", "C##", "E#"],
            "quality": "7",
            "rn": "V7",
        },
        "c": {"chord": ["G", "B", "D", "F"], "quality": "7", "rn": "V7"},
    },
    (2, 5, 8): {
        "D#": {"chord": ["C##", "E#", "G#"], "quality": "dim", "rn": "viio"},
        "E-": {"chord": ["D", "F", "A-"], "quality": "dim", "rn": "viio"},
        "b#": {"chord": ["C##", "E#", "G#"], "quality": "dim", "rn": "iio"},
        "c": {"chord": ["D", "F", "A-"], "quality": "dim", "rn": "iio"},
        "d#": {"chord": ["C##", "E#", "G#"], "quality": "dim", "rn": "viio"},
        "e-": {"chord": ["D", "F", "A-"], "quality": "dim", "rn": "viio"},
    },
    (2, 5, 8, 10): {
        "D": {
            "chord": ["G#", "B-", "D", "F"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "D#": {"chord": ["A#", "C##", "E#", "G#"], "quality": "7", "rn": "V7"},
        "E-": {"chord": ["B-", "D", "F", "A-"], "quality": "7", "rn": "V7"},
        "d": {
            "chord": ["G#", "B-", "D", "F"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "d#": {"chord": ["A#", "C##", "E#", "G#"], "quality": "7", "rn": "V7"},
        "e-": {"chord": ["B-", "D", "F", "A-"], "quality": "7", "rn": "V7"},
    },
    (2, 5, 8, 11): {
        "a": {
            "chord": ["G#", "B", "D", "F"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "b#": {
            "chord": ["A##", "C##", "E#", "G#"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "c": {
            "chord": ["B", "D", "F", "A-"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "d#": {
            "chord": ["C##", "E#", "G#", "B"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "e-": {
            "chord": ["D", "F", "A-", "C-"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "f#": {
            "chord": ["E#", "G#", "B", "D"],
            "quality": "dim7",
            "rn": "viio7",
        },
        "g-": {
            "chord": ["F", "A-", "C-", "E--"],
            "quality": "dim7",
            "rn": "viio7",
        },
    },
    (2, 5, 9): {
        "B-": {"chord": ["D", "F", "A"], "quality": "min", "rn": "iii"},
        "C": {"chord": ["D", "F", "A"], "quality": "min", "rn": "ii"},
        "F": {"chord": ["D", "F", "A"], "quality": "min", "rn": "vi"},
        "a": {"chord": ["D", "F", "A"], "quality": "min", "rn": "iv"},
        "d": {"chord": ["D", "F", "A"], "quality": "min", "rn": "i"},
    },
    (2, 5, 9, 10): {
        "B-": {"chord": ["B-", "D", "F", "A"], "quality": "maj7", "rn": "I7"},
        "F": {"chord": ["B-", "D", "F", "A"], "quality": "maj7", "rn": "IV7"},
        "d": {"chord": ["B-", "D", "F", "A"], "quality": "maj7", "rn": "VI7"},
    },
    (2, 5, 9, 11): {
        "C": {
            "chord": ["B", "D", "F", "A"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "a": {"chord": ["B", "D", "F", "A"], "quality": "hdim7", "rn": "iiø7"},
    },
    (2, 5, 10): {
        "A": {"chord": ["B-", "D", "F"], "quality": "maj", "rn": "N"},
        "B-": {"chord": ["B-", "D", "F"], "quality": "maj", "rn": "I"},
        "B--": {"chord": ["C--", "E--", "G--"], "quality": "maj", "rn": "N"},
        "D#": {"chord": ["A#", "C##", "E#"], "quality": "maj", "rn": "V"},
        "E-": {"chord": ["B-", "D", "F"], "quality": "maj", "rn": "V"},
        "F": {"chord": ["B-", "D", "F"], "quality": "maj", "rn": "IV"},
        "a": {"chord": ["B-", "D", "F"], "quality": "maj", "rn": "N"},
        "d": {"chord": ["B-", "D", "F"], "quality": "maj", "rn": "VI"},
        "d#": {"chord": ["A#", "C##", "E#"], "quality": "maj", "rn": "V"},
        "e-": {"chord": ["B-", "D", "F"], "quality": "maj", "rn": "V"},
    },
    (2, 5, 11): {
        "C": {"chord": ["B", "D", "F"], "quality": "dim", "rn": "viio"},
        "a": {"chord": ["B", "D", "F"], "quality": "dim", "rn": "iio"},
        "b#": {"chord": ["A##", "C##", "E#"], "quality": "dim", "rn": "viio"},
        "c": {"chord": ["B", "D", "F"], "quality": "dim", "rn": "viio"},
    },
    (2, 6, 7, 11): {
        "D": {"chord": ["G", "B", "D", "F#"], "quality": "maj7", "rn": "IV7"},
        "G": {"chord": ["G", "B", "D", "F#"], "quality": "maj7", "rn": "I7"},
        "b": {"chord": ["G", "B", "D", "F#"], "quality": "maj7", "rn": "VI7"},
    },
    (2, 6, 8, 11): {
        "A": {
            "chord": ["G#", "B", "D", "F#"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "B--": {
            "chord": ["A-", "C-", "E--", "G-"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "f#": {
            "chord": ["G#", "B", "D", "F#"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
        "g-": {
            "chord": ["A-", "C-", "E--", "G-"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (2, 6, 9): {
        "A": {"chord": ["D", "F#", "A"], "quality": "maj", "rn": "IV"},
        "B--": {"chord": ["E--", "G-", "B--"], "quality": "maj", "rn": "IV"},
        "C#": {"chord": ["D", "F#", "A"], "quality": "maj", "rn": "N"},
        "D": {"chord": ["D", "F#", "A"], "quality": "maj", "rn": "I"},
        "D-": {"chord": ["E--", "G-", "B--"], "quality": "maj", "rn": "N"},
        "G": {"chord": ["D", "F#", "A"], "quality": "maj", "rn": "V"},
        "c#": {"chord": ["D", "F#", "A"], "quality": "maj", "rn": "N"},
        "d-": {"chord": ["E--", "G-", "B--"], "quality": "maj", "rn": "N"},
        "f#": {"chord": ["D", "F#", "A"], "quality": "maj", "rn": "VI"},
        "g": {"chord": ["D", "F#", "A"], "quality": "maj", "rn": "V"},
        "g-": {"chord": ["E--", "G-", "B--"], "quality": "maj", "rn": "VI"},
    },
    (2, 6, 9, 10): {
        "g": {
            "chord": ["B-", "D", "F#", "A"],
            "quality": "aug7",
            "rn": "III+7",
        }
    },
    (2, 6, 9, 11): {
        "A": {"chord": ["B", "D", "F#", "A"], "quality": "min7", "rn": "ii7"},
        "B--": {
            "chord": ["C-", "E--", "G-", "B--"],
            "quality": "min7",
            "rn": "ii7",
        },
        "D": {"chord": ["B", "D", "F#", "A"], "quality": "min7", "rn": "vi7"},
        "G": {"chord": ["B", "D", "F#", "A"], "quality": "min7", "rn": "iii7"},
        "b": {"chord": ["B", "D", "F#", "A"], "quality": "min7", "rn": "i7"},
        "f#": {"chord": ["B", "D", "F#", "A"], "quality": "min7", "rn": "iv7"},
        "g-": {
            "chord": ["C-", "E--", "G-", "B--"],
            "quality": "min7",
            "rn": "iv7",
        },
    },
    (2, 6, 10): {
        "B": {"chord": ["F#", "A#", "C##"], "quality": "aug", "rn": "V+"},
        "C-": {"chord": ["G-", "B-", "D"], "quality": "aug", "rn": "V+"},
        "D#": {"chord": ["A#", "C##", "E##"], "quality": "aug", "rn": "V+"},
        "E-": {"chord": ["B-", "D", "F#"], "quality": "aug", "rn": "V+"},
        "G": {"chord": ["D", "F#", "A#"], "quality": "aug", "rn": "V+"},
        "b": {"chord": ["D", "F#", "A#"], "quality": "aug", "rn": "III+"},
        "d#": {"chord": ["F#", "A#", "C##"], "quality": "aug", "rn": "III+"},
        "e-": {"chord": ["G-", "B-", "D"], "quality": "aug", "rn": "III+"},
        "g": {"chord": ["B-", "D", "F#"], "quality": "aug", "rn": "III+"},
    },
    (2, 6, 11): {
        "A": {"chord": ["B", "D", "F#"], "quality": "min", "rn": "ii"},
        "B--": {"chord": ["C-", "E--", "G-"], "quality": "min", "rn": "ii"},
        "D": {"chord": ["B", "D", "F#"], "quality": "min", "rn": "vi"},
        "G": {"chord": ["B", "D", "F#"], "quality": "min", "rn": "iii"},
        "b": {"chord": ["B", "D", "F#"], "quality": "min", "rn": "i"},
        "f#": {"chord": ["B", "D", "F#"], "quality": "min", "rn": "iv"},
        "g-": {"chord": ["C-", "E--", "G-"], "quality": "min", "rn": "iv"},
    },
    (2, 7, 10): {
        "B-": {"chord": ["G", "B-", "D"], "quality": "min", "rn": "vi"},
        "D#": {"chord": ["F##", "A#", "C##"], "quality": "min", "rn": "iii"},
        "E-": {"chord": ["G", "B-", "D"], "quality": "min", "rn": "iii"},
        "F": {"chord": ["G", "B-", "D"], "quality": "min", "rn": "ii"},
        "d": {"chord": ["G", "B-", "D"], "quality": "min", "rn": "iv"},
        "g": {"chord": ["G", "B-", "D"], "quality": "min", "rn": "i"},
    },
    (2, 7, 11): {
        "C": {"chord": ["G", "B", "D"], "quality": "maj", "rn": "V"},
        "D": {"chord": ["G", "B", "D"], "quality": "maj", "rn": "IV"},
        "F#": {"chord": ["G", "B", "D"], "quality": "maj", "rn": "N"},
        "G": {"chord": ["G", "B", "D"], "quality": "maj", "rn": "I"},
        "G-": {"chord": ["A--", "C-", "E--"], "quality": "maj", "rn": "N"},
        "b": {"chord": ["G", "B", "D"], "quality": "maj", "rn": "VI"},
        "b#": {"chord": ["F##", "A##", "C##"], "quality": "maj", "rn": "V"},
        "c": {"chord": ["G", "B", "D"], "quality": "maj", "rn": "V"},
        "f#": {"chord": ["G", "B", "D"], "quality": "maj", "rn": "N"},
        "g-": {"chord": ["A--", "C-", "E--"], "quality": "maj", "rn": "N"},
    },
    (2, 8, 10): {
        "D": {"chord": ["G#", "B-", "D"], "quality": "aug6", "rn": "It"},
        "d": {"chord": ["G#", "B-", "D"], "quality": "aug6", "rn": "It"},
    },
    (2, 8, 11): {
        "A": {"chord": ["G#", "B", "D"], "quality": "dim", "rn": "viio"},
        "B--": {"chord": ["A-", "C-", "E--"], "quality": "dim", "rn": "viio"},
        "a": {"chord": ["G#", "B", "D"], "quality": "dim", "rn": "viio"},
        "f#": {"chord": ["G#", "B", "D"], "quality": "dim", "rn": "iio"},
        "g-": {"chord": ["A-", "C-", "E--"], "quality": "dim", "rn": "iio"},
    },
    (3, 4, 8, 11): {
        "B": {"chord": ["E", "G#", "B", "D#"], "quality": "maj7", "rn": "IV7"},
        "C-": {
            "chord": ["F-", "A-", "C-", "E-"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "E": {"chord": ["E", "G#", "B", "D#"], "quality": "maj7", "rn": "I7"},
        "F-": {
            "chord": ["F-", "A-", "C-", "E-"],
            "quality": "maj7",
            "rn": "I7",
        },
        "a-": {
            "chord": ["F-", "A-", "C-", "E-"],
            "quality": "maj7",
            "rn": "VI7",
        },
        "g#": {
            "chord": ["E", "G#", "B", "D#"],
            "quality": "maj7",
            "rn": "VI7",
        },
    },
    (3, 5, 8, 11): {
        "F#": {
            "chord": ["E#", "G#", "B", "D#"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "G-": {
            "chord": ["F", "A-", "C-", "E-"],
            "quality": "hdim7",
            "rn": "viiø7",
        },
        "d#": {
            "chord": ["E#", "G#", "B", "D#"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
        "e-": {
            "chord": ["F", "A-", "C-", "E-"],
            "quality": "hdim7",
            "rn": "iiø7",
        },
    },
    (3, 5, 9): {
        "A": {"chord": ["D#", "F", "A"], "quality": "aug6", "rn": "It"},
        "B--": {"chord": ["E-", "G--", "B--"], "quality": "aug6", "rn": "It"},
        "a": {"chord": ["D#", "F", "A"], "quality": "aug6", "rn": "It"},
    },
    (3, 5, 9, 11): {
        "A": {"chord": ["B", "D#", "F", "A"], "quality": "aug6", "rn": "Fr7"},
        "B--": {
            "chord": ["C-", "E-", "G--", "B--"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "D#": {
            "chord": ["E#", "G##", "B", "D#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "E-": {
            "chord": ["F", "A", "C-", "E-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "a": {"chord": ["B", "D#", "F", "A"], "quality": "aug6", "rn": "Fr7"},
        "d#": {
            "chord": ["E#", "G##", "B", "D#"],
            "quality": "aug6",
            "rn": "Fr7",
        },
        "e-": {
            "chord": ["F", "A", "C-", "E-"],
            "quality": "aug6",
            "rn": "Fr7",
        },
    },
    (3, 6, 7, 11): {
        "e": {
            "chord": ["G", "B", "D#", "F#"],
            "quality": "aug7",
            "rn": "III+7",
        }
    },
    (3, 6, 8, 11): {
        "B": {
            "chord": ["G#", "B", "D#", "F#"],
            "quality": "min7",
            "rn": "vi7",
        },
        "C-": {
            "chord": ["A-", "C-", "E-", "G-"],
            "quality": "min7",
            "rn": "vi7",
        },
        "E": {
            "chord": ["G#", "B", "D#", "F#"],
            "quality": "min7",
            "rn": "iii7",
        },
        "F#": {
            "chord": ["G#", "B", "D#", "F#"],
            "quality": "min7",
            "rn": "ii7",
        },
        "F-": {
            "chord": ["A-", "C-", "E-", "G-"],
            "quality": "min7",
            "rn": "iii7",
        },
        "G-": {
            "chord": ["A-", "C-", "E-", "G-"],
            "quality": "min7",
            "rn": "ii7",
        },
        "a-": {
            "chord": ["A-", "C-", "E-", "G-"],
            "quality": "min7",
            "rn": "i7",
        },
        "d#": {
            "chord": ["G#", "B", "D#", "F#"],
            "quality": "min7",
            "rn": "iv7",
        },
        "e-": {
            "chord": ["A-", "C-", "E-", "G-"],
            "quality": "min7",
            "rn": "iv7",
        },
        "g#": {
            "chord": ["G#", "B", "D#", "F#"],
            "quality": "min7",
            "rn": "i7",
        },
    },
    (3, 6, 9): {
        "E": {"chord": ["D#", "F#", "A"], "quality": "dim", "rn": "viio"},
        "F-": {"chord": ["E-", "G-", "B--"], "quality": "dim", "rn": "viio"},
        "c#": {"chord": ["D#", "F#", "A"], "quality": "dim", "rn": "iio"},
        "d-": {"chord": ["E-", "G-", "B--"], "quality": "dim", "rn": "iio"},
        "e": {"chord": ["D#", "F#", "A"], "quality": "dim", "rn": "viio"},
    },
    (3, 6, 9, 11): {
        "D#": {
            "chord": ["G##", "B", "D#", "F#"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "E": {"chord": ["B", "D#", "F#", "A"], "quality": "7", "rn": "V7"},
        "E-": {
            "chord": ["A", "C-", "E-", "G-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "F-": {"chord": ["C-", "E-", "G-", "B--"], "quality": "7", "rn": "V7"},
        "d#": {
            "chord": ["G##", "B", "D#", "F#"],
            "quality": "aug6",
            "rn": "Ger7",
        },
        "e": {"chord": ["B", "D#", "F#", "A"], "quality": "7", "rn": "V7"},
        "e-": {
            "chord": ["A", "C-", "E-", "G-"],
            "quality": "aug6",
            "rn": "Ger7",
        },
    },
    (3, 6, 10): {
        "B": {"chord": ["D#", "F#", "A#"], "quality": "min", "rn": "iii"},
        "C#": {"chord": ["D#", "F#", "A#"], "quality": "min", "rn": "ii"},
        "C-": {"chord": ["E-", "G-", "B-"], "quality": "min", "rn": "iii"},
        "D-": {"chord": ["E-", "G-", "B-"], "quality": "min", "rn": "ii"},
        "F#": {"chord": ["D#", "F#", "A#"], "quality": "min", "rn": "vi"},
        "G-": {"chord": ["E-", "G-", "B-"], "quality": "min", "rn": "vi"},
        "a#": {"chord": ["D#", "F#", "A#"], "quality": "min", "rn": "iv"},
        "b-": {"chord": ["E-", "G-", "B-"], "quality": "min", "rn": "iv"},
        "d#": {"chord": ["D#", "F#", "A#"], "quality": "min", "rn": "i"},
        "e-": {"chord": ["E-", "G-", "B-"], "quality": "min", "rn": "i"},
    },
    (3, 6, 10, 11): {
        "B": {"chord": ["B", "D#", "F#", "A#"], "quality": "maj7", "rn": "I7"},
        "C-": {
            "chord": ["C-", "E-", "G-", "B-"],
            "quality": "maj7",
            "rn": "I7",
        },
        "F#": {
            "chord": ["B", "D#", "F#", "A#"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "G-": {
            "chord": ["C-", "E-", "G-", "B-"],
            "quality": "maj7",
            "rn": "IV7",
        },
        "d#": {
            "chord": ["B", "D#", "F#", "A#"],
            "quality": "maj7",
            "rn": "VI7",
        },
        "e-": {
            "chord": ["C-", "E-", "G-", "B-"],
            "quality": "maj7",
            "rn": "VI7",
        },
    },
    (3, 6, 11): {
        "B": {"chord": ["B", "D#", "F#"], "quality": "maj", "rn": "I"},
        "B-": {"chord": ["C-", "E-", "G-"], "quality": "maj", "rn": "N"},
        "C-": {"chord": ["C-", "E-", "G-"], "quality": "maj", "rn": "I"},
        "E": {"chord": ["B", "D#", "F#"], "quality": "maj", "rn": "V"},
        "F#": {"chord": ["B", "D#", "F#"], "quality": "maj", "rn": "IV"},
        "F-": {"chord": ["C-", "E-", "G-"], "quality": "maj", "rn": "V"},
        "G-": {"chord": ["C-", "E-", "G-"], "quality": "maj", "rn": "IV"},
        "a#": {"chord": ["B", "D#", "F#"], "quality": "maj", "rn": "N"},
        "b-": {"chord": ["C-", "E-", "G-"], "quality": "maj", "rn": "N"},
        "d#": {"chord": ["B", "D#", "F#"], "quality": "maj", "rn": "VI"},
        "e": {"chord": ["B", "D#", "F#"], "quality": "maj", "rn": "V"},
        "e-": {"chord": ["C-", "E-", "G-"], "quality": "maj", "rn": "VI"},
    },
    (3, 7, 10): {
        "A-": {"chord": ["E-", "G", "B-"], "quality": "maj", "rn": "V"},
        "B-": {"chord": ["E-", "G", "B-"], "quality": "maj", "rn": "IV"},
        "D": {"chord": ["E-", "G", "B-"], "quality": "maj", "rn": "N"},
        "D#": {"chord": ["D#", "F##", "A#"], "quality": "maj", "rn": "I"},
        "E-": {"chord": ["E-", "G", "B-"], "quality": "maj", "rn": "I"},
        "G#": {"chord": ["D#", "F##", "A#"], "quality": "maj", "rn": "V"},
        "a-": {"chord": ["E-", "G", "B-"], "quality": "maj", "rn": "V"},
        "d": {"chord": ["E-", "G", "B-"], "quality": "maj", "rn": "N"},
        "g": {"chord": ["E-", "G", "B-"], "quality": "maj", "rn": "VI"},
        "g#": {"chord": ["D#", "F##", "A#"], "quality": "maj", "rn": "V"},
    },
    (3, 7, 10, 11): {
        "a-": {
            "chord": ["C-", "E-", "G", "B-"],
            "quality": "aug7",
            "rn": "III+7",
        },
        "g#": {
            "chord": ["B", "D#", "F##", "A#"],
            "quality": "aug7",
            "rn": "III+7",
        },
    },
    (3, 7, 11): {
        "A-": {"chord": ["E-", "G", "B"], "quality": "aug", "rn": "V+"},
        "C": {"chord": ["G", "B", "D#"], "quality": "aug", "rn": "V+"},
        "E": {"chord": ["B", "D#", "F##"], "quality": "aug", "rn": "V+"},
        "F-": {"chord": ["C-", "E-", "G"], "quality": "aug", "rn": "V+"},
        "G#": {"chord": ["D#", "F##", "A##"], "quality": "aug", "rn": "V+"},
        "a-": {"chord": ["C-", "E-", "G"], "quality": "aug", "rn": "III+"},
        "b#": {"chord": ["D#", "F##", "A##"], "quality": "aug", "rn": "III+"},
        "c": {"chord": ["E-", "G", "B"], "quality": "aug", "rn": "III+"},
        "e": {"chord": ["G", "B", "D#"], "quality": "aug", "rn": "III+"},
        "g#": {"chord": ["B", "D#", "F##"], "quality": "aug", "rn": "III+"},
    },
    (3, 8, 11): {
        "B": {"chord": ["G#", "B", "D#"], "quality": "min", "rn": "vi"},
        "C-": {"chord": ["A-", "C-", "E-"], "quality": "min", "rn": "vi"},
        "E": {"chord": ["G#", "B", "D#"], "quality": "min", "rn": "iii"},
        "F#": {"chord": ["G#", "B", "D#"], "quality": "min", "rn": "ii"},
        "F-": {"chord": ["A-", "C-", "E-"], "quality": "min", "rn": "iii"},
        "G-": {"chord": ["A-", "C-", "E-"], "quality": "min", "rn": "ii"},
        "a-": {"chord": ["A-", "C-", "E-"], "quality": "min", "rn": "i"},
        "d#": {"chord": ["G#", "B", "D#"], "quality": "min", "rn": "iv"},
        "e-": {"chord": ["A-", "C-", "E-"], "quality": "min", "rn": "iv"},
        "g#": {"chord": ["G#", "B", "D#"], "quality": "min", "rn": "i"},
    },
    (3, 9, 11): {
        "D#": {"chord": ["G##", "B", "D#"], "quality": "aug6", "rn": "It"},
        "E-": {"chord": ["A", "C-", "E-"], "quality": "aug6", "rn": "It"},
        "d#": {"chord": ["G##", "B", "D#"], "quality": "aug6", "rn": "It"},
        "e-": {"chord": ["A", "C-", "E-"], "quality": "aug6", "rn": "It"},
    },
    (4, 6, 10): {
        "B-": {"chord": ["E", "G-", "B-"], "quality": "aug6", "rn": "It"},
        "a#": {"chord": ["D##", "F#", "A#"], "quality": "aug6", "rn": "It"},
        "b-": {"chord": ["E", "G-", "B-"], "quality": "aug6", "rn": "It"},
    },
    (4, 7, 10): {
        "F": {"chord": ["E", "G", "B-"], "quality": "dim", "rn": "viio"},
        "d": {"chord": ["E", "G", "B-"], "quality": "dim", "rn": "iio"},
        "e#": {"chord": ["D##", "F##", "A#"], "quality": "dim", "rn": "viio"},
        "f": {"chord": ["E", "G", "B-"], "quality": "dim", "rn": "viio"},
    },
    (4, 7, 11): {
        "C": {"chord": ["E", "G", "B"], "quality": "min", "rn": "iii"},
        "D": {"chord": ["E", "G", "B"], "quality": "min", "rn": "ii"},
        "G": {"chord": ["E", "G", "B"], "quality": "min", "rn": "vi"},
        "b": {"chord": ["E", "G", "B"], "quality": "min", "rn": "iv"},
        "e": {"chord": ["E", "G", "B"], "quality": "min", "rn": "i"},
    },
    (4, 8, 11): {
        "A": {"chord": ["E", "G#", "B"], "quality": "maj", "rn": "V"},
        "B": {"chord": ["E", "G#", "B"], "quality": "maj", "rn": "IV"},
        "B--": {"chord": ["F-", "A-", "C-"], "quality": "maj", "rn": "V"},
        "C-": {"chord": ["F-", "A-", "C-"], "quality": "maj", "rn": "IV"},
        "D#": {"chord": ["E", "G#", "B"], "quality": "maj", "rn": "N"},
        "E": {"chord": ["E", "G#", "B"], "quality": "maj", "rn": "I"},
        "E-": {"chord": ["F-", "A-", "C-"], "quality": "maj", "rn": "N"},
        "F-": {"chord": ["F-", "A-", "C-"], "quality": "maj", "rn": "I"},
        "a": {"chord": ["E", "G#", "B"], "quality": "maj", "rn": "V"},
        "a-": {"chord": ["F-", "A-", "C-"], "quality": "maj", "rn": "VI"},
        "d#": {"chord": ["E", "G#", "B"], "quality": "maj", "rn": "N"},
        "e-": {"chord": ["F-", "A-", "C-"], "quality": "maj", "rn": "N"},
        "g#": {"chord": ["E", "G#", "B"], "quality": "maj", "rn": "VI"},
    },
    (5, 7, 11): {
        "B": {"chord": ["E#", "G", "B"], "quality": "aug6", "rn": "It"},
        "C-": {"chord": ["F", "A--", "C-"], "quality": "aug6", "rn": "It"},
        "b": {"chord": ["E#", "G", "B"], "quality": "aug6", "rn": "It"},
    },
    (5, 8, 11): {
        "F#": {"chord": ["E#", "G#", "B"], "quality": "dim", "rn": "viio"},
        "G-": {"chord": ["F", "A-", "C-"], "quality": "dim", "rn": "viio"},
        "d#": {"chord": ["E#", "G#", "B"], "quality": "dim", "rn": "iio"},
        "e-": {"chord": ["F", "A-", "C-"], "quality": "dim", "rn": "iio"},
        "f#": {"chord": ["E#", "G#", "B"], "quality": "dim", "rn": "viio"},
        "g-": {"chord": ["F", "A-", "C-"], "quality": "dim", "rn": "viio"},
    },
}
