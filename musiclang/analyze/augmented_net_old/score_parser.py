"""Turns a MusicXML file into a pandas DataFrame."""

import music21
from music21.note import Rest
import numpy as np
import pandas as pd

from .cache import m21Interval

FLOATSCALE = 4

# Sixteenth notes
FRAMEBASENOTE = 32
FIXEDOFFSET = round(4.0 / FRAMEBASENOTE, FLOATSCALE)

S_COLUMNS = [
    "s_offset",
    "s_duration",
    "s_measure",
    "s_notes",
    "s_intervals",
    "s_isOnset",
]

S_LISTTYPE_COLUMNS = [
    "s_notes",
    "s_intervals",
    "s_isOnset",
]


def m21Parse(f, fmt=None, remove_perc=True):
    """

    Parameters
    ----------
    f :

    fmt :
         (Default value = None)

    Returns
    -------

    """
    s = music21.converter.parse(f, format=fmt, forceSource=True)
    if remove_perc:

        for el in s.recurse():
            if set(el.classes).intersection(['PercussionChord', 'Unpitched']):  # or 'Piano'
                # el.activeSite.replace(el, instrument.Violin())
                el.activeSite.remove(el)

        # perc = [
        #     p
        #     for p in s.parts
        #     if list(p.recurse().getElementsByClass(["PercussionClef", "PercussionChord"]))
        # ]
        # s.remove(perc, recurse=True)
    return s


def from_tsv(tsv, sep="\t"):
    """

    Parameters
    ----------
    tsv :
        
    sep :
         (Default value = "\t")

    Returns
    -------

    """
    df = pd.read_csv(tsv, sep=sep)
    df.set_index("s_offset", inplace=True)
    for col in S_LISTTYPE_COLUMNS:
        df[col] = df[col].apply(eval)
    return df


def _measureNumberShift(m21Score):
    """

    Parameters
    ----------
    m21Score :
        

    Returns
    -------

    """
    firstMeasure = m21Score.parts[0].measure(0) or m21Score.parts[0].measure(1)
    isAnacrusis = True if firstMeasure.paddingLeft > 0.0 else False
    if isAnacrusis and firstMeasure.number == 1:
        measureNumberShift = -1
    else:
        measureNumberShift = 0
    return measureNumberShift


def _lastOffset(m21Score):
    """

    Parameters
    ----------
    m21Score :
        

    Returns
    -------

    """
    lastMeasure = m21Score.parts[0].measure(-1)
    filledDuration = lastMeasure.duration.quarterLength / float(
        lastMeasure.barDurationProportion()
    )
    lastOffset = lastMeasure.offset + filledDuration
    return lastOffset


def _initialDataFrame(s, fmt=None):
    """Parses a score and produces a pandas dataframe.
    
    The features obtained are the note names, their position in the score,
    measure number, and their ties (in case something fancy needs to be done,
    with the tie information).

    Parameters
    ----------
    s :
        
    fmt :
         (Default value = None)

    Returns
    -------

    """
    dfdict = {col: [] for col in S_COLUMNS}
    measureNumberShift = _measureNumberShift(s)
    for c in s.chordify().flat.notesAndRests:
        dfdict["s_offset"].append(round(float(c.offset), FLOATSCALE))
        dfdict["s_duration"].append(round(float(c.quarterLength), FLOATSCALE))
        dfdict["s_measure"].append(c.measureNumber + measureNumberShift)
        if isinstance(c, Rest):
            # We need dummy entries for rests at the beginning of a measure
            dfdict["s_notes"].append(np.nan)
            dfdict["s_intervals"].append(np.nan)
            dfdict["s_isOnset"].append(np.nan)
            continue
        dfdict["s_notes"].append([n.pitch.nameWithOctave for n in c])
        pitches = [p.nameWithOctave for p in c.pitches]
        intervs = [m21Interval(pitches[0], p).simpleName for p in pitches[1:]]
        dfdict["s_intervals"].append(intervs)
        onsets = [(not n.tie or n.tie.type == "start") for n in c]
        dfdict["s_isOnset"].append(onsets)
    df = pd.DataFrame(dfdict)
    currentLastOffset = float(df.tail(1).s_offset) + float(
        df.tail(1).s_duration
    )
    deltaDuration = _lastOffset(s) - currentLastOffset
    df.loc[len(df) - 1, "s_duration"] += deltaDuration
    df.set_index("s_offset", inplace=True)
    df = df[~df.index.duplicated()]

    return df


def _reindexDataFrame(df, fixedOffset=FIXEDOFFSET):
    """Reindexes a dataframe according to a fixed note-value.
    
    It could be said that the DataFrame produced by parseScore
    is a "salami-sliced" version of the score. This is intuitive
    for humans, but does not really work in machine learning.
    
    What works, is to slice the score in fixed note intervals,
    for example, a sixteenth note. This reindex function does
    exactly that.

    Parameters
    ----------
    df :
        
    fixedOffset :
         (Default value = FIXEDOFFSET)

    Returns
    -------

    """
    firstRow = df.head(1)
    lastRow = df.tail(1)
    minOffset = firstRow.index.to_numpy()[0]
    maxOffset = (lastRow.index + lastRow.s_duration).to_numpy()[0]
    newIndex = np.arange(minOffset, maxOffset, fixedOffset)
    # All operations done over the full index, i.e., fixed-timesteps
    # plus original onsets. Later, original onsets (e.g., triplets)
    # are removed and just the fixed-timesteps are kept
    df = df.reindex(index=df.index.union(newIndex))
    df.s_notes.fillna(method="ffill", inplace=True)
    df.s_notes.fillna(method="bfill", inplace=True)
    # the "isOnset" column is hard to generate in fixed-timesteps
    # however, it allows us to encode a "hold" symbol if we wanted to
    newCol = pd.Series(
        [[False] * n for n in df.s_notes.str.len().to_list()], index=df.index
    )
    df.s_isOnset.fillna(value=newCol, inplace=True)
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)
    df = df.reindex(index=newIndex)
    return df


def parseScore(f, fmt=None, fixedOffset=FIXEDOFFSET, eventBased=False):
    """

    Parameters
    ----------
    f :
        
    fmt :
         (Default value = None)
    fixedOffset :
         (Default value = FIXEDOFFSET)
    eventBased :
         (Default value = False)

    Returns
    -------

    """

    # Step 0: Use music21 to parse the score
    s = m21Parse(f, fmt)

    # Step 1: Parse and produce a salami-sliced dataset
    df = _initialDataFrame(s, fmt)
    # Step 2: Turn salami-slice into fixed-duration steps
    if not eventBased:
        df = _reindexDataFrame(df, fixedOffset=fixedOffset)
    return df
