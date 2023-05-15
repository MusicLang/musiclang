"""Run the network to annotate an unseen musical input (inference)."""

import os

import music21
import numpy as np
import pandas as pd
import re


from . import __version__
from .chord_vocabulary import frompcset, cosineSimilarity
from .cache import forceTonicization, getTonicizationScaleDegree
from .score_parser import parseScore, m21Parse
from .input_representations import available_representations as availableInputs
from .output_representations import (
    available_representations as availableOutputs,
)
from .utils import tensorflowGPUHack, disableGPU, padToSequenceLength
from tensorflow import keras

modelPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'AugmentedNet.hdf5')

MODEL = None

def get_model():
    global MODEL
    print('LOADING MODEL')
    if MODEL is not None:
        return MODEL
    else:
        disableGPU()
        MODEL = keras.models.load_model(modelPath)
        return MODEL



inversions = {
    "triad": {
        0: "",
        1: "6",
        2: "64",
    },
    "seventh": {
        0: "7",
        1: "65",
        2: "43",
        3: "2",
    },
}


def formatChordLabel(cl):
    """Format the chord label for end-user presentation.

    Parameters
    ----------
    cl :
        

    Returns
    -------

    """
    # The only change I can think of: Cmaj -> C
    cl = cl.replace("maj", "") if cl.endswith("maj") else cl
    cl = cl.replace("-", "b")
    return cl


def formatRomanNumeral(rn, key):
    """Format the Roman numeral label for end-user presentation.

    Parameters
    ----------
    rn :
        
    key :
        

    Returns
    -------

    """
    # Something of "I" and "I" of something
    if rn == "I/I":
        rn = "I"
    return rn


def solveChordSegmentation(df):
    """

    Parameters
    ----------
    df :
        

    Returns
    -------

    """
    return df[df.HarmonicRhythm7 == 0].dropna()


def resolveRomanNumeralCosine(b, t, a, s, pcs, key, numerator, tonicizedKey):
    """

    Parameters
    ----------
    b :
        
    t :
        
    a :
        
    s :
        
    pcs :
        
    key :
        
    numerator :
        
    tonicizedKey :
        

    Returns
    -------

    """
    pcsetVector = np.zeros(12)
    chord = music21.chord.Chord(f"{b}2 {t}3 {a}4 {s}5")
    for n in chord.pitches:
        pcsetVector[n.pitchClass] += 1
    for pc in pcs:
        pcsetVector[pc] += 1
    chordNumerator = music21.roman.RomanNumeral(
        numerator.replace("Cad", "Cad64"), tonicizedKey
    ).pitchClasses
    for pc in chordNumerator:
        pcsetVector[pc] += 1
    smallestDistance = -2
    for pcs in frompcset:
        v2 = np.zeros(12)
        for p in pcs:
            v2[p] = 1
        similarity = cosineSimilarity(pcsetVector, v2)
        if similarity > smallestDistance:
            pcset = pcs
            smallestDistance = similarity
    if tonicizedKey not in frompcset[pcset]:
        # print("Forcing a tonicization")
        candidateKeys = list(frompcset[pcset].keys())
        # prioritize modal mixture
        tonicizedKey = forceTonicization(key, candidateKeys)
    rnfigure = frompcset[pcset][tonicizedKey]["rn"]
    chord = frompcset[pcset][tonicizedKey]["chord"]
    quality = frompcset[pcset][tonicizedKey]["quality"]
    chordtype = "seventh" if len(pcset) == 4 else "triad"
    # if you can't find the predicted bass
    # in the pcset, assume root position
    inv = chord.index(b) if b in chord else 0
    invfigure = inversions[chordtype][inv]
    if invfigure in ["65", "43", "2"]:
        rnfigure = rnfigure.replace("7", invfigure)
    elif invfigure in ["6", "64"]:
        rnfigure += invfigure
    rn = rnfigure
    if numerator == "Cad" and inv == 2:
        rn = "Cad64"
    if tonicizedKey != key:
        denominator = getTonicizationScaleDegree(key, tonicizedKey)
        rn = f"{rn}/{denominator}"
    chordLabel = f"{chord[0]}{quality}"
    if inv != 0:
        chordLabel += f"/{chord[inv]}"
    return rn, chordLabel


