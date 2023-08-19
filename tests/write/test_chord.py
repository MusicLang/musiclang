from musiclang import Chord, Element, Tonality
from musiclang.library import *

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
    assert chord['7'].chord_pitches == [0, 4, 7, 11]


def test_chord_pitches_ninth():

    chord = Element(0) % Tonality(0)
    assert chord['9'].chord_pitches == [0, 4, 7, 11, 14]

def test_chord_pitches():

    chord = Element(0) % Tonality(0)
    assert chord.chord_pitches == [0, 4, 7]

def test_chord_from_element():
    chord = Element(0) % Element(3).s.m
    assert chord.scale_pitches == [6, 8, 9, 11, 13, 14, 17]


def test_chord_notes_to_scale_pitches_with_octave():
    chord = (I % I.M.o(1)).o(1)
    pitch = chord.to_pitch(c0)

    assert pitch == 24



def test_patternize_melody():
    chord = ((I % I.M)(
        piano__0=s0.h.mp + s4.o(-1).mp,
        piano__3=s0.h.o(-1).p + s4.o(-2).p))
    expected_pattern = (
    (I % I.M)(
        v__0=x0.h.mp + bd1.mp))

    data, pattern = chord.patternize(melody=True)

    assert pattern == expected_pattern
    assert data['metadata']['melody'] == True
    assert data['voicing'] == [b0]
    assert data['metadata']['bar_duration'] == 3


def test_patternize_melody_with_octave_voicing():
    chord = ((I % VII.b.M)(
        piano__0=s0.h.mp + s4.o(-1).mp,
        piano__3=s0.h.o(-1).p + s4.o(-2).p))
    expected_pattern = (
    (I % I.M)(
        v__0=x0.h.mp + bd1.mp))

    data, pattern = chord.patternize(melody=True)

    assert pattern == expected_pattern
    assert data['metadata']['melody'] == True
    assert data['voicing'] == [b0.o(1)]
    assert data['metadata']['bar_duration'] == 3


def test_patternize_acc():
    chord = ((I % VII.b.M)(
        piano__0=s0.h.mp + s4.o(-1).mp,
        piano__3=s0.h.o(-1).p + s4.o(-2).p))
    expected_pattern = (
    (I % I.M)(
        v__0=x0.h.p + bd1.p))

    data, pattern = chord.patternize(melody=False, nb_excluded_instruments=1)

    assert pattern == expected_pattern
    assert data['metadata']['melody'] == False
    assert data['voicing'] == [b0]
    assert data['metadata']['bar_duration'] == 3


