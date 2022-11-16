
import numpy as np



_PERC_CHANNEL = 9

def voice_to_track(instrument_list, voice, instruments):
    instrument_of_voice = instruments.get(voice, 0)
    return instrument_list.index(instrument_of_voice)



def number_to_channel(n):
    if n < _PERC_CHANNEL:
        return n
    if n >= _PERC_CHANNEL:
        return n + 1

def matrix_to_mid(matrix, output_file=None, ticks_per_beat=96, tempo=120, instruments={}, **kwargs):
    from mido import MidiFile, MidiTrack, Message, MetaMessage
    from ..constants import SILENCE, CONTINUATION, PITCH, TRACK, OFFSET, VELOCITY, DURATION
    from .constants import OCTAVES
    import os

    matrix = np.asarray(matrix)


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

    nb_tracks = len(instrument_list)



    for i in range(nb_tracks):
        track = MidiTrack()
        if i in instruments.keys():
            track.append(Message('program_change', program=instrument_list[i], time=0, channel=number_to_channel(i)))
        elif i != _PERC_CHANNEL:
            track.append(Message('program_change', program=0, time=0, channel=number_to_channel(i)))
        mid.tracks.append(track)

    if output_file is not None:
        mid.tracks[0].append(MetaMessage("track_name", name=os.path.split(output_file)[1], time=int(0)))
        mid.tracks[0].append(MetaMessage("set_tempo", tempo=(480000 * 120) // tempo, time=int(0)))
        mid.tracks[0].append(MetaMessage("time_signature", numerator=4, denominator=4, time=int(0)))

    sort_events = []
    last_silence = True
    events = []
    idx = 0

    for row in matrix:
        pitch = row[PITCH] + 60 + 12 * OCTAVES.get(instruments.get(row[TRACK], 0), 0)
        row = row.tolist()
        if row[SILENCE]:
            last_silence = True
            continue
        if row[CONTINUATION] == 0:
            sort_events.append([pitch,
                                1, row[OFFSET], row[VELOCITY], row[TRACK]])

        sort_events.append([pitch, 0, (row[OFFSET] + row[DURATION]), row[TRACK], row[CONTINUATION]])
        last_silence = False

    sort_events.sort(key=lambda tup: tup[2])
    from fractions import Fraction as frac
    from itertools import product
    track_voices = product(list(range(nb_tracks)), list(instruments.keys()))
    lapso = {idx: 0 for idx in range(nb_tracks)}
    prev_pitch = {idx: 0 for idx in track_voices}
    lapso_track_index = {idx: 0 for idx in track_voices}
    prev_track_index = {idx: 0 for idx in track_voices}
    for evt in sort_events:
        if evt[1] == 1:
            vel = int(evt[3])
            track_idx = int(evt[4])
            track_nb = voice_to_track(instrument_list, track_idx, instruments)
            if track_nb != 0:
                print(track_nb)
            track = mid.tracks[track_nb]
            track.append(Message('note_on', note=int(evt[0]), channel=number_to_channel(track_nb),
                                 velocity=vel, time=int((evt[2] - lapso[track_nb]) * ticks_per_beat)))

            lapso[track_nb] = evt[2]
            prev_pitch[track_nb, track_idx] = int(evt[0])

        elif evt[1] == 0:
            track_idx = int(evt[3])
            track_nb = voice_to_track(instrument_list, track_idx, instruments)
            track = mid.tracks[track_nb]

            if evt[4] == 1 and prev_pitch[track_nb, track_idx] > 0:
                message = track[prev_track_index[track_nb, track_idx]]
                next_message = track[prev_track_index[track_nb, track_idx] + 1]
                delta_time = int((evt[2] - lapso[track_nb]) * ticks_per_beat)
                message.time += delta_time
                next_message.time -= delta_time
            else:
                message = Message('note_off', note=int(evt[0]), channel=number_to_channel(track_nb),
                                     velocity=0, time=int((evt[2] - lapso[track_nb]) * ticks_per_beat))
                track.append(message)
                prev_track_index[track_nb, track_idx] = len(track) - 2
                lapso[track_nb] = evt[2]

    if output_file is not None:
        for track in mid.tracks:
            track.append(MetaMessage('end_of_track', time=(int(0))))
        mid.save(output_file)
    return mid
