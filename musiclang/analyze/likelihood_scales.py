from .constants import PROFILES
import numpy as np
import pandas as pd
import itertools

from .utils import softmax

_ROW_INDEX = list(itertools.product(range(12), ['M', 'm', 'mm']))
def get_index():
    return _ROW_INDEX


def get_scale_prior_matrix():
    index = get_index()
    return np.log(np.ones(len(index)) / len(index))

def get_scale_transition_matrix(temperature=1):
    index = get_index()
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
    row_index = get_index()
    likelihoods = [loglikelihood_tonality_with_distribution(dist, row_index)[0] for dist in distributions]
    likelihoods = np.asarray(likelihoods)
    return likelihoods


def loglikelihood_tonality_with_distribution(distribution, index, temperature=1):
    corr = [np.roll(PROFILES[mode], i) for i, mode in index]
    corrs_coeff = np.asarray([np.corrcoef(c, distribution)[1, 0] for c in corr])
    # Normalize with softmax
    density = np.log(softmax(corrs_coeff, temperature=temperature))
    return density, index


