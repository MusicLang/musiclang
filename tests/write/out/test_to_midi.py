from musiclang import Chord, Tonality, Element, Silence, Note, Continuation
from musiclang.write.out.to_midi import *


def test_note_to_pitch_down():
    from musiclang import Chord, Tonality, Element

    note = Note("sd", 1, 0, 1)
    last_pitch = [12]
    chord = Element(3) % Tonality(2, mode="m", octave=-1)
    result = note_to_pitch(note, chord, 0, 12, last_pitch)
    res = [10, 12, 1, 66, 0, 0, 0, None, None]
    assert result == (res, res)


def test_note_to_pitch_up():
    note = Note("su", 1, 0, 1)
    last_pitch = [12]
    chord = Element(3) % Tonality(1, mode="m", octave=-1)
    result = note_to_pitch(note, chord, 0, 12, last_pitch)
    res = [13, 12, 1, 66, 0, 0, 0, None, None]
    assert result == (res, res)


def test_note_to_pitch_abs():
    from musiclang import Chord, Tonality, Element

    note = Note("s", 1, -1, 1)
    last_pitch = [12]
    chord = Element(3) % Tonality(2, mode="m", octave=-1)
    result = note_to_pitch(note, chord, 0, 12, last_pitch)
    res = [-15, 12, 1, 66, 0, 0, 0, None, None]
    assert result == (res, res)


def test_note_to_pitch_abs_octave_tonality():
    from musiclang import Chord, Tonality, Element

    note = Note("s", 1, -1, 1)
    last_pitch = [12]
    chord = Element(3).o(1) % Tonality(2, mode="m", octave=-1)
    result = note_to_pitch(note, chord, 0, 12, last_pitch)
    res = [-3, 12, 1, 66, 0, 0, 0, None, None]
    assert result == (res, res)


def test_note_to_pitch_silence():
    note = Silence(1)
    last_pitch = [12]
    chord = Element(3) % Tonality(1, mode="m", octave=-1)
    result = note_to_pitch(note, chord, 0, 12, last_pitch)
    res = [0, 12, 1, 66, 0, 1, 0, None, None]
    assert result == (res, last_pitch)


def test_note_to_pitch_continuation():
    note = Continuation(1)
    last_pitch = [12]
    chord = Element(3) % Tonality(1, mode="m", octave=-1)
    result = note_to_pitch(note, chord, 0, 12, last_pitch)
    res = [0, 12, 1, 66, 0, 0, 1, None, None]
    assert result == (res, last_pitch)


def test_to_midi():
    notes = [[0, 12, 1, 66, 0, 0, 0, None, None], [0, 12, 1, 66, 0, 0, 0, None, None]]
    res = to_midi(notes, output_file=None)
    assert res is not None


def test_score_to_midi():
    from musiclang.write.library import s0, s1, s2, I
    score = I(piano__0=s0 + s1 + s2)
    res = score_to_midi(score, None)
    assert res is not None


def test_get_track_list():
    from musiclang.write.library import s0, s1, s2, I
    chord1 = I(piano__0=s0 + s1 + s2, piano__1=s0 + s1 + s2, violin__0=s0 + s1 + s2)
    chord2 = I(piano__0=s0 + s1 + s2, oboe__0=s0 + s1 + s2, violin__0=s0 + s1 + s2)
    score = chord1 + chord2
    tracks = get_track_list(score)

    assert tracks == ['piano__0', 'piano__1', 'violin__0', 'oboe__0']


def test_tracks_to_instruments():
    res, names = tracks_to_instruments(['piano__0', 'violin__0'])
    assert res == {0: 0, 1: 40}
    assert names == ['piano', 'violin']


def test_create_melody_for_track():
    from musiclang.write.library import s0, s1, s2, I, V
    chord1 = I(piano__0=s0 + s1 + s2, piano__1=s0 + s1 + s2, violin__0=s0 + s1 + s2)
    chord2 = V(piano__0=s0 + s1 + s2, oboe__0=s0 + s1 + s2, violin__0=s0 + s1 + s2)
    score = chord1 + chord2

    res = create_melody_for_track(score, 0, 'piano__0')
    expected_res = [[0, 0, 1, 66, 0, 0, 0, None, None],
                    [2, 1, 1, 66, 0, 0, 0, None, None],
                    [4, 2, 1, 66, 0, 0, 0, None, None],
                    [7, 3, 1, 66, 0, 0, 0, None, None],
                    [9, 4, 1, 66, 0, 0, 0, None, None],
                    [11, 5, 1, 66, 0, 0, 0, None, None]]
    assert res == expected_res
