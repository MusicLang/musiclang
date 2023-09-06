"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
from ..constants import CONTINUATION, SILENCE
from ..note_pitch import NotePitch
from ..pitches.pitches_utils import note_to_pitch_result


def get_track_list(score):
    """

    Parameters
    ----------
    score :
        

    Returns
    -------

    """
    items = sum([chord.parts for chord in score.chords], [])
    tracks = list(dict.fromkeys(items))

    return tracks


def get_or_default_last_pitch(chord, track_idx, time, last_pitch):
    """

    Parameters
    ----------
    chord :
        
    track_idx :
        
    time :
        
    last_pitch :
        

    Returns
    -------

    """
    if last_pitch is not None:
        return last_pitch

    return None


def note_to_pitch(note, chord, track_idx, time, last_pitch):
    """

    Parameters
    ----------
    note :
        
    chord :
        
    track_idx :
        
    time :
        
    last_pitch :
        

    Returns
    -------

    """

    # Get real scale pitches
    if last_pitch is not None:
        last_pitch_pitch = last_pitch[0]
    else:
        last_pitch_pitch = 0

    pitch_result = note_to_pitch_result(note, chord, last_pitch=last_pitch_pitch)

    if pitch_result is None:
        pitch_result = 0

    pitch = NotePitch(pitch_result, offset=time, duration=note.duration, track=track_idx,
                      velocity=note.amp,
                      silence=1 * (note.is_silence or (note.is_continuation and last_pitch is None)),
                      continuation=1 * (note.is_continuation and last_pitch is not None),
                      tempo= note.tempo,
                      pedal= note.pedal
                      )

    if pitch.is_note():
        last_pitch = pitch.to_midi_note()

    return pitch.to_midi_note(), last_pitch


def melody_to_pitches(part, chord, track_idx, time, last_pitch):
    """

    Parameters
    ----------
    part :
        
    chord :
        
    track_idx :
        
    time :
        
    last_pitch :
        

    Returns
    -------

    """
    chord_result = []
    for note in part.notes:
        to_append, last_pitch = note_to_pitch(note, chord, track_idx, time, last_pitch)
        time += note.duration
        chord_result.append(to_append)

    return chord_result, last_pitch


def create_melody_for_track(score, track_idx, track):
    """

    Parameters
    ----------
    score :
        
    track_idx :
        
    track :
        

    Returns
    -------

    """
    result = []
    last_pitch = None
    time = 0
    from musiclang import Melody, Silence
    for idx_chord, chord in enumerate(score.chords):
        if track in chord.score.keys():
            last_pitch = get_or_default_last_pitch(chord, track_idx, time, last_pitch)
            part = chord.score[track]
            last_note = score.chords[idx_chord - 1].score.get(track, Melody([Silence(1)])).notes[-1] if idx_chord -1 >= 0 else None
            next_note = score.chords[idx_chord + 1].score.get(track, Melody([Silence(1)])).notes[0] if idx_chord + 1 < len(score.chords) else None
            part_enriched = part.realize_tags(last_note=last_note, final_note=next_note)
            chord_result, last_pitch = melody_to_pitches(part_enriched, chord, track_idx, time, last_pitch)
            result += chord_result
        else:
            last_pitch = None
        time += chord.duration
    return result


def to_midi(notes, output_file=None, **kwargs):
    """

    Parameters
    ----------
    notes :
        
    output_file :
         (Default value = None)
    **kwargs :
        

    Returns
    -------

    """
    from .midi_utils import matrix_to_mid

    res = matrix_to_mid(notes, output_file=output_file, **kwargs)
    return res


def tracks_to_instruments(tracks):
    """

    Parameters
    ----------
    tracks :
        

    Returns
    -------

    """
    from .constants import INSTRUMENTS_DICT
    names = [t.split('__')[0] for t in tracks]
    instruments_idx = {i: INSTRUMENTS_DICT.get(name, 0) for i, name in enumerate(names)}
    return instruments_idx, names




def get_pitches_instruments(score):
    tracks = get_track_list(score)

    # For each track create melody
    melodies = []
    for track_idx, track in enumerate(tracks):
        melody = create_melody_for_track(score, track_idx, track)
        melodies.append([n[0] for n in melody if not n[CONTINUATION] and not n[SILENCE]])

    return melodies
def get_pitches(score):
    notes = get_notes(score)
    return [n[0] for n in notes if not n[CONTINUATION] and not n[SILENCE]]

def get_notes(score):
    """
    Get all notes from a score

    Parameters
    ----------
    score: Score
        The score to get notes from

    Returns
    -------
    notes: list
        A list of notes

    """
    # Get all tracks
    tracks = get_track_list(score)

    # For each track create melody
    notes = []
    for track_idx, track in enumerate(tracks):
        melody = create_melody_for_track(score, track_idx, track)
        notes += melody

    return notes



def score_to_midi(score, filepath, **kwargs):
    """Transform a score to a midi file

    Parameters
    ----------
    score :
        param filepath:
    kwargs :
        return:
    filepath :
        
    **kwargs :
        

    Returns
    -------

    """

    # Get all tracks
    tracks = get_track_list(score)

    # For each track create melody
    notes = get_notes(score)
    instruments, instrument_names = tracks_to_instruments(tracks)

    res = to_midi(notes, output_file=filepath, instruments=instruments, instrument_names=instrument_names, **kwargs)
    return res


def score_to_events(score, **kwargs):
    """Transform a score to a event list

    Parameters
    ----------
    score :
        param filepath:
    kwargs :
        return:
    filepath :

    **kwargs :


    Returns
    -------

    """

    # Get all tracks
    tracks = get_track_list(score)

    # For each track create melody
    notes = get_notes(score)
    instruments, instrument_names = tracks_to_instruments(tracks)

    res = matrix_to_events(notes, instruments=instruments, instrument_names=instrument_names, **kwargs)
    return res

def matrix_to_events(matrix,
                     ticks_per_beat=480,
                     tempo=120,
                     instruments={},
                     time_signature=(4, 4),
                     instrument_names=None, **kwargs):
    matrix = list(sorted(matrix, key=lambda x: x[1]))
    events = {}  # [(time, instrument, duration, message)]

    for idx, el in enumerate(matrix):
        pitch, offset, duration, velocity, track, silence, continuation, tempo_change, pedal = el
        # Add note on, note off for each track
        if tempo_change is not None:
            tempo = tempo_change

        real_instrument_name = instrument_names[track]
        second_offset = offset * 60 / tempo
        second_duration = float(duration * 60 / tempo)

        if not continuation:
            event = {
                'event_name': 'note_on',
                'duration': float(second_duration),
                'pitch': int(pitch),
                'offset': float(second_offset),
                'velocity': int(velocity),
                'instrument': real_instrument_name,
                'silence': silence,
                'pedal': pedal
            }

            events[track] = events.get(track, []) + [event]
        if continuation:
            last_event = events.get(track, None)
            if last_event is not None:
                last_event[-1]['duration'] += duration
            else:
                event = {
                    'event_name': 'note_on',
                    'duration': float(second_duration),
                    'pitch': int(pitch),
                    'offset': float(second_offset),
                    'velocity': int(velocity),
                    'instrument': real_instrument_name,
                    'silence': True,
                    'pedal': pedal
                }
                events[track] = events.get(track, []) + [event]

    events = sum([ev for key, ev in events.items()], [])
    events = [e for e in events if not e['silence']]
    events = list(sorted(events, key=lambda x: x['offset']))

    return events