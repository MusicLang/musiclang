from musiclang.library import *

def test_extension_notes_basics():

    chord = (I % I.M)
    assert chord.to_pitch(b0) == 0
    chord = (I % I.M)['6']
    assert chord.to_pitch(b0) == 4
    assert chord.to_pitch(b1) == 7
    assert chord.to_pitch(b2) == 12
    assert chord.to_pitch(b3) == 16
    assert chord.to_pitch(b0.o(1)) == 16
    assert chord.to_pitch(b0.o(-1)) == -8



def test_extension_notes_complicated_chord():

    chord = (I % I.M)['2[add2]']
    assert chord.to_pitch(b0) == -1
    assert chord.to_pitch(b1) == 0
    assert chord.to_pitch(b2) == 2
    assert chord.to_pitch(b3) == 4


def test_extension_notes_to_scale_pitches_with_octave():
    chord = (I % I.M.o(1)).o(1)
    pitch = chord.to_pitch(b0)

    assert pitch == 24


