"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import pandas as pd
import numpy as np
from mido import MidiFile


TYPE = "type"
TIME = "time"
NOTE = "note"
VEL = "vel"
CHANNEL = "channel"
DURATION = "duration"
END_TIME = "end_time"
START_TIME = "start_time"
TRACK = "track"
VOICE = "voice"
ON = 1
OFF = 0


def parse_midi(filename, **kwargs):
    """Parse a midi files and returns array of notes, instruments and the tempo

    Parameters
    ----------
    filename :
        param kwargs:
    **kwargs :
        

    Returns
    -------

    """
    notes, config = _load_midi(filename, **kwargs)
    instruments = config['instruments']
    tempo = config['tempo']
    return notes, instruments, tempo


"""
Below, some loader helpers :
"""

class MusicLangIgnoreException(Exception):
    """ """
    pass


def _load_midi(filename, ignore_file_with_bar_change=False, **kwargs):
    """Create a note array from a midi file

    Parameters
    ----------
    filename :
        return:
    ignore_file_with_bar_change :
         (Default value = False)
    **kwargs :
        

    Returns
    -------

    """
    notes, config = _parse(filename)
    if len(config['bar_durations']) > 1 and ignore_file_with_bar_change:
        raise MusicLangIgnoreException('Bar duration change events in midifile, MusicLang cannot parse that')
    elif len(config['bar_durations']) == 1:
        config['bar_duration'] = config['bar_durations'][0]
    else:
        config['bar_duration'] = None
    return notes, config


def _parse(filename, **kwargs):
    """

    Parameters
    ----------
    filename :
        
    **kwargs :
        

    Returns
    -------

    """
    from fractions import Fraction as frac

    mf = MidiFile(filename)
    instruments = _infer_instruments(mf)
    notes = []
    bar_durations = []
    tempos = []

    for track_idx, track in enumerate(mf.tracks):
        time = 0
        for note in track:
            if note.type == 'note_on':
                notes.append([1, time + note.time, note.note, note.velocity, note.channel, track_idx])
            elif note.type == 'note_off':
                notes.append([0, time + note.time, note.note, note.velocity, note.channel, track_idx])
            elif note.type == 'time_signature':
                bar_durations.append(note.numerator * frac(4, note.denominator))
            elif note.type == 'set_tempo':
                tempos.append((time, note.tempo))
            time = time + note.time
    notes = np.asarray(notes)
    first_tempo = int(60/(tempos[0][1]/1e6))
    config = {'ticks_per_beats': mf.ticks_per_beat,
             'instruments': instruments,
             'tempo': first_tempo, 'tempos': tempos, 'bar_durations': bar_durations}

    notes = _get_notes_dataframe(notes)
    notes = _get_notes_in_beats(notes, mf.ticks_per_beat)
    notes = np.asarray(notes[[START_TIME, NOTE, DURATION, VEL, TRACK, CHANNEL, VOICE]])
    return notes, config


def _get_notes_in_beats(df, ticks_per_beats):
    """By default notes are stored in ticks from midi file, convert it to beats
    :return:

    Parameters
    ----------
    df :
        
    ticks_per_beats :
        

    Returns
    -------

    """
    df = df.copy()
    df[START_TIME] /= ticks_per_beats
    df[END_TIME] /= ticks_per_beats
    df[DURATION] /= ticks_per_beats
    return df

def _get_notes_dataframe(notes):
    """Convert note_on, note_off events to a note dataframe
    :return:

    Parameters
    ----------
    notes :
        

    Returns
    -------

    """
    from itertools import product
    events = pd.DataFrame(notes, columns=[TYPE, TIME, NOTE, VEL, CHANNEL, TRACK])
    times = {(track, note): 0 for track, note in product(events[TRACK].unique(), range(120))}
    vels = {(track, note): 0 for track, note in product(events[TRACK].unique(), range(120))}
    ons = {(track, note): False for track, note in product(events[TRACK].unique(), range(120))}
    notes = []
    for idx, row in events.iterrows():
        if (row[TYPE] == ON) and row[VEL] > 0 and not ons[row[TRACK], row[NOTE]]:
            times[row[TRACK], row[NOTE]] = row[TIME]
            vels[row[TRACK], row[NOTE]] = row[VEL]
            ons[row[TRACK], row[NOTE]] = True
        else: # Note OFF
            start_time = times[row[TRACK], row[NOTE]]
            ons[row[TRACK], row[NOTE]] = False
            vel = vels[row[TRACK], row[NOTE]]
            end_time = row[TIME]
            duration = end_time - start_time
            notes.append([start_time, end_time, duration, row[NOTE], vel, row[CHANNEL], row[TRACK], 0])

    notes = pd.DataFrame(notes, columns=[START_TIME, END_TIME, DURATION, NOTE, VEL, CHANNEL, TRACK, VOICE]).sort_values(START_TIME)
    return notes


def _infer_instruments(mf):
    """

    Parameters
    ----------
    mf :
        

    Returns
    -------

    """
    from musiclang.write.out.constants import REVERSE_INSTRUMENT_DICT
    channel_inst = {}
    for track in mf.tracks:
        for note in track:
            if note.type == 'program_change':
                channel_inst[note.channel] = REVERSE_INSTRUMENT_DICT[note.program]
    return channel_inst




