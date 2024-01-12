"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import numpy as np
import mido
from fractions import Fraction as frac
from mido import MidiFile, MidiTrack, Message, MetaMessage
from ..constants import SILENCE, CONTINUATION, PITCH, TRACK, OFFSET, VELOCITY, DURATION, TEMPO, PEDAL
from .constants import OCTAVES
import os


def voice_to_channel(instrument_list, voice, instruments):
    """

    Parameters
    ----------
    instrument_list :
        
    voice :
        
    instruments :
        

    Returns
    -------

    """
    instrument_of_voice = instruments.get(voice, 0)
    return instrument_list.index(instrument_of_voice)



def matrix_to_events(matrix, 
                     output_file=None, 
                     ticks_per_beat=384,
                     tempo=120, 
                     instruments={}, 
                     time_signature=(4, 4),
                     instrument_names=None):
    matrix = np.asarray(matrix)
    events = [] # [(time, instrument, duration, message)]
    for el in matrix:
        pitch, offset, duration, velocity, track, silence, continuation, tempo, pedal = el
        # Add note on, note off for each track

    return events



def set_tracks(mid, nb_tracks, instruments, instrument_names, channels, tempo, time_signature, output_file=None):
    for i in range(nb_tracks + 1):
        track = MidiTrack()
        if (len(instrument_names) > i) and instrument_names[i].startswith('drum'):
            channels[i] = 9
            track.append(Message('program_change', program=0, time=0, channel=9))
        elif i in instruments.keys():
            track.append(Message('program_change', program=instruments.get(i, 0), time=0, channel=channels[i]))
        elif i != 9:
            track.append(Message('program_change', program=0, time=0, channel=channels[i]))
        mid.tracks.append(track)

    if isinstance(output_file, str):
        mid.tracks[0].append(MetaMessage("track_name", name=os.path.split(output_file)[1], time=int(0)))
    else:
        mid.tracks[0].append(MetaMessage("track_name", name='track', time=int(0)))
    mid.tracks[0].append(MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo), time=int(0)))
    mid.tracks[0].append(MetaMessage("time_signature", numerator=time_signature[0], denominator=time_signature[1], time=int(0)))



def setup_instruments(matrix, instrument_names, instruments):
    instrument_names_new = []
    instrument_group = {}
    for track_nb, program in instruments.items():
        instrument_name = instrument_names[track_nb]
        if instrument_name.startswith('drums_'):
            instrument_group[-1] = instrument_group.get(-1, []) + [track_nb]
        else:
            instrument_group[program] = instrument_group.get(program, []) + [track_nb]

    # Change the tracks associated to each instrument
    instruments = {i: program for i, program in enumerate(instrument_group.keys())}
    invert_instruments = {program: i for i, program in instruments.items()}
    instruments = {key: val if val != -1 else 0 for key, val in instruments.items() }
    # Associate each track to the right new track
    for program, tracks in instrument_group.items():
        instrument_name = instrument_names[tracks[0]]
        if program == -1:
            instrument_name = 'drums_0'
        instrument_names_new.append(instrument_name)
        for i, track in enumerate(tracks):
            matrix[matrix[:, TRACK] == track, TRACK] = invert_instruments[program]

    instrument_names = instrument_names_new
    return instrument_names

def number_to_channel(n):
    """
    Given a number, return the corresponding channel (avoiding drum channel)
    Parameters
    ----------
    n :

    Returns
    -------

    """
    if n < 9:
        return n
    if n >= 9:
        return n + 1


def init_midi_file(matrix, instruments, ticks_per_beat=480, time_signature=(4, 4), anachrusis_time=0):
    mid = MidiFile()
    mid.ticks_per_beat = ticks_per_beat
    mid.type = 1

    bar_duration = time_signature[0] * 4 / time_signature[1]
    start_time = (-anachrusis_time) % bar_duration

    from fractions import Fraction as frac
    matrix[:, OFFSET] = matrix[:, OFFSET] + frac(start_time).limit_denominator(24)

    instrument_list = list(sorted(list(set([0] + list(instruments.values())))))
    nb_tracks = matrix[:, TRACK].max()
    channels = [number_to_channel(voice_to_channel(instrument_list, i, instruments)) for i in range(nb_tracks + 1)]

    return mid, nb_tracks, channels


def matrix_to_events(matrix):
    """
    Convert a matrix of notes, silences or continuations to a list of midi events (NOTE_ON, NOTE_OFF)
    It should :
    - Groupby each track
    - For each track sort by time
    - For each track, create a list of events (pitch, time, velocity, duration, track)
    - Use continuations to delay note_off event
    - Use silences to create note_off events
    - Use next note to create note_off events

    Parameters
    ----------
    matrix

    Returns
    -------
    events: np.ndarray
        List of events (pitch, time, velocity, duration, track)
    """






