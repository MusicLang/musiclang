"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

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

    return NotePitch(chord.scale_pitches[0], offset=time - 1, duration=1, track=track_idx).to_midi_note()


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
                      velocity=note.amp, silence=1 * note.is_silence, continuation=1 * note.is_continuation)

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
    for chord in score.chords:
        last_pitch = get_or_default_last_pitch(chord, track_idx, time, last_pitch)
        if track in chord.score.keys():
            part = chord.score[track]
            chord_result, last_pitch = melody_to_pitches(part, chord, track_idx, time, last_pitch)
            result += chord_result

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
    return instruments_idx


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
    notes = []
    for track_idx, track in enumerate(tracks):
        melody = create_melody_for_track(score, track_idx, track)
        notes += melody

    instruments = tracks_to_instruments(tracks)
    res = to_midi(notes, output_file=filepath, instruments=instruments, **kwargs)
    return res
