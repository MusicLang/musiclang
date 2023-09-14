from musiclang import Score, Melody
import numpy as np
from fractions import Fraction as frac
from musiclang.library import *


def grid_to_melody(grid, tatum, notes, mode='legato'):
    """
    A grid in an array of array (dimensions : notes, time)
    Parameters
    ----------
    grid

    Returns
    -------

    """

    notes = [Score.from_str(n) for n in notes]
    step = frac(*tatum)
    grid = np.asarray(grid)

    melody = []
    for j, col in enumerate(grid.T):
        for i, row in enumerate(col):
            if row:
                note = notes[i]
                note.duration = step
                melody.append(x0.n)
                melody.append(note)
                break
        else:

            if mode == 'staccato' or j == 0:
                melody.append(r.set_duration(step))
            elif mode == 'legato':
                melody.append(l.set_duration(step))

    return Melody(melody)
