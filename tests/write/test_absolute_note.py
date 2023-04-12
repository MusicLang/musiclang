from musiclang.library import *

def test_absolute_note_basics():

    chord = (I % I.M)
    assert chord.to_pitch(C5) == 0
    assert chord.to_pitch(Cs5) == 1
    chord = (V % II.b.M)['6']
    assert chord.to_pitch(C5) == 0
    assert chord.to_pitch(Cs5) == 1


def test_absolute_note_no_octave():
    assert C5.o(1) == C6
