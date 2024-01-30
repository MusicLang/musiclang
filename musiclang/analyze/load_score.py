import pandas as pd
import numpy as np
from miditoolkit import MidiFile
import partitura.musicanalysis as analysis
from musiclang.write.out.constants import REVERSE_INSTRUMENT_DICT



def load_score(filename, merge_tracks=True):
    """
    Load a score from a midi file and assign voices to each note

    Parameters
    ----------
    filename
    merge_tracks

    Returns
    -------
    notes: list
        List of notes with onset_beat, offset_beat, velocity, pitch, track, channel, voice
    bars: list
        List of bars with onset_beat, offset_beat
    instruments: dict
        Dictionary of instruments with channel as key and instrument name as value
    config: dict
        Dictionary of config with ticks_per_beats, bar_durations, tempo, tempos, time_signatures

    """

    import time as time_measure
    def get_end_of_bar(bar_start, time_signatures, ticks_per_beat):
        # Find time signature
        _, num, den, duration = [ts for ts in time_signatures if bar_start >= ts[0]][-1]
        return int(bar_start + duration * ticks_per_beat)

    def get_channel(idx, is_drum):
        if is_drum:
            return 9
        elif idx < 9:
            return idx
        else:
            return idx + 1

    def estimate_voices_with_index(x):
        y = x.copy()[['onset_quarter', 'duration_quarter', 'pitch']]
        y['duration_quarter'] -= 1e-1
        result = pd.Series(analysis.estimate_voices(y.to_records(), monophonic_voices=True))
        result.index = x.index  # Set the index to match the input
        return result

    m = MidiFile(filename)
    ticks_per_beat = m.ticks_per_beat
    score = []

    if len(m.time_signature_changes) > 0:
        time_signatures = [(ts.time, ts.numerator, ts.denominator, 4 * ts.numerator / ts.denominator) for ts in
                           m.time_signature_changes]
        time_signatures = list(sorted(time_signatures, key=lambda x: x[0]))
    else:
        time_signatures = [(0, 4, 4, 4)]

    # Calculate bars
    time = 0
    bars = []
    while time < m.max_tick:
        start_time = time
        end_time = get_end_of_bar(time, time_signatures, ticks_per_beat)
        bars.append((start_time / ticks_per_beat, end_time / ticks_per_beat))
        time = end_time

    programs = [(inst.program, inst.is_drum, get_channel(idx, inst.is_drum)) for idx, inst in enumerate(m.instruments)]
    instruments = {channel: REVERSE_INSTRUMENT_DICT[program] if not is_drum
    else f"drums_{program}" for program, is_drum, channel in programs}

    ## Step 1 : Get notes
    for idx, instrument in enumerate(m.instruments):
        id_instrument = f'0{idx}'[-2:]
        for idx_note, note in enumerate(instrument.notes):
            score.append({
                'onset_beat': note.start / ticks_per_beat,
                'duration_beat': (note.end - note.start) / ticks_per_beat,
                'onset_quarter': note.start / ticks_per_beat,
                'duration_quarter': (note.end - note.start) / ticks_per_beat,
                'onset_div': note.start,
                'duration_div': (note.end - note.start),
                'pitch': note.pitch,
                'voice': 0,
                'id': f"P{id_instrument}_n{idx_note}",
                'divs_pq': ticks_per_beat,
                'velocity': note.velocity,
                'track': idx,
                'channel': get_channel(idx, instrument.is_drum)
            })


    df = pd.DataFrame(score)

    def quantize_channel(df):
        ## Step 2 : Quantize
        from music21 import stream, note
        s = stream.Stream()

        for idx, row in df.iterrows():
            n = note.Note()
            n.quarterLength = row['duration_quarter']
            s.repeatInsert(n, [row['onset_quarter']])

        s.quantize((4,3), processOffsets=True, processDurations=True, inPlace=True)
        onsets = [e.offset for e in s]
        durations = [e.quarterLength for e in s]

        df['onset_quarter'] = onsets
        df['duration_quarter'] = durations
        df['onset_beat'] = df['onset_quarter']
        df['duration_beat'] = df['duration_quarter']
        df['onset_div'] = df['onset_quarter'] * ticks_per_beat
        df['duration_div'] = df['duration_quarter'] * ticks_per_beat
        return df

    df = df.sort_values(by=['onset_beat', 'pitch', 'duration_beat'])
    df = df.groupby('channel').apply(quantize_channel).reset_index(level=0, drop=True)
    df['offset_beat'] = df['onset_beat'] + df['duration_beat']
    df = df.sort_values(by=['onset_beat', 'pitch', 'duration_beat'])

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

    df['track'] = df['track'] + 1
    df['voice'] = df['voice'] - 1

    tempos = [temp.tempo for temp in m.tempo_changes]

    config = {'ticks_per_beats': ticks_per_beat,
              'bar_durations': [bar[1] - bar[0] for bar in bars],
              'instruments': instruments,
              'tempo': tempos[0], 'tempos': tempos, 'time_signatures': time_signatures}

    return df, bars, instruments, config