"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import numpy as np
from musiclang.write.library import *
from .random_rythm import generate_random_sequence
from musiclang.composing.arrange import get_absolute_voice



def generate_random_melody(duration, seed=None):
    """

    Parameters
    ----------
    duration :
        
    seed :
         (Default value = None)

    Returns
    -------

    """
    rythm, patterns = generate_random_sequence(duration, seed=seed)
    melody = generate_random_melody_on_rythm(rythm, seed=seed)
    # Convert to absolute melody
    melody = get_absolute_voice(melody)
    return melody, patterns


def generate_random_melody_on_patterns(patterns, **kwargs):
    """

    Parameters
    ----------
    patterns :
        
    **kwargs :
        

    Returns
    -------

    """
    result = generate_random_melody_on_rythm(sum(patterns, None), **kwargs)
    assert result.duration == sum(patterns, None).duration
    return result, patterns

def generate_random_melody_on_rythm(rythm, octaves=2, seed=None, **kwargs):
    """

    Parameters
    ----------
    rythm :
        
    octaves :
         (Default value = 2)
    seed :
         (Default value = None)
    **kwargs :
        

    Returns
    -------

    """
    if seed is None:
        seed = np.random.randint(0, 2 ** 31)
    rg = np.random.RandomState(seed)
    candidates_first = [s6.o(-1), s5.o(-1), s4.o(-1), s0, s1, s2, s3, s4, s5, s6, s0.o(1)]
    candidates = [su0, su1, sd1, su2, sd2, su3, sd3]
    acc = 0
    result_melody = None
    had_first = False
    for idx, rythm_note in enumerate(rythm.notes):
        if rythm_note.is_note:
            if not had_first:
                candidate = rg.choice(candidates_first)
                acc = candidate.scale_pitch
            else:
                possible_candidates = get_possible_candidates(candidates, octaves, acc)
                candidate = rg.choice(possible_candidates)
                acc += candidate.delta_value
            had_first = True
            result_melody += candidate.augment(rythm_note.duration)
        else:
            result_melody += rythm_note.copy()

    return result_melody


def get_possible_candidates(candidates, octaves, acc):
    """

    Parameters
    ----------
    candidates :
        
    octaves :
        
    acc :
        

    Returns
    -------

    """
    possible_values = [c for c in candidates if abs(c.delta_value + acc) <= 7 * (octaves//2)]
    return possible_values