def generateRomanText(h, ts):
    """

    Parameters
    ----------
    h :
        
    ts :
        

    Returns
    -------

    """
    metadata = h.metadata
    metadata.composer = metadata.composer or "Unknown"
    metadata.title = metadata.title or "Unknown"
    composer = metadata.composer.split("\n")[0]
    title = metadata.title.split("\n")[0]
    rntxt = f"""\
Composer: {composer}
Title: {title}
Analyst: AugmentedNet v{__version__} - https://github.com/napulen/AugmentedNet
"""
    currentMeasure = -1
    for n in h.stream().flat.notes:
        if not n.lyric:
            continue
        rn = n.lyric.split()[0]
        key = ""
        measure = n.measureNumber
        beat = float(n.beat)
        if beat.is_integer():
            beat = int(beat)
        newts = ts.get((measure, beat), None)
        if newts:
            rntxt += f"\nTime Signature: {newts}\n"
        if ":" in rn:
            key, rn = rn.split(":")
        if measure != currentMeasure:
            rntxt += f"\nm{measure}"
            currentMeasure = measure
        if beat != 1:
            rntxt += f" b{round(beat, 3)}"
        if key:
            rntxt += f" {key.replace('-', 'b')}:"
        rntxt += f" {rn}"
    return rntxt


def predict(model, inputPath):
    """

    Parameters
    ----------
    model :
        
    inputPath :
        

    Returns
    -------

    """
    df = parseScore(inputPath)
    inputs = [l.name.rsplit("_")[1] for l in model.inputs]
    encodedInputs = [availableInputs[i](df) for i in inputs]
    outputLayers = [l.name.split("/")[0] for l in model.outputs]
    seqlen = model.inputs[0].shape[1]
    modelInputs = [
        padToSequenceLength(i.array, seqlen, value=-1) for i in encodedInputs
    ]
    predictions = model.predict(modelInputs)
    predictions = [p.reshape(1, -1, p.shape[2]) for p in predictions]
    dfdict = {}
    for outputRepr, pred in zip(outputLayers, predictions):
        predOnehot = np.argmax(pred[0], axis=1).reshape(-1, 1)
        decoded = availableOutputs[outputRepr].decode(predOnehot)
        dfdict[outputRepr] = decoded
    dfout = pd.DataFrame(dfdict)
    scoreLength = len(dfout.index)
    paddedIndex = np.full((scoreLength,), np.nan)
    paddedMeasure = np.full((scoreLength,), np.nan)
    paddedIndex[: len(df.index)] = df.index
    paddedMeasure[: len(df.s_measure)] = df.s_measure
    dfout["offset"] = paddedIndex
    dfout["measure"] = paddedMeasure
    chords = solveChordSegmentation(dfout)
    #s = music21.converter.parse(inputPath, forceSource=True)
    s = m21Parse(inputPath)
    ts = {
        (ts.measureNumber, float(ts.beat)): ts.ratioString
        for ts in s.flat.getElementsByClass("TimeSignature")
    }
    schord = s.chordify().flat.notesAndRests
    schord.metadata = s.metadata
    # remove all lyrics from score
    # for note in s.recurse().notes:
    #     note.lyrics = []
    prevkey = ""
    for analysis in chords.itertuples():
        notes = []
        for n in schord.getElementsByOffset(analysis.offset):
            if isinstance(n, music21.note.Note):
                notes.append((n, n.pitch.midi))
            elif isinstance(n, music21.chord.Chord) and not isinstance(
                n, music21.harmony.NoChord
            ):
                notes.append((n, n[0].pitch.midi))
        if not notes:
            continue
        bass = sorted(notes, key=lambda n: n[1])[0][0]
        thiskey = analysis.LocalKey38
        tonicizedKey = analysis.TonicizedKey38
        pcset = analysis.PitchClassSet121
        numerator = analysis.RomanNumeral31
        rn2, chordLabel = resolveRomanNumeralCosine(
            analysis.Bass35,
            analysis.Tenor35,
            analysis.Alto35,
            analysis.Soprano35,
            pcset,
            thiskey,
            numerator,
            tonicizedKey,
        )
        if thiskey != prevkey:
            rn2fig = f"{thiskey}:{rn2}"
            prevkey = thiskey
        else:
            rn2fig = rn2
        bass.addLyric(formatRomanNumeral(rn2fig, thiskey))
        bass.addLyric(formatChordLabel(chordLabel))
    rntxt = generateRomanText(schord, ts)
    filename, _ = inputPath.rsplit(".", 1)
    annotatedRomanText = f"{filename}_annotated.rntxt"
    with open(annotatedRomanText, "w") as fd:
        fd.write(rntxt)


def infer_chords(inputPath, useGpu=False):
    """

    Parameters
    ----------
    inputPath :
        
    useGpu :
         (Default value = False)

    Returns
    -------

    """

    if not os.path.isdir(inputPath):
        predict(get_model(), inputPath)
    for root, _, files in os.walk(inputPath):
        for f in files:
            name, ext = os.path.splitext(f)
            if ext not in [".mxl", ".xml", ".musicxml", ".krn"]:
                continue
            if "_annotated" in name:
                # do not recursively annotate an annotated_file
                continue
            filepath = os.path.join(root, f)
            predict(get_model(), inputPath=filepath)

