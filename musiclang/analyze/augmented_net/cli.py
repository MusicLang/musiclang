"""The argparse interfaces for the runnable scripts in AugmentedNet."""

from argparse import ArgumentParser

from . import models
from .data import available_collections as availableCollections
from .dataset_npz_generator import __doc__ as npz_description
from .dataset_tsv_generator import __doc__ as tsv_description
from .train import __doc__ as train_description
from .inference import __doc__ as inference_description
from .feature_representation import TRANSPOSITIONKEYS
from .input_representations import (
    available_representations as availableInputs,
)
from .output_representations import (
    available_representations as availableOutputs,
)


class DefaultArguments(object):
    """ """
    base = {
        "tsvDir": "dataset",
    }
    tsv = {
        "synthesize": False,
        "texturize": False,
    }
    npz = {
        "synthetic": False,
        "texturizeEachTransposition": False,
        "noTransposition": False,
        "collections": ["bps"],
        "testCollections": ["bps"],
        "inputRepresentations": [
            "Bass19",
            "Chromagram19",
            "MeasureNoteOnset14",
        ],
        "outputRepresentations": [
            "Alto35",
            "Bass35",
            # "ChordQuality11",
            # "ChordRoot35",
            "HarmonicRhythm7",
            # "Inversion4",
            "LocalKey38",
            "PitchClassSet121",
            # "PrimaryDegree22",
            "RomanNumeral31",
            # "SecondaryDegree22",
            "Soprano35",
            "Tenor35",
            "TonicizedKey38",
        ],
        "sequenceLength": 640,
        "scrutinizeData": False,
        "testSetOn": False,
        "npzOutput": "dataset",
        "transpositionKeys": TRANSPOSITIONKEYS,
    }
    train = {
        "nogpu": False,
        "useExistingNpz": False,
        "syntheticDataStrategy": None,
        "model": "AugmentedNet",
        "lr_boundaries": [40],
        "lr_values": [0.001, 0.001],
        "epochs": 100,
        "batchsize": 16,
        "transferLearningFrom": "",
        "transferLearningFreeze": False,
    }
    inference = {
        "modelPath": "AugmentedNet.hdf5",
        "dir": False,
        "useGpu": False,
    }


def _base(is_parent_parser=True):
    """

    Parameters
    ----------
    is_parent_parser :
         (Default value = True)

    Returns
    -------

    """
    if is_parent_parser:
        parser = ArgumentParser(add_help=False)
    else:
        parser = ArgumentParser()
    parser.add_argument(
        "--tsvDir",
        type=str,
        help="A path to the directory where the tsvs will be located.",
    )
    parser.set_defaults(**DefaultArguments.base)
    return parser


def tsv():
    """ """
    parents = [_base()]
    parser = ArgumentParser(description=tsv_description, parents=parents)
    parser.add_argument(
        "--synthesize",
        action="store_true",
        help="Instead of a real score, synthesize one from the RNA.",
    )
    parser.add_argument(
        "--texturize",
        action="store_true",
        help="If synthesizing a score, apply texturization to it.",
    )
    parser.set_defaults(**DefaultArguments.tsv)
    return parser


def npz(is_parent_parser=False):
    """

    Parameters
    ----------
    is_parent_parser :
         (Default value = False)

    Returns
    -------

    """
    parents = [_base()]
    if is_parent_parser:
        parser = ArgumentParser(add_help=False, parents=parents)
    else:
        parser = ArgumentParser(description=npz_description, parents=parents)
    parser.add_argument(
        "--collections",
        choices=list(availableCollections.keys()),
        nargs="+",
        help="Include training files from a specific corpus/collection.",
    )
    parser.add_argument(
        "--noTransposition",
        action="store_true",
        help="Disable transposition data augmentation on the training set.",
    )
    parser.add_argument(
        "--inputRepresentations",
        choices=list(availableInputs.keys()),
        nargs="+",
        help="The input representations to be used.",
    )
    parser.add_argument(
        "--npzOutput", type=str, help="The path of the output .npz file(s)."
    )
    parser.add_argument(
        "--outputRepresentations",
        choices=list(availableOutputs.keys()),
        nargs="+",
        help="The output representations to be used.",
    )
    parser.add_argument(
        "--scrutinizeData",
        action="store_true",
        help="Exclude bad-quality annotations from the training data.",
    )
    parser.add_argument(
        "--sequenceLength",
        choices=range(64, 640),
        type=int,
        help="The number of frames in each input sequence.",
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Search for a synthetic dataset, not one from real scores.",
    )
    parser.add_argument(
        "--texturizeEachTransposition",
        action="store_true",
        help="Texturize each time you transpose a synthesized file.",
    )
    parser.add_argument(
        "--testCollections",
        choices=list(availableCollections.keys()),
        nargs="+",
        help="Include test files from a specific corpus/collection.",
    )
    parser.add_argument(
        "--testSetOn",
        action="store_true",
        help="Use the real test set, and add the validation set to training.",
    )
    parser.add_argument(
        "--transpositionKeys",
        choices=TRANSPOSITIONKEYS,
        nargs="+",
        help="Constraint the keys for transposition (data augmentation).",
    )
    parser.set_defaults(**DefaultArguments.npz)
    return parser


def train():
    """ """
    parents = [npz(is_parent_parser=True)]
    parser = ArgumentParser(description=train_description, parents=parents)
    parser.add_argument(
        "experiment_name",
        choices=[
            "local",
            "computecanada",
            "colab",
            "ablation",
            "validationset",
            "testset",
            "debug",
        ],
        help="A short name for this experiment.",
    )
    parser.add_argument(
        "run_name", type=str, help="A name for this experiment run."
    )
    parser.add_argument(
        "--batchsize",
        type=int,
        help="Number of training examples per batch",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--useExistingNpz",
        action="store_true",
        help="Do not generate the numpy dataset, use an existing one.",
    )
    parser.add_argument(
        "--lr_boundaries",
        nargs="+",
        type=int,
        help="The piecewise learning rate boundary points (in epochs).",
    )
    parser.add_argument(
        "--lr_values",
        nargs="+",
        type=float,
        help="The piecewise learning rate values for different boundaries.",
    )
    parser.add_argument(
        "--model",
        choices=list(models.available_models.keys()),
        help="The neural network architecture to use.",
    )
    parser.add_argument(
        "--nogpu",
        action="store_true",
        help="Disable the use of any GPU.",
    )
    parser.add_argument(
        "--syntheticDataStrategy",
        choices=["syntheticOnly", "concatenate"],
        help="The strategy to use for synthetic training examples (if any).",
    )
    parser.add_argument(
        "--transferLearningFrom",
        type=str,
        help="Start from a pretrained model to do transfer learning.",
    )
    parser.add_argument(
        "--transferLearningFreeze",
        action="store_true",
        help="If transfer learning, freeze all but the classification layers.",
    )
    parser.set_defaults(**DefaultArguments.train)
    return parser


def inference():
    """ """
    parser = ArgumentParser(description=inference_description, parents=[])
    parser.add_argument(
        "inputPath",
        help="The path to a MusicXML (or similar) input score to process.",
    )
    parser.add_argument(
        "--modelPath", help="The path to a trained HDF5 AugmentedNet model."
    )
    parser.add_argument(
        "--dir",
        action="store_true",
        help="Specify a directory input. Run inference on all files within.",
    )
    parser.add_argument(
        "--useGpu",
        action="store_true",
        help="Use GPU if available.",
    )
    parser.set_defaults(**DefaultArguments.inference)
    return parser
