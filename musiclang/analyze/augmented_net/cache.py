"""Several cached music21 objects and functions for performance."""

from music21.key import Key
from music21.pitch import Pitch
from music21.interval import Interval
from .keydistance import weberEuclidean as _we
from .keydistance import getTonicizationScaleDegree as _gtsd

_transposeKey = {}
_transposePitch = {}
_transposePcSet = {}
_pitchObj = {}
_keyObj = {}
_intervalObj = {}
_weberEuclidean = {}
_getTonicizationScaleDegree = {}


def weberEuclidean(k1, k2):
    """A cached version of keydistance.weberEuclidean.

    Parameters
    ----------
    k1 :
        
    k2 :
        

    Returns
    -------

    """
    duple = (k1, k2)
    if duple in _weberEuclidean:
        return _weberEuclidean[duple]
    distance = _we(k1, k2)
    _weberEuclidean[duple] = distance
    return distance


def getTonicizationScaleDegree(localKey, tonicizedKey):
    """A cached version of keydistance.weberEuclidean.

    Parameters
    ----------
    localKey :
        
    tonicizedKey :
        

    Returns
    -------

    """
    duple = (localKey, tonicizedKey)
    if duple in _getTonicizationScaleDegree:
        return _getTonicizationScaleDegree[duple]
    degree = _gtsd(localKey, tonicizedKey)
    _getTonicizationScaleDegree[duple] = degree
    return degree


def forceTonicization(localKey, candidateKeys):
    """Forces a tonicization of candidateKey that exist in vocabulary.

    Parameters
    ----------
    localKey :
        
    candidateKeys :
        

    Returns
    -------

    """
    tonicizationDistance = 1337
    tonicization = ""
    for candidateKey in candidateKeys:
        distance = weberEuclidean(localKey, candidateKey)
        # print(f"\t{localKey} -> {candidateKey} = {distance}")
        scaleDegree = getTonicizationScaleDegree(localKey, candidateKey)
        if scaleDegree not in ["i", "III"]:
            # Slight preference for parallel minor and relative major
            distance *= 1.05
        if scaleDegree not in ["i", "I", "III", "iv", "IV", "v", "V"]:
            distance *= 1.05
        if distance < tonicizationDistance:
            tonicization = candidateKey
            tonicizationDistance = distance
    return tonicization


def TransposeKey(key, interval):
    """Transposes a key based on an interval string (e.g., 'm3').

    Parameters
    ----------
    key :
        
    interval :
        

    Returns
    -------

    """
    duple = (key, interval)
    if duple in _transposeKey:
        return _transposeKey[duple]
    keyObj = m21Key(key)
    transposed = keyObj.transpose(interval).tonicPitchNameWithCase
    _transposeKey[duple] = transposed
    return transposed


def TransposePitch(pitch, interval):
    """Transposes a pitch based on an interval string (e.g., 'm3').

    Parameters
    ----------
    pitch :
        
    interval :
        

    Returns
    -------

    """
    duple = (pitch, interval)
    if duple in _transposePitch:
        return _transposePitch[duple]
    pitchObj = m21Pitch(pitch)
    transposed = pitchObj.transpose(interval).nameWithOctave
    _transposePitch[duple] = transposed
    return transposed


def TransposePcSet(pcset, interval):
    """Transposes a pcset based on an interval string (e.g., 'm3').

    Parameters
    ----------
    pcset :
        
    interval :
        

    Returns
    -------

    """
    duple = (pcset, interval)
    if duple in _transposePcSet:
        return _transposePcSet[duple]
    semitones = m21IntervalStr(interval).semitones
    transposed = [(x + semitones) % 12 for x in pcset]
    transposed = tuple(sorted(transposed))
    _transposePcSet[duple] = transposed
    return transposed


def m21IntervalStr(interval):
    """A cached interval object, based on the string (e.g., 'm3').

    Parameters
    ----------
    interval :
        

    Returns
    -------

    """
    if interval in _intervalObj:
        return _intervalObj[interval]
    intervalObj = Interval(interval)
    _intervalObj[interval] = intervalObj
    return intervalObj


def m21Interval(pitch1, pitch2):
    """A cached interval object, computed from two pitches.

    Parameters
    ----------
    pitch1 :
        
    pitch2 :
        

    Returns
    -------

    """
    duple = (pitch1, pitch2)
    if duple in _intervalObj:
        return _intervalObj[duple]
    p1, p2 = m21Pitch(pitch1), m21Pitch(pitch2)
    intervalObj = Interval(p1, p2)
    _intervalObj[duple] = intervalObj
    return intervalObj


def m21Key(key):
    """A cached key object, based on a string (e.g., 'c#').

    Parameters
    ----------
    key :
        

    Returns
    -------

    """
    if key in _keyObj:
        return _keyObj[key]
    keyObj = Key(key)
    _keyObj[key] = keyObj
    return keyObj


def m21Pitch(pitch):
    """A cached pitch object, based on a string (e.g., 'C#').

    Parameters
    ----------
    pitch :
        

    Returns
    -------

    """
    if pitch in _pitchObj:
        return _pitchObj[pitch]
    pitchObj = Pitch(pitch)
    _pitchObj[pitch] = pitchObj
    return pitchObj
