import partitura as pt
import pandas as pd
import warnings


def _get_bars_from_parts(note_info):
    """
    Get bars start and end beat for each bar of the song
    """
    bars = None
    max_time = -1
    for part in note_info.parts:

        starts = []
        ends = []
        for measure in part.measures:
            start, end = measure.start.t, measure.end.t
            starts.append(start)
            ends.append(end)

        beats_start = part.beat_map(starts)
        beats_end = part.beat_map(ends)

        if max(beats_end) > max_time:
            bars = [(s, e) for s, e in zip(beats_start, beats_end)]

        return bars

def load_score(midi_file):
    note_info = pt.load_score_midi(midi_file,
                                   part_voice_assign_mode=5,
                                   quantization_unit=None,
                                   estimate_voice_info=True,
                                   estimate_key=False,
                                   assign_note_ids=True,
                                   )


    bars = _get_bars_from_parts(note_info)
    note_info_2 = pt.load_performance_midi(midi_file)
    columns = ['pitch', 'onset_beat', 'duration_beat', 'voice']
    columns_2 = ['velocity', 'track', 'channel']
    array = note_info.note_array()
    array_2 = note_info_2.note_array()
    assert len(array) == len(array_2) and all(array['pitch'] == array_2['pitch']), "Partitura does not output the same arrays when load_score_midi and load_performance_midi"
    df = pd.DataFrame(array[columns], columns=columns)
    df2 = pd.DataFrame(array_2, columns=columns_2)
    df['offset_beat'] = df['onset_beat'] + df['duration_beat']
    df['velocity'] = df2['velocity']
    df['track'] = df2['track']
    df['channel'] = df2['channel']
    notes = df[['onset_beat', 'offset_beat', 'velocity', 'pitch', 'track', 'channel', 'voice']].values.tolist()

    return notes, bars