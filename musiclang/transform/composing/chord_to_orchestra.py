import glob
import random
from musiclang import Score, Tonality
import numpy as np
from musiclang.library import *

def map_nearest_indices(A, B):
    def nearest_index(a, b):
        return min(range(len(a)), key=lambda i: abs(a[i] - b))

    return {i: nearest_index(A, b) for i, b in enumerate(B)}


def map_matrix(A, B, Mb):
    """
    Map a matrix Mb to a matrix Ma, such that Ma[i] is the row in Mb that is closest to B[i]
    Parameters
    ----------
    A: list
    B: list
    Mb: matrix

    Returns
    -------
    Ma: matrix

    """
    Mb = np.asarray(Mb)
    if not len(B) == Mb.shape[0]:
        raise ValueError("Length of B must be equal to the number of rows in Mb")

    mapping = map_nearest_indices(A, B)
    Ma = np.zeros((len(A), Mb.shape[1]), dtype=int)

    for i in range(len(A)):
        # Finding the indices in B that are mapped to the current index in A
        mapped_indices = [index for index, mapped_index in mapping.items() if mapped_index == i]

        # Averaging the rows in Mb that are mapped to the current row in Ma
        if mapped_indices:
            Ma[i] = np.sum(Mb[mapped_indices], axis=0)

    return Ma.tolist()


def chord_to_orchestra(chord, drop_drums=True, nb=4, pattern=False):
    """
    Convert a chord to an orchestra
    Parameters
    ----------
    chord: Chord
        The musiclang chord to convert into an orchestra
    drop_drums : bool, optional, default=True
        Drop drums instruments
    nb: int, optional, default=4
        nb arpeggio notes to consider on each side, it will give the acceptable range of the instrument melody


    Returns
    -------
    l:list
    Orchestra object, one entry per instrument

    """
    orchestra_raw = chord.get_orchestration()
    orchestra = []

    # chord_tonality =
    for instrument in orchestra_raw:
        if drop_drums and instrument['instrument'].startswith('drums_0'):
            continue
        else:
            note = instrument['note']
            base_note = chord.__getattribute__(note)
            base_pitch = chord.to_pitch(base_note)
            pitch_grid = (
                    [chord.to_pitch(Score.from_str(f'bd{nb - i}'), last_pitch=base_pitch) for i in range(nb)]
                    + [base_pitch]
                    + [chord.to_pitch(Score.from_str(f'bu{i + 1}'), last_pitch=base_pitch) for i in range(nb)]
            )
            notes_grid = (
                    [f'bd{nb - i}' for i in range(nb)]
                    + ['x0']
                    + [f'bu{i + 1}' for i in range(nb)]
            )

            melody_score = instrument['pattern'].apply_pattern(base_note)
            grid = chord(melody_score).to_score().to_melody_grid('piano__0', octave=0)
            pitch_range = grid['notes']

            # Convert absolute notes to arpeggio
            grid['rhythm'] = map_matrix(pitch_grid, pitch_range, grid['rhythm'])
            instrument['rhythm'] = grid
            instrument['rhythm']['notes'] = notes_grid
            instrument['rhythm']['octave'] = instrument['octave']
            if not pattern:
                del instrument['pattern']
            orchestra.append(instrument)

    return orchestra