def matrix_to_mid(matrix, output_file=None, ticks_per_beat=480, tempo=120, instruments={}, time_signature=(4, 4),
                  anachrusis_time=0,
                  instrument_names=None, one_track_per_instrument=False, **kwargs):
    """
    Convert a matrix of notes, silences or continuations to a midi file


    Parameters
    ----------
    anachrusis_time: float
        Time in seconds of the anachrusis
    instrument_names: list of str
        List of instrument names
    one_track_per_instrument: bool
        If True, each instrument will be on a different track
    matrix :
        
    output_file :
         (Default value = None)
    ticks_per_beat :
         (Default value = 480)
    tempo :
         (Default value = 120)
    instruments :
         (Default value = {})
    **kwargs :

    Returns
    -------

    """
    if instrument_names is None:
        instrument_names = []


    matrix = np.asarray(matrix)

    if one_track_per_instrument:
        instrument_names = setup_instruments(matrix, instrument_names, instruments)

    mid, nb_tracks, channels = init_midi_file(matrix, instruments, ticks_per_beat=480,
                                              time_signature=(4, 4), anachrusis_time=0)
    set_tracks(mid, nb_tracks, instruments, instrument_names, channels, tempo, time_signature, output_file=None)

    sort_events = []
    last_silence = True

    for row in matrix:
        pitch = row[PITCH] + 60 + 12 * OCTAVES.get(instruments.get(row[TRACK], 0), 0)
        row = row.tolist()
        if row[SILENCE]:
            last_silence = True
            sort_events.append([0, 2, row[OFFSET], row[TEMPO], row[PEDAL], row[TRACK]])
            continue

        if row[CONTINUATION]:
            sort_events.append([0, 2, row[OFFSET], row[TEMPO], row[PEDAL], row[TRACK]])

        if row[CONTINUATION] == 0:
            sort_events.append([pitch,
                                1, row[OFFSET], row[VELOCITY], row[TRACK], row[TEMPO], row[PEDAL]])

        if not (row[CONTINUATION] and last_silence):
            sort_events.append([pitch, 0, (row[OFFSET] + row[DURATION]), row[TRACK], row[CONTINUATION],
                                row[TEMPO], row[PEDAL]
                                ])
            last_silence = False

    sort_events.sort(key=lambda tup: tup[2])
    current_tempo = tempo
    lapso = {idx: 0 for idx in range(nb_tracks + 1)}
    prev_pitch = {idx: 0 for idx in range(nb_tracks + 1)}
    for evt in sort_events:
        if evt[1] == 1:
            vel = int(evt[3])
            track_nb = int(evt[4])
            track = mid.tracks[track_nb]
            if evt[0] > 100 or evt[0] < 10:
                evt[0] = 0
                vel = 0

            real_time = int((evt[2] - lapso[track_nb]) * ticks_per_beat)

            track.append(Message('note_on', note=int(evt[0]), channel=channels[track_nb],
                                 velocity=vel, time=real_time))

            if evt[5] is not None and evt[5] != current_tempo:
                real_tempo =(480000 * 120) // evt[5]
                track.append(MetaMessage("set_tempo", tempo=real_tempo, time=int(0)))
                current_tempo = evt[5]

            if evt[6] is not None and evt[6]:
                track.append(Message('control_change', value=127, channel=channels[track_nb], control=4, time=int(0)))

            if evt[6] is not None and not evt[6]:
                track.append(Message('control_change', value=0, channel=channels[track_nb], control=4, time=int(0)))

            lapso[track_nb] = evt[2]
            prev_pitch[track_nb] = int(evt[0])
        elif evt[1] == 0:
            track_nb = int(evt[3])
            track = mid.tracks[track_nb]
            if evt[0] > 100 or evt[0] < 10:
                evt[0] = 0
            if evt[4] == 1 and prev_pitch[track_nb] > 0:
                track[-1] = Message('note_off', note=prev_pitch[track_nb], channel=channels[track_nb],
                                    velocity=0, time=int((evt[2] - lapso[track_nb]) * ticks_per_beat + track[-1].time))
            else:
                track.append(Message('note_off', note=int(evt[0]), channel=channels[track_nb],
                                     velocity=0, time=int((evt[2] - lapso[track_nb]) * ticks_per_beat)))
            lapso[track_nb] = evt[2]

        elif evt[1] == 2:
            track_nb = int(evt[5])
            track = mid.tracks[track_nb]
            tempo_change = evt[3]
            pedal_change = evt[4]

            if tempo_change is not None and tempo_change != current_tempo:
                real_tempo = (480000 * 120) // tempo_change
                track.append(MetaMessage("set_tempo", tempo=real_tempo, time=int(0)))
                current_tempo = tempo_change

            if pedal_change is not None and pedal_change:
                track.append(Message('control_change', value=127, channel=channels[track_nb], control=4, time=int(0)))

            if pedal_change is not None and not pedal_change:
                track.append(Message('control_change', value=0, channel=channels[track_nb], control=4, time=int(0)))


    if output_file is not None:
        for track in mid.tracks:
            track.append(MetaMessage('end_of_track', time=(int(0))))
        if isinstance(output_file, str):
            mid.save(output_file)
        else:
            mid.save(file=output_file)

    return mid


