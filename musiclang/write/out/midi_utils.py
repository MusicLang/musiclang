"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import numpy as np

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


def matrix_to_mid(matrix, output_file=None, ticks_per_beat=480, tempo=120, instruments={}, **kwargs):
    """

    Parameters
    ----------
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
    from mido import MidiFile, MidiTrack, Message, MetaMessage
    from ..constants import SILENCE, CONTINUATION, PITCH, TRACK, OFFSET, VELOCITY, DURATION
    from .constants import OCTAVES
    import os

    matrix = np.asarray(matrix)

    def number_to_channel(n):
        """

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

    mid = MidiFile()
    mid.ticks_per_beat = ticks_per_beat
    mid.type = 1

    # Take care of continuation
    # matrix = matrix[(matrix['pitch'] > 0) | (matrix['continuation'] > 0)]
    # Remove all continuations that follows a silence
    # Put all instruments with same name in same track
    # For each voice assign right track
    instrument_list = list(sorted(list(set([0] + list(instruments.values())))))
    # Replace with track in matrix
    # For each voice assign right track

    # Replace with track in matrix
    nb_tracks = matrix[:, TRACK].max()
    channels = [number_to_channel(voice_to_channel(instrument_list, i, instruments)) for i in range(nb_tracks + 1)]

    for i in range(nb_tracks + 1):
        track = MidiTrack()
        if i in instruments.keys():
            track.append(Message('program_change', program=instruments.get(i, 0), time=0, channel=channels[i]))
        elif i != 9:
            track.append(Message('program_change', program=0, time=0, channel=channels[i]))
        mid.tracks.append(track)

    if output_file is not None:
        mid.tracks[0].append(MetaMessage("track_name", name=os.path.split(output_file)[1], time=int(0)))
        mid.tracks[0].append(MetaMessage("set_tempo", tempo=(480000 * 120) // tempo, time=int(0)))
        mid.tracks[0].append(MetaMessage("time_signature", numerator=4, denominator=4, time=int(0)))

    sort_events = []
    last_silence = True
    for row in matrix:
        pitch = row[PITCH] + 60 + 12 * OCTAVES.get(instruments.get(row[TRACK], 0), 0)
        row = row.tolist()
        if row[SILENCE]:
            last_silence = True
            continue
        if row[CONTINUATION] == 0:
            sort_events.append([pitch,
                                1, row[OFFSET], row[VELOCITY], row[TRACK]])

        if not (row[CONTINUATION] and last_silence):
            sort_events.append([pitch, 0, (row[OFFSET] + row[DURATION]), row[TRACK], row[CONTINUATION]])
            last_silence = False

    sort_events.sort(key=lambda tup: tup[2])
    from fractions import Fraction as frac

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
            track.append(Message('note_on', note=int(evt[0]), channel=channels[track_nb],
                                 velocity=vel, time=int((evt[2] - lapso[track_nb]) * ticks_per_beat)))

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

    if output_file is not None:
        for track in mid.tracks:
            track.append(MetaMessage('end_of_track', time=(int(0))))
        mid.save(output_file)
    return mid



def matrix_to_mid_one_channel_per_track(matrix, output_file=None, ticks_per_beat=96, tempo=120, instruments={}, **kwargs):
    """

    Parameters
    ----------
    matrix :
        
    output_file :
         (Default value = None)
    ticks_per_beat :
         (Default value = 96)
    tempo :
         (Default value = 120)
    instruments :
         (Default value = {})
    **kwargs :
        

    Returns
    -------

    """
    from mido import MidiFile, MidiTrack, Message, MetaMessage
    from ..constants import SILENCE, CONTINUATION, PITCH, TRACK, OFFSET, VELOCITY, DURATION
    from .constants import OCTAVES
    import os

    matrix = np.asarray(matrix)

    def number_to_channel(n):
        """

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

    mid = MidiFile()
    mid.ticks_per_beat = ticks_per_beat
    mid.type = 1

    # Take care of continuation
    # matrix = matrix[(matrix['pitch'] > 0) | (matrix['continuation'] > 0)]
    # Remove all continuations that follows a silence
    # Put all instruments with same name in same track


    # For each voice assign right track
    instrument_list = list(set(list(instruments.values())))

    # Replace with track in matrix

    nb_tracks = matrix[:, TRACK].max()
    for i in range(nb_tracks + 1):
        track = MidiTrack()
        if i in instruments.keys():
            track.append(Message('program_change', program=instruments.get(i, 0), time=0, channel=number_to_channel(i)))
        elif i != 9:
            track.append(Message('program_change', program=0, time=0, channel=number_to_channel(i)))
        mid.tracks.append(track)

    if output_file is not None:
        mid.tracks[0].append(MetaMessage("track_name", name=os.path.split(output_file)[1], time=int(0)))
        mid.tracks[0].append(MetaMessage("set_tempo", tempo=(480000 * 120) // tempo, time=int(0)))
        mid.tracks[0].append(MetaMessage("time_signature", numerator=4, denominator=4, time=int(0)))

    sort_events = []
    last_silence = True
    for row in matrix:
        pitch = row[PITCH] + 60 + 12 * OCTAVES.get(instruments.get(row[TRACK], 0), 0)
        row = row.tolist()
        if row[SILENCE]:
            last_silence = True
            continue
        if row[CONTINUATION] == 0:
            sort_events.append([pitch,
                                1, row[OFFSET], row[VELOCITY], row[TRACK]])

        if not (row[CONTINUATION] and last_silence):
            sort_events.append([pitch, 0, (row[OFFSET] + row[DURATION]), row[TRACK], row[CONTINUATION]])
            last_silence = False

    sort_events.sort(key=lambda tup: tup[2])
    from fractions import Fraction as frac

    lapso = {idx: 0 for idx in range(nb_tracks + 1)}
    prev_pitch = {idx: 0 for idx in range(nb_tracks + 1)}
    for evt in sort_events:
        if evt[1] == 1:
            vel = int(evt[3])
            track_nb = int(evt[4])
            track = mid.tracks[track_nb]
            track.append(Message('note_on', note=int(evt[0]), channel=number_to_channel(track_nb),
                                 velocity=vel, time=int((evt[2] - lapso[track_nb]) * ticks_per_beat)))

            lapso[track_nb] = evt[2]
            prev_pitch[track_nb] = int(evt[0])
        elif evt[1] == 0:
            track_nb = int(evt[3])
            track = mid.tracks[track_nb]

            if evt[4] == 1 and prev_pitch[track_nb] > 0:
                track[-1] = Message('note_off', note=prev_pitch[track_nb], channel=number_to_channel(track_nb),
                                    velocity=0, time=int((evt[2] - lapso[track_nb]) * ticks_per_beat + track[-1].time))


            else:
                track.append(Message('note_off', note=int(evt[0]), channel=number_to_channel(track_nb),
                                     velocity=0, time=int((evt[2] - lapso[track_nb]) * ticks_per_beat)))
            lapso[track_nb] = evt[2]

    if output_file is not None:
        for track in mid.tracks:
            track.append(MetaMessage('end_of_track', time=(int(0))))
        mid.save(output_file)
    return mid
