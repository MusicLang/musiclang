"""A Roman numeral analysis network with synthetic data and additional tasks."""

from os.path import dirname, basename, isfile, join
import glob

__author__ = "Néstor Nápoles López"
__version__ = "1.9.0"

from .inference import get_model, m21Parse, infer_chords

