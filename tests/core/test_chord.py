from musiclang import Chord, Element, Tonality

def test_chord_to_scale_pitches():
    chord = Element(2) % Tonality(1, mode="m", octave=1)
    scale_pitches = chord.scale_pitches

    assert scale_pitches == [16, 18, 20, 21, 24, 25, 27]


def test_initial_chord_to_scale_pitches():
    chord = Element(1)
    scale_pitches = chord.scale_pitches

    assert scale_pitches == [2, 4, 5, 7, 9, 11, 12]


def test_chord_with_mode_to_scale_pitches():
    chord = Element(1) % Tonality(1, mode="locrian", octave=0)
    scale_pitches = chord.scale_pitches

    assert scale_pitches == [2, 4, 6, 7, 9, 11, 13]

def test_chord_with_mode_to_scale_pitches2():
    T = Tonality(1, mode="locrian", octave=0)
    chord = Element(1) % (T + T)
    scale_pitches = chord.scale_pitches
    assert scale_pitches == [3, 5, 7, 8, 10, 12, 14]


def test_chord_pitches_seventh():

    chord = Element(0) % Tonality(0)
    assert chord[7].chord_pitches == [0, 4, 7, 11]


def test_chord_pitches_ninth():

    chord = Element(0) % Tonality(0)
    assert chord[9].chord_pitches == [0, 4, 7, 11, 2]

def test_chord_pitches():

    chord = Element(0) % Tonality(0)
    assert chord.chord_pitches == [0, 4, 7]

def test_chord_from_element():
    chord = Element(0) % Element(3).s.m
    assert chord.scale_pitches == [6, 8, 9, 11, 13, 14, 17]