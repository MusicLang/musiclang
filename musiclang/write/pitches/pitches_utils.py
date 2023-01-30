"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import numpy as np

def relative_scale_up_value(delta, last_pitch, scale_pitches):
    """

    Parameters
    ----------
    delta :
        
    last_pitch :
        
    scale_pitches :
        

    Returns
    -------

    """
    scale_mod = list(sorted([i % 12 for i in scale_pitches]))
    # Get scale index
    if delta == 0:
        new_pitch = last_pitch
    else:
        whole_scale = [s + octave * 12 for octave in range(-5, 5) for s in scale_mod]
        dists = np.asarray(whole_scale) - last_pitch
        dists = dists[dists >= 0] + last_pitch
        new_pitch = dists[delta - 1 * (last_pitch not in whole_scale)]

    return new_pitch


def relative_scale_down_value(delta, last_pitch, scale_pitches):
    """

    Parameters
    ----------
    delta :
        
    last_pitch :
        
    scale_pitches :
        

    Returns
    -------

    """
    scale_mod = list(sorted([i % 12 for i in scale_pitches]))
    # Get scale index
    if delta == 0:
        new_pitch = last_pitch
    else:
        whole_scale = [s + octave * 12 for octave in range(-5, 5) for s in scale_mod]
        dists = np.asarray(whole_scale) - last_pitch
        dists = dists[dists <= 0] + last_pitch
        new_pitch = dists[-(delta + 1) + 1 * (last_pitch not in whole_scale)]
    return new_pitch


def get_relative_scale_value(note, last_pitch, scale_pitches):
    """

    Parameters
    ----------
    note :
        
    last_pitch :
        
    scale_pitches :
        

    Returns
    -------

    """
    if note.is_up:
        return relative_scale_up_value(note.val + 7 * note.octave, last_pitch, scale_pitches)
    elif note.is_down:
        return relative_scale_down_value(note.val + 7 * note.octave, last_pitch, scale_pitches)
    else:
        pass


def get_value_to_scale_note_with_accident(note, chord):
    """
    Get the value of the note if there is an accident
    Parameters
    ----------
    note
    chord

    Returns
    -------

    """
    from musiclang.write.constants import ACCIDENTS_TO_NOTE
    tonic = chord.scale_pitches[0]
    return tonic + ACCIDENTS_TO_NOTE[(note.val, note.accident)] + 12 * note.octave

def get_value_to_scale_note(value, scale_pitches):
    """

    Parameters
    ----------
    value :
        
    scale_pitches :
        

    Returns
    -------

    """
    return scale_pitches[value % len(scale_pitches)] + 12 * (value // len(scale_pitches))

def note_to_pitch_result(note, chord, last_pitch=None):
    """

    Parameters
    ----------
    note :
        
    chord :
        
    last_pitch :
         (Default value = None)

    Returns
    -------
    pitch: int
           Resulting pitch

    """
    real_chord = note.real_chord(chord)
    scale_pitches = real_chord.scale_pitches

    pitch_result = None
    if not note.is_relative:
        if note.has_accident:
            pitch_result = get_value_to_scale_note_with_accident(note, real_chord)
        elif note.is_scale_note:
            pitch_result = get_value_to_scale_note(note.val + 7 * note.octave, scale_pitches)
        elif note.is_chord_note:
            raise Exception('Chord notes parsing are not implemented yet')
            pass
        elif note.is_chromatic_note:
            chromatic_pitches = [scale_pitches[0] + i for i in range(12)]
            pitch_result = get_value_to_scale_note(note.val + 12 * note.octave, chromatic_pitches)

    elif note.is_relative:
        if note.is_scale_note:
            pitch_result = get_relative_scale_value(note, last_pitch, scale_pitches)
            pass
        elif note.is_chord_note:
            raise Exception('Relative chord notes parsing are not implemented yet')
            pass
        elif note.is_chromatic_note:
            raise Exception('Relative chromatic notes parsing are not implemented yet')
            pass

    return pitch_result
