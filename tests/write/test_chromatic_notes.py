from musiclang.library import *

def test_chromatic_notes_to_scale_pitches_with_octave():
    chord = (I % II.M.o(1)).o(1)
    pitch = chord.to_pitch(h1)
    assert pitch == 27