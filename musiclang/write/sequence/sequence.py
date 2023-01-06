"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

# Groupby
from fractions import Fraction as frac


def sequence_to_score(sequence, sort_by_time=True, **kwargs):
    """Convert a dataframe (called a sequence) to a MusicLang score

    Parameters
    ----------
    sequence :
        pandas.DataFrame with required columns
    sort_by_time :
        boolean, default=True, If true sort by 'start' column before reconverting to score
    **kwargs :
        

    Returns
    -------
    type
        score, Score : converted score

    """
    from ..chord import Chord
    from ..tonality import Tonality
    from ..note import Note, Silence, Continuation
    if sort_by_time:
        sequence = sequence.sort_values(by='start', ascending=True)
    groups_chord = sequence.groupby('chord_idx')
    score = None
    for chord_idx, group_chord in groups_chord:
        chord_row = group_chord.iloc[0]
        tonality = Tonality(int(chord_row['tonality_degree']), mode=chord_row['tonality_mode'],
                            octave=int(chord_row['tonality_octave']))
        chord = Chord(int(chord_row['chord_degree']), extension=chord_row['chord_extension'], tonality=tonality)
        parts = {}
        groups_instrument = group_chord.groupby('instrument')
        for instrument, row in groups_instrument:
            part = None
            for idx_note, note in row.iterrows():
                if note['silence']:
                    new_note = Silence(note['note_duration'])
                elif note['continuation']:
                    new_note = Continuation(note['note_duration'])
                else:
                    new_note = Note(note['note_type'],
                                val=int(note['note_val']),
                                octave=int(note['note_octave']),
                                duration=frac(note['note_duration']).limit_denominator(8),
                                amp=int(note['note_amp']))
                part += new_note
            parts[instrument] = part
        score += chord(**parts)
    return score


def score_to_sequence(score, **kwargs):
    """Convert a score to a sequence (pandas.DataFrame with specific columns)

    Parameters
    ----------
    score :
        musiclang.Score
    **kwargs :
        

    Returns
    -------
    type
        sequence, pandas.DataFrame : converted sequence

    """

    sequence = []
    time = 0
    for idx, chord in enumerate(score):
        sequence += [[time, idx] + s for s in chord.to_sequence()]
        time += chord.duration

    import pandas as pd
    import numpy as np

    sequence = pd.DataFrame(sequence,
                            columns=['chord_time', 'chord_idx', 'chord_relative_start', 'chord_relative_end', 'pitch',
                                     'chord', 'instrument', 'note'])
    sequence['start'] = sequence['chord_time'] + sequence['chord_relative_start']
    sequence['end'] = sequence['chord_time'] + sequence['chord_relative_end']
    sequence['chord_degree'] = sequence['chord'].apply(lambda x: x.element)
    sequence['chord_extension'] = sequence['chord'].apply(lambda x: x.extension)
    sequence['chord_octave'] = sequence['chord'].apply(lambda x: x.octave)
    sequence['tonality_degree'] = sequence['chord'].apply(lambda x: x.tonality.degree)
    sequence['tonality_mode'] = sequence['chord'].apply(lambda x: x.tonality.mode)
    sequence['tonality_octave'] = sequence['chord'].apply(lambda x: x.tonality.octave)

    sequence['silence'] = sequence['note'].apply(lambda x: x.is_silence)
    sequence['continuation'] = sequence['note'].apply(lambda x: x.is_continuation)
    sequence['note_type'] = sequence['note'].apply(lambda x: x.type)
    sequence['note_val'] = sequence['note'].apply(lambda x: x.val)
    sequence['note_octave'] = sequence['note'].apply(lambda x: x.octave)
    sequence['note_amp'] = sequence['note'].apply(lambda x: x.amp)
    sequence['note_duration'] = sequence['note'].apply(lambda x: x.duration)
    sequence['note_idx'] = np.arange(len(sequence))
    COLUMNS = ['chord_time', 'chord_idx', 'chord_relative_start', 'chord_relative_end', 'pitch', 'instrument',
                'start', 'end', 'chord_degree', 'chord_extension', 'chord_octave', 'tonality_degree',
               'tonality_mode', 'tonality_octave', 'silence', 'continuation',
               'note_type', 'note_val', 'note_octave', 'note_amp',
               'note_duration', 'note_idx'
               ]
    return sequence[COLUMNS].sort_values(by='start', ascending=True)