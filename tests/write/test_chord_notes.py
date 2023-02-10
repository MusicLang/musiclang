from musiclang.library import *

def test_chord_note_basics():

    chord = (I % I.M)
    assert chord.to_pitch(c0) == 0
    chord = (I % I.M)['6']
    assert chord.to_pitch(c0) == 0
    assert chord.to_pitch(c1) == 4
    assert chord.to_pitch(c2) == 7
    assert chord.to_pitch(c3) == 12
    assert chord.to_pitch(c0.o(1)) == 12
    assert chord.to_pitch(c0.o(-1)) == -12



def test_chord_note_complicated_chord():

    chord = (II % II.M)['2[add2]']
    assert chord.to_pitch(c0) == 4
    assert chord.to_pitch(c1) == 6
    assert chord.to_pitch(c2) == 7
    assert chord.to_pitch(c3) == 11