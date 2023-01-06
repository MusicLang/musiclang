from musiclang.write.library import *
from fractions import Fraction as frac
import numpy as np


def generate_chords_from_sequence(patterns):
    """

    Parameters
    ----------
    patterns :
        

    Returns
    -------

    """

    pass
    return [I] * len(patterns), [pattern.duration for pattern in patterns]

def generate_random_sequence(duration, seed=None):
    """

    Parameters
    ----------
    duration :
        
    seed :
         (Default value = None)

    Returns
    -------

    """
    if seed is None:
        seed = np.random.randint(0, 2 ** 31)
    rg = np.random.RandomState(seed)

    # Only binary beats
    countings = [frac(1, i) for i in [1, 2] if (duration % i) == 0] # X/8 or x/4
    counting = rg.choice(countings)
    tick = rg.choice([counting, counting/2])
    nb_patterns_candidate = [i for i in range(1, int(duration)) if duration/i == duration//i]
    nb_patterns = rg.choice(nb_patterns_candidate)
    repeat_patterns_list = [rg.randint(0, nb_patterns) for i in range(nb_patterns)]
    unique_patterns = {el: idx for idx, el in enumerate(list(dict.fromkeys(repeat_patterns_list)))}
    repeat_patterns = [unique_patterns[el] for el in repeat_patterns_list]
    duration_pattern = duration // nb_patterns
    # Generate n patterns
    patterns = [generate_random_rythm_pattern(duration_pattern, counting, tick, seed=seed) for i in range(nb_patterns)]
    patterns_list = [patterns[i] for i in repeat_patterns]
    result = sum(patterns_list, None)
    assert result.duration == duration
    return result, patterns_list


def generate_random_rythm_pattern(duration, counting, tick, seed=None):
    """

    Parameters
    ----------
    duration :
        
    counting :
        
    tick :
        
    seed :
         (Default value = None)

    Returns
    -------

    """
    if seed is None:
        seed = np.random.randint(0, 2 ** 31)
    rg = np.random.RandomState(seed)
    # duration = 16, counting = 1/2, tick = 1/4
    CANDIDATE_FIRST_BEAT = [TONIC] * 4 + [TONIC_OR_FIFTH] * 3 + [CHORD_NOTE] * 1 + [SILENCE] * 1
    CANDIDATE_COUNTING_BEAT = [TONIC] * 1 + [TONIC_OR_FIFTH] * 1 + [CHORD_NOTE] * 3 + [SCALE_NOTE] * 1 + [SCALE_DISSONNANCE] * 1 + [SILENCE] * 1 + [CONTINUATION] * 1
    CANDIDATE_OTHER_BEAT = [CHORD_NOTE] * 1 + [SCALE_NOTE] * 1 + [SILENCE] * 2 + [CONTINUATION] * 3 + [SCALE_DISSONNANCE] * 4
    result = None
    assert int(duration / tick) == duration / tick
    for time in range(int(duration / tick)):
        if time == 0: # First beat
            result += rg.choice(CANDIDATE_FIRST_BEAT).augment(tick)
        elif (time % counting) == 0:  # Counting beat
            result += rg.choice(CANDIDATE_COUNTING_BEAT).augment(tick)
        else: # Other beat
            result += rg.choice(CANDIDATE_OTHER_BEAT).augment(tick)

    return result



