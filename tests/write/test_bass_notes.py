from musiclang.library import *

def test_bass_note_basics():

    chord = (I % I.M)
    assert chord.to_pitch(b0) == 0
    chord = (I % I.M)['6']
    assert chord.to_pitch(b0) == 4
    assert chord.to_pitch(b1) == 7
    assert chord.to_pitch(b2) == 12
    assert chord.to_pitch(b3) == 16
    assert chord.to_pitch(b0.o(1)) == 16
    assert chord.to_pitch(b0.o(-1)) == -8



def test_bass_note_complicated_chord():

    chord = (I % I.M)['2[add2]']
    assert chord.to_pitch(b0) == -1
    assert chord.to_pitch(b1) == 0
    assert chord.to_pitch(b2) == 2
    assert chord.to_pitch(b3) == 4
