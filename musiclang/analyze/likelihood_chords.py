
from .constants import PROFILES
import numpy as np
import pandas as pd
import itertools
from .utils import softmax

from musiclang.core.chord import Chord



_CHORD_INDEX = list(itertools.product(range(7), range(12), ['M', 'm', 'mm']))

def get_chord_index():
    return _CHORD_INDEX


def get_pitch_scale_vector(index, bonus=0.4):
    prior = [1, 0.4, 0.1, 0.5, 0.8, 0.4, 0.1]
    pass


def get_chord_emission_matrix(distributions, scales):
    """
    Get the probability of one chord to another given distribution, and current scale
    :param distributions:
    :param scales:
    :return:
    """
    row_index = get_chord_index()
    likelihoods = [loglikelihood_chords_vs_tonality(dist, row_index)[0] for dist in distributions]
    likelihoods = np.asarray(likelihoods)
    return likelihoods


def loglikelihood_chords_vs_tonality(distribution, index, temperature=1):
    corr = [np.roll(PROFILES[mode], i) for i, mode in index]
    corrs_coeff = np.asarray([np.corrcoef(c, distribution)[1, 0] for c in corr])
    # Normalize with softmax
    density = np.log(softmax(corrs_coeff, temperature=temperature))
    return density, index




