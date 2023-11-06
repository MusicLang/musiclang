import partitura as pt
import pandas as pd
import warnings
from fractions import Fraction as frac

def _get_bars_from_parts(note_info):
    """
    Get bars start and end beat for each bar of the song
    """
    bars = None
    max_time = -1

    # First get longest part
    longest_part = max(note_info.parts, key=lambda x: len(x.measures))

    barss = []
    for part in note_info.parts:
        starts = []
        ends = []
        for measure in part.measures:
            start, end = measure.start.t, measure.end.t
            starts.append(start)
            ends.append(end)

        beats_start = part.beat_map(starts)
        beats_end = part.beat_map(ends)
        barss.append([(s, e) for s, e in zip(beats_start, beats_end)])

    # Concatenate all bars in barss
    bars = list(sorted(list(set([item for sublist in barss for item in sublist])), key=lambda x: x[0]))
    return bars

import numpy as np
def load_score(midi_file, merge_tracks=True, ticks_per_beat=480):
    import partitura.musicanalysis as analysis
    note_info = pt.load_score_midi(midi_file,
                                   part_voice_assign_mode=5,
                                   quantization_unit=None,
                                   estimate_voice_info=False,
                                   estimate_key=False,
                                   assign_note_ids=True,
                                   )


    bars = _get_bars_from_parts(note_info)
    note_info_2 = pt.load_performance_midi(midi_file)
    array = note_info.note_array()
    dtypes = array.dtype
    columns = list(dtypes.names)
    array_2 = note_info_2.note_array()
    dtypes2 = array_2.dtype
    columns_2 = list(dtypes2.names)



    # Sort by
    assert len(array) == len(array_2), "Partitura does not output the same arrays when load_score_midi and load_performance_midi"

    try:
        assert all(array['pitch'] == array_2['pitch']), "Partitura does not output the same pitches when load_score_midi and load_performance_midi"
    except:
        array = np.sort(array, order=['pitch', 'onset_beat', 'duration_beat'])
        array_2 = np.sort(array_2, order=['pitch', 'onset_sec', 'duration_sec'])
        assert all(array['pitch'] == array_2['pitch']), "After sorting, Partitura does not output the same pitches when load_score_midi and load_performance_midi"

    df = pd.DataFrame(array[columns], columns=columns)
    df2 = pd.DataFrame(array_2, columns=columns_2)
    df['offset_beat'] = df['onset_beat'] + df['duration_beat']
    df['velocity'] = df2['velocity']
    df['track'] = df2['track']
    df['channel'] = df2['channel']
    df = df.sort_values(by=['onset_beat', 'pitch', 'duration_beat'])
    def estimate_voices_with_index(x):
        result = pd.Series(analysis.estimate_voices(x.to_records()))
        result.index = x.index  # Set the index to match the input
        return result
    if merge_tracks:
        df['old_track'] = df['track']
        df['track'] = 0
        gpb = df.groupby('channel').apply(estimate_voices_with_index).reset_index(level=0, drop=True)
        try:
            df['voice'] = gpb
        except:
            df['voice'] = np.squeeze(gpb.values.T)
        df['track'] = df['old_track']
    else:
        df['voice'] = estimate_voices_with_index(df)

    # Quantize onset beats and offset beats
    #df['onset_beat'] = df['onset_beat'].apply(lambda x: float(frac(x).limit_denominator(8)))
    #df['offset_beat'] = df['offset_beat'].apply(lambda x: float(frac(x).limit_denominator(8)))

    notes = df[['onset_beat', 'offset_beat', 'velocity', 'pitch', 'track', 'channel', 'voice']].values.tolist()
    return notes, bars