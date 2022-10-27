import pytest

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


