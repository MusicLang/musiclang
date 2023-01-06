"""Generate pkl files for every tsv training example."""

import os
import pandas as pd
import numpy as np
import tensorflow as tf

from . import cli
from . import joint_parser
from .cache import TransposeKey
from .common import DATASETSUMMARYFILE
from .feature_representation import TRANSPOSITIONKEYS, INTERVALCLASSES
from .input_representations import (
    available_representations as availableInputs,
)
from .output_representations import (
    available_representations as availableOutputs,
)
from .utils import padToSequenceLength, DynamicArray


def _getTranspositions(df, transpositionKeys=TRANSPOSITIONKEYS):
    """

    Parameters
    ----------
    df :
        
    transpositionKeys :
         (Default value = TRANSPOSITIONKEYS)

    Returns
    -------

    """
    tonicizedKeys = df.a_localKey.to_list() + df.a_tonicizedKey.to_list()
    tonicizedKeys = set(tonicizedKeys)
    ret = []
    for interval in INTERVALCLASSES:
        transposed = [TransposeKey(k, interval) for k in tonicizedKeys]
        # Transpose to this interval if every modulation lies within
        # the set of KEY classes that we can classify
        if set(transposed).issubset(set(transpositionKeys)):
            ret.append(interval)
    return ret


def initializeArrays(inputRepresentations, outputRepresentations):
    """Each array becomes a dict entry with the name of the input/output

    Parameters
    ----------
    inputRepresentations :
        
    outputRepresentations :
        

    Returns
    -------

    """
    outputArrays = {}
    for split in ["training", "validation"]:
        for x in inputRepresentations:
            outputArrays[split + f"_X_{x}"] = []
        for y in outputRepresentations:
            outputArrays[split + f"_y_{y}"] = []
    return outputArrays


def scrutinize(df, qualityThresh=0.75, bassThresh=0.8):
    """Filter 'bad quality' annotations.

    Parameters
    ----------
    df :
        
    qualityThresh :
         (Default value = 0.75)
    bassThresh :
         (Default value = 0.8)

    Returns
    -------

    """
    originalIndex = len(df.index)
    df = df[
        (df.qualitySquaredSum < qualityThresh)
        & (df.measureMisalignment == False)
        & (df.incongruentBass < bassThresh)
    ]
    filteredIndex = len(df.index)
    print(f"\t({originalIndex}, {filteredIndex})")


def correctSplit(split, testSetOn):
    """Correct the split of this file according to 'testSetOn' parameter.

    Parameters
    ----------
    split :
        
    testSetOn :
        

    Returns
    -------

    """
    if testSetOn:
        if split == "validation":
            return "training"
        elif split == "test":
            return "validation"
    return split


def generateDataset(
    synthetic,
    texturizeEachTransposition,
    noTransposition,
    collections,
    testCollections,
    inputRepresentations,
    outputRepresentations,
    sequenceLength,
    scrutinizeData,
    testSetOn,
    tsvDir,
    npzOutput,
    transpositionKeys,
):
    """

    Parameters
    ----------
    synthetic :
        
    texturizeEachTransposition :
        
    noTransposition :
        
    collections :
        
    testCollections :
        
    inputRepresentations :
        
    outputRepresentations :
        
    sequenceLength :
        
    scrutinizeData :
        
    testSetOn :
        
    tsvDir :
        
    npzOutput :
        
    transpositionKeys :
        

    Returns
    -------

    """
    outputArrays = {}
    training = ["training", "validation"] if testSetOn else ["training"]
    validation = ["test"] if testSetOn else ["validation"]
    datasetDir = f"{tsvDir}-synth" if synthetic else tsvDir
    summaryFile = os.path.join(datasetDir, DATASETSUMMARYFILE)
    if not os.path.exists(summaryFile):
        print("You need to generate the tsv files first.")
        exit()
    datasetSummary = pd.read_csv(summaryFile, sep="\t")
    trainingdf = datasetSummary[
        (datasetSummary.collection.isin(collections))
        & (datasetSummary.split.isin(training))
    ]
    validationdf = datasetSummary[
        (datasetSummary.collection.isin(testCollections))
        & (datasetSummary.split.isin(validation))
    ]
    df = pd.concat([trainingdf, validationdf])
    for row in df.itertuples():
        split = correctSplit(row.split, testSetOn)
        if split == "test":
            # Preemptive measure just to avoid a potential disaster
            continue
        print(f"{row.split} -used-as-> {split}", row.file)
        tsvlocation = os.path.join(datasetDir, row.split, f"{row.file}.tsv")
        df = joint_parser.from_tsv(tsvlocation)
        if scrutinizeData and split == "training":
            df = scrutinize(df)
        if noTransposition or split != "training":
            transpositions = ["P1"]
        else:
            transpositions = _getTranspositions(df, transpositionKeys)
            print("\t", transpositions)
        if synthetic:
            if not texturizeEachTransposition:
                # once per file
                df = joint_parser.retexturizeSynthetic(df)
            else:
                # once per transposition
                dfsynth = df.copy()
        for transposition in transpositions:
            if synthetic and texturizeEachTransposition:
                df = joint_parser.retexturizeSynthetic(dfsynth)
            for inputRepresentation in inputRepresentations:
                inputLayer = availableInputs[inputRepresentation](df)
                Xi = inputLayer.run(transposition=transposition)
                Xi = padToSequenceLength(Xi, sequenceLength, value=-1)
                npzfile = f"{split}_X_{inputRepresentation}"
                if npzfile not in outputArrays:
                    outputArrays[npzfile] = DynamicArray(
                        shape=Xi.shape, dtype="int8", memmap=f".{npzfile}.mmap"
                    )
                for sequence in Xi:
                    outputArrays[npzfile].update(sequence)
            for outputRepresentation in outputRepresentations:
                outputLayer = availableOutputs[outputRepresentation](df)
                yi = outputLayer.run(transposition=transposition)
                if outputRepresentation == "HarmonicRhythm7":
                    yi = padToSequenceLength(yi, sequenceLength, value=6)
                else:
                    yi = padToSequenceLength(yi, sequenceLength)
                npzfile = f"{split}_y_{outputRepresentation}"
                if npzfile not in outputArrays:
                    outputArrays[npzfile] = DynamicArray(
                        shape=yi.shape, dtype="int8", memmap=f".{npzfile}.mmap"
                    )
                for sequence in yi:
                    outputArrays[npzfile].update(sequence)
    # drop the extension, we'll overwrite it to .npz
    filename, _ = os.path.splitext(npzOutput)
    outputFile = f"{filename}-synth" if synthetic else filename
    outputArrays = {k: v.finalize() for k, v in outputArrays.items()}
    np.savez_compressed(outputFile, **outputArrays)


if __name__ == "__main__":
    parser = cli.npz()
    args = parser.parse_args()
    generateDataset(**vars(args))
