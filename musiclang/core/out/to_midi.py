from ..note_pitch import NotePitch

import numpy as np


def get_track_list(score):
    items = sum([chord.parts for chord in score.chords], [])
    tracks = list(dict.fromkeys(items))

    return tracks


def get_or_default_last_pitch(chord, track_idx, time, last_pitch):
    if last_pitch is not None:
        return last_pitch

    return NotePitch(chord.scale_pitches[0], offset=time - 1, duration=1, track=track_idx).to_midi_note()


def relative_scale_up_value(delta, last_pitch, scale_pitches):
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
    if note.is_up:
        return relative_scale_up_value(note.val + 7 * note.octave, last_pitch, scale_pitches)
    elif note.is_down:
        return relative_scale_down_value(note.val + 7 * note.octave, last_pitch, scale_pitches)
    else:
        pass


def get_value_to_scale_note(value, scale_pitches):
    return scale_pitches[value % len(scale_pitches)] + 12 * (value // len(scale_pitches))


def note_to_pitch(note, chord, track_idx, time, last_pitch):

    # Get real scale pitches
    real_chord = note.real_chord(chord)
    scale_pitches = real_chord.scale_pitches
    last_pitch_pitch = last_pitch[0]

    pitch_result = 0
    if not note.is_relative:
        if note.is_scale_note:
            pitch_result = get_value_to_scale_note(note.val + 7 * note.octave, scale_pitches)
        elif note.is_chord_note:
            raise Exception('Chord notes parsing are not implemented yet')
            pass
        elif note.is_chromatic_note:
            raise Exception('Chromatic notes parsing are not implemented yet')

    elif note.is_relative:
        if note.is_scale_note:
            pitch_result = get_relative_scale_value(note, last_pitch_pitch, scale_pitches)
            pass
        elif note.is_chord_note:
            raise Exception('Relative chord notes parsing are not implemented yet')
            pass
        elif note.is_chromatic_note:
            raise Exception('Relative chromatic notes parsing are not implemented yet')
            pass

    pitch = NotePitch(pitch_result, offset=time, duration=note.duration, track=track_idx,
                      velocity=note.amp, silence=1 * note.is_silence, continuation=1 * note.is_continuation)

    if pitch.is_note():
        last_pitch = pitch.to_midi_note()

    return pitch.to_midi_note(), last_pitch


def melody_to_pitches(part, chord, track_idx, time, last_pitch):
    chord_result = []
    for note in part.notes:
        to_append, last_pitch = note_to_pitch(note, chord, track_idx, time, last_pitch)
        time += note.duration
        chord_result.append(to_append)

    return chord_result, last_pitch


def create_melody_for_track(score, track_idx, track):
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
    from .midi_utils import matrix_to_mid
    res = matrix_to_mid(notes, output_file=output_file, **kwargs)
    return res


def tracks_to_instruments(tracks):
    from .constants import INSTRUMENTS_DICT
    names = [t.split('__')[0] for t in tracks]
    instruments_idx = {i: INSTRUMENTS_DICT[name] for i, name in enumerate(names)}
    return instruments_idx


def score_to_midi(score, filepath, **kwargs):
    """
    Transform a score to a midi file
    :param score:
    :param filepath:
    :param kwargs:
    :return:
    """

    # Get all tracks
    tracks = get_track_list(score)

    # For each track create melody
    notes = []
    for track_idx, track in enumerate(tracks):
        melody = create_melody_for_track(score, track_idx, track)
        notes += melody

    instruments = tracks_to_instruments(tracks)
    res = to_midi(notes, output_file=filepath, instruments=instruments)
    return res
