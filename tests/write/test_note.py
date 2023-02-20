import pytest
from musiclang.library import *

import musiclang as ml

def test_notes_equal():

    n1 = ml.Note("s", 1, 0, 1)
    n2 = ml.Note("s", 1, 0, 1)
    assert n1 == n2

def test_notes_octave_different_not_equal():
    n1 = ml.Note("s", 1, 0, 1)
    n2 = ml.Note("s", 1, 1, 1)
    assert n1 != n2

def test_notes_duration_different_not_equal():
    n1 = ml.Note("s", 1, 0, 1)
    n2 = ml.Note("s", 1, 0, 2)
    assert n1 != n2

def test_notes_type_different_not_equal():
    n1 = ml.Note("s", 1, 0, 1)
    n2 = ml.Note("su", 1, 0, 1)
    assert n1 != n2

def test_notes_val_different_not_equal():
    n1 = ml.Note("su", 2, 0, 1)
    n2 = ml.Note("su", 1, 0, 1)
    assert n1 != n2



def test_as_key():
    note = s4.o(1).e.fff
    assert note.as_key() == s4

    note = s4.o(1).e.fff
    assert note.as_key(octave=True) == s4.o(1)

    note = s4.o(1).e.fff
    assert note.as_key(amp=True) == s4.fff
    note = s4.o(1).e.fff

    assert note.as_key(duration=True) == s4.e


def test_to_extension_note():
    chord = (I % I.M)['6']
    note = s2
    assert note.to_extension_note(chord) == b0
    assert note.o(1).to_extension_note(chord) == b0.o(1)
    assert note.e.o(1).to_extension_note(chord) == b0.e.o(1)
    assert note.e.o(1).fff.to_extension_note(chord) == b0.e.o(1).fff

    chord = (I % I.M)['2']
    note = s6
    assert note.to_extension_note(chord) == b0.o(1)
    note = s5
    assert note.to_extension_note(chord) == s5

    chord = (I % I.M)['2[add6]']
    note = s5
    assert note.to_extension_note(chord) == b4


def test_to_chord_note():
    chord = (I % I.M)['6']
    note = s2
    assert note.to_chord_note(chord) == c1
    assert note.o(1).to_chord_note(chord) == c1.o(1)
    assert note.e.o(1).to_chord_note(chord) == c1.e.o(1)
    assert note.e.o(1).fff.to_chord_note(chord) == c1.e.o(1).fff
    chord = (I % I.M)['2[add6]']
    note = s5
    assert note.to_chord_note(chord) == c3
