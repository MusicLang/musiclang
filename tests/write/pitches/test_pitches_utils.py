from musiclang.write.pitches.pitches_utils import *
from musiclang import Note

def test_relative_scale_up_value():

    new_pitch = relative_scale_up_value(1, 12, [0, 2, 4, 5, 7, 9, 11])

    assert new_pitch == 14

def test_relative_scale_up_value_negative():
    new_pitch = relative_scale_up_value(1, -2, [0, 2, 4, 5, 7, 9, 11])

    assert new_pitch == -1


def test_relative_scale_up_value_octave():

    new_pitch = relative_scale_up_value(8, 12, [0, 2, 4, 5, 7, 9, 11])
    assert new_pitch == 26

def test_relative_scale_up_value_not_in_scale():

    new_pitch = relative_scale_up_value(1, 13, [0, 2, 4, 5, 7, 9, 11])

    assert new_pitch == 14



def test_relative_scale_down_value():
    new_pitch = relative_scale_down_value(1, 12, [0, 2, 4, 5, 7, 9, 11])

    assert new_pitch == 11



def test_relative_scale_down_value_not_in_scale():

    new_pitch = relative_scale_down_value(1, 13, [0, 2, 4, 5, 7, 9, 11])

    assert new_pitch == 12


def test_get_relative_scale_value():

    note = Note("su", 1, 1, 1)
    last_pitch = -2
    scale_pitches = [0, 2, 4, 5, 7, 9, 11]
    result = get_relative_scale_value(note, last_pitch, scale_pitches)

    assert result == 11

def test_get_relative_scale_value_down():

    note = Note("sd", 1, 0, 1)
    last_pitch = -1
    scale_pitches = [0, 2, 4, 5, 7, 9, 11]
    result = get_relative_scale_value(note, last_pitch, scale_pitches)

    assert result == -3