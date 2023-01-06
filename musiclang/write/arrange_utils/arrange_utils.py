"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import numpy as np
import pandas as pd

from .skyline_algorithm import SkylineSolution


def reduce_one(sequence, high=True):
    """

    Parameters
    ----------
    sequence :
        
    high :
         (Default value = True)

    Returns
    -------

    """
    sequence = sequence.copy()
    SILENCE_ABS_VAL = 2000
    silence_value = -SILENCE_ABS_VAL if high else SILENCE_ABS_VAL
    # Use skyline algorithm to find height map
    notes = sequence[['start', 'end', 'pitch', 'note_type', 'note_val', 'note_octave', 'note_duration',
                      'note_amp', 'chord_degree', 'chord_extension', 'chord_octave', 'tonality_degree',
                      'tonality_mode', 'tonality_octave', 'chord_idx', 'instrument', 'note_idx']].fillna(
        silence_value)

    if not high:
        notes['pitch'] = - notes['pitch']
    notes['pitch'] += SILENCE_ABS_VAL

    # Add little randomness to store equals pitches
    random_noise = np.random.random(len(notes)) / 3
    notes['pitch'] += random_noise
    notes = notes.values.tolist()
    solution = pd.DataFrame(SkylineSolution().get_skyline(notes),
                            columns=['start', 'pitch', 'note_type', 'note_val', 'note_octave', 'note_duration',
                      'note_amp', 'chord_degree', 'chord_extension', 'chord_octave', 'tonality_degree',
                      'tonality_mode', 'tonality_octave', 'chord_idx', 'instrument', 'note_idx'])
    solution['end'] = solution['start'] + solution['start'].diff(1).shift(-1)
    solution['pitch'] -= SILENCE_ABS_VAL
    if not high:
        solution['pitch'] = - solution['pitch']
    solution.loc[solution['pitch'] == silence_value, 'pitch'] = np.nan
    solution = solution.iloc[:-1]
    return solution


def recalculate_pitch(row):
    """

    Parameters
    ----------
    row :
        

    Returns
    -------

    """
    from musiclang.write.chord import Chord
    from musiclang.write.tonality import Tonality
    from musiclang.write.note import Note
    tonality = Tonality(row['tonality_degree'], mode=row['tonality_mode'], octave=row['tonality_octave'])
    chord = Chord(row['chord_degree'], octave=row['chord_octave'], tonality=tonality)
    note = Note(row['note_type'], row['note_val'], row['note_octave'], row['note_duration'], amp=row['note_amp'])
    return chord.to_pitch(note)

def reduce(score, n_voices=4, start_low=False, instruments=None):
    """Arrange a score to sum it up of 4 voices

    Parameters
    ----------
    score :
        param n_voices:
    n_voices :
         (Default value = 4)
    start_low :
         (Default value = False)
    instruments :
         (Default value = None)

    Returns
    -------

    """

    from ..note import Silence
    sequence = score.to_sequence()

    # Use skyline algorithm to find enveloppes
    if instruments is None:
        instruments = [f'piano__{idx}' for idx in range(n_voices)]
    if not start_low:
        instruments = instruments[::-1]
    idxs = [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6][:n_voices]
    solutions = []
    for i, idx in enumerate(idxs):
        solution = reduce_one(sequence, high=(i % 2) == 1 * start_low)
        solution['instrument'] = instruments[idx]
        solutions.append(solution)
        # Replace all solution notes in sequence with silences
        replace_silence = set(solution['note_idx'].unique())
        indexer = sequence['note_idx'].isin(replace_silence)
        len_indexer = indexer.sum()
        sequence.loc[indexer, 'note_type'] = ['r' for i in range(len_indexer)]
        sequence.loc[indexer, 'pitch'] = np.nan

    solution = pd.concat(solutions, axis=0).sort_values('start')

    # For each voice reassign to most probable pitch average
    # Recalculate pitch
    solution['pitch'] = solution.apply(recalculate_pitch, axis=1)
    # Recalculate is_silence
    # For each chord remove voices with only silences
    # For each chord each voice calculate average pitch
    # Then starting with first chord reassign each voice with closenessness of average pitch

    # Remove silences

    # Parse solution to new sequence
    from ..score import Score
    solution['silence'] = solution['note_type'] == 'r'
    solution['continuation'] = solution['note_type'] == 'l'
    solution['note_duration'] = solution['end'] - solution['start']
    score_result = Score.from_sequence(solution)

    return score_result


