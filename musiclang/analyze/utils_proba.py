import numpy as np
import itertools

from .constants import PROFILES
from .utils import softmax


_CHORD_INDEX = list(itertools.product(range(7), range(12), ['M', 'm', 'mm']))
_SCALE_INDEX = list(itertools.product(range(12), ['M', 'm']))

def get_chord_index():
    return _CHORD_INDEX

def get_scale_index():
    return _SCALE_INDEX


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
    """

    :param distribution:
    :param index:
    :param temperature:
    :return:
    """
    corr = [np.roll(PROFILES[mode], i) for i, mode in index]
    corrs_coeff = np.asarray([np.corrcoef(c, distribution)[1, 0] for c in corr])
    # Normalize with softmax
    density = np.log(softmax(corrs_coeff, temperature=temperature))
    return density, index


def loglikelihood_tonality_with_distribution(distribution, index, temperature=1):
    corr = [np.roll(PROFILES[mode], i) for i, mode in index]
    corrs_coeff = np.asarray([np.corrcoef(c, distribution)[1, 0] for c in corr])
    # Normalize with softmax
    density = np.log(softmax(corrs_coeff, temperature=temperature))
    return density, index


def get_scale_prior_matrix():
    index = get_scale_index()
    return np.log(np.ones(len(index)) / len(index))

def get_scale_transition_matrix(temperature=1):
    index = get_scale_index()
    # CORRELATE ALL PROFILES
    corr = [np.roll(PROFILES[mode], i) for i, mode in index]
    corrs_coeff = np.asarray([[np.corrcoef(ci, cj)[1, 0] for ci in corr] for cj in corr])
    # Normalize with softmax
    density = np.log(np.asarray([softmax(c, temperature=temperature) for c in corrs_coeff]))
    return density


def get_scale_emission_matrix(distributions):
    """
    Matrix of proba densities of each tonalities
    Row : Tonalities
    Column : For specific bar
    :param distributions:
    :return:
    """
    row_index = get_scale_index()
    likelihoods = [loglikelihood_tonality_with_distribution(dist, row_index)[0] for dist in distributions]
    likelihoods = np.asarray(likelihoods)
    return likelihoods



