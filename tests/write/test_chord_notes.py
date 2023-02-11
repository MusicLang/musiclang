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


def test_some_chords_works():
    D_major_sus2_second_inversion = (I % II.M)['64(sus2)']  # I in key of D major
    assert D_major_sus2_second_inversion.extension_notes == [s4, s0.o(1), s1.o(1)]
    augmented = (I % II.M)['(+)']
    assert augmented.extension_notes == [s0, s2, h8]
    add_sixth = (I % II.M)['[add6]']
    assert add_sixth.extension_notes == [s0, s2, s4, s5]