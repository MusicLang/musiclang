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
    note : Note
    last_pitch : int
    scale_pitches : list[int]


    Returns
    -------
    pitch: int

    """
    scale_mod = list(sorted([i % 12 for i in scale_pitches]))
    # Get scale index
    if delta == 0:
        whole_scale = [s + octave * 12 for octave in range(-10, 10) for s in scale_mod]
        whole_scale = [s for s in whole_scale if s >= last_pitch]
        new_pitch = whole_scale[0]
        return new_pitch
    # else:
    whole_scale = [s + octave * 12 for octave in range(-10, 10) for s in scale_mod]
    dists = np.asarray(whole_scale) - last_pitch
    dists = dists[dists >= 0] + last_pitch
    new_pitch = dists[delta - 1 * (last_pitch not in whole_scale)]
    return new_pitch


def relative_scale_down_value(delta, last_pitch, scale_pitches):
    """

    Parameters
    ----------
    note : Note
    last_pitch : int
    scale_pitches : list[int]


    Returns
    -------
    pitch: int

    """
    scale_mod = list(sorted([i % 12 for i in scale_pitches]))
    # Get scale index
    if delta == 0:
        whole_scale = [s + octave * 12 for octave in range(-10, 10) for s in scale_mod]
        whole_scale = [s for s in whole_scale if s <= last_pitch]
        new_pitch = whole_scale[-1]
        return new_pitch
    # else:
    whole_scale = [s + octave * 12 for octave in range(-10, 10) for s in scale_mod]
    dists = np.asarray(whole_scale) - last_pitch
    dists = dists[dists <= 0] + last_pitch
    new_pitch = dists[-(delta + 1) + 1 * (last_pitch not in whole_scale)]
    return new_pitch


def get_relative_scale_value(note, last_pitch, scale_pitches):
    """
    Parameters
    ----------
    note : Note
    last_pitch : int
    scale_pitches : list[int]

    Returns
    -------
    pitch: int
    """
    # Remove non unique scale_pitches
    scale_pitches = list(sorted(set([s % 12 for s in scale_pitches])))
    total_val = note.val + len(scale_pitches) * note.octave
    if note.is_down: # su or sd
        total_val = - total_val
    if total_val > 0:
        return relative_scale_up_value(total_val, last_pitch, scale_pitches)
    elif total_val < 0:
        return relative_scale_down_value(-total_val, last_pitch, scale_pitches)
    elif total_val == 0:
        if last_pitch % 12 in [s % 12 for s in scale_pitches]:
            return last_pitch
        pitch_up = relative_scale_up_value(total_val, last_pitch, scale_pitches)
        pitch_down = relative_scale_down_value(-total_val, last_pitch, scale_pitches)
        # Select nearest from last pitch
        if abs(pitch_up - last_pitch) <= abs(pitch_down - last_pitch):
            return pitch_up
        return pitch_down
    else:
        raise Exception(f'This relative note {note} is nor up or down')


def get_value_to_scale_note_with_accident(note, chord):
    """
    Get the value of the note if there is an accident
    Parameters
    ----------
    note: Note
    chord: Chord

    Returns
    -------
    pitch: int

    """
    from musiclang.write.constants import ACCIDENTS_TO_NOTE
    tonic = chord.scale_pitches[0]
    return tonic + ACCIDENTS_TO_NOTE[(note.val, note.accident)] + 12 * (note.octave)

def get_value_to_scale_note(value, scale_pitches):
    """
    Transform an absolute value and a scale pitches to an unique pitch

    Parameters
    ----------
    value : int
        
    scale_pitches : list[int]
        

    Returns
    -------
    pitch: int

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
        if note.is_scale_note:
            if note.has_accident:
                pitch_result = get_value_to_scale_note_with_accident(note, real_chord)
            else:
                pitch_result = get_value_to_scale_note(note.val + 7 * note.octave, scale_pitches)
        elif note.is_chord_note:
            scale_chord = chord.chord_pitches
            pitch_result = get_value_to_scale_note(note.val + len(scale_chord) * note.octave, scale_chord)
        elif note.is_bass_note:
            scale_chord = chord.chord_extension_pitches
            pitch_result = get_value_to_scale_note(note.val + len(scale_chord) * note.octave, scale_chord)
        elif note.is_absolute_note:
            chromatic_pitches = list(range(12))
            pitch_result = get_value_to_scale_note(note.val + 12 * note.octave, chromatic_pitches)
        elif note.is_chromatic_note:
            chromatic_pitches = [scale_pitches[0] + i for i in range(12)]
            pitch_result = get_value_to_scale_note(note.val + 12 * note.octave, chromatic_pitches)
        elif note.is_drum_note:
            chromatic_pitches = list(range(12))
            pitch_result = get_value_to_scale_note(note.val + 12 * note.octave, chromatic_pitches)

    elif note.is_relative:
        if note.is_scale_note:
            pitch_result = get_relative_scale_value(note, last_pitch, scale_pitches)
            pass
        elif note.is_chord_note:
            scale_chord = chord.chord_pitches
            pitch_result = get_relative_scale_value(note, last_pitch, scale_chord)
            pass
        elif note.is_bass_note:
            scale_chord = chord.chord_extension_pitches
            pitch_result = get_relative_scale_value(note, last_pitch, scale_chord)
            pass
        elif note.is_chromatic_note:
            chromatic_pitches = chord.chromatic_pitches
            pitch_result = get_relative_scale_value(note, last_pitch, chromatic_pitches)
            pass
        else:
            raise Exception('This kind of note is not supported or has no pitch : {}'.format(note.type))

    return pitch_result
