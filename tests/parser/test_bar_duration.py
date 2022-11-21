import numpy as np
from musiclang.parser.bar_duration import BarDurationEstimator


def test_get_mean_pitches_every_beat():


    notes = [
        [0, 60],
        [0, 62],
        [1, 64]

    ]
    duration = 1
    offset = 0
    notes = np.asarray(notes)
    mean_pitches = BarDurationEstimator()._get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=False)
    assert mean_pitches == 1.5


def test_get_mean_pitches_every_beat_with_offset():


    notes = [
        [0, 60],
        [0, 62],
        [1, 64]

    ]
    duration = 1
    offset = 0.5
    notes = np.asarray(notes)
    mean_pitches = BarDurationEstimator()._get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=False)
    assert mean_pitches == 0


def test_get_mean_pitches_every_beat_with_offset2():


    notes = [
        [0, 60],
        [0, 62],
        [1.5, 64]

    ]
    duration = 1
    offset = 0.5
    notes = np.asarray(notes)
    mean_pitches = BarDurationEstimator()._get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=False)
    assert mean_pitches == 0.5


def test_get_mean_pitches_every_beat_with_other_duration_and_offset():

    notes = [
        [0.5, 60],
        [0.5, 62],
        [1.5, 64],
        [3.05, 62],
        [3.01, 64]
    ]

    duration = 1.5
    offset = 0
    notes = np.asarray(notes)
    mean_pitches = BarDurationEstimator()._get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=False)
    assert mean_pitches == 1




def test_binary_or_ternary():
    notes = [
        [0, 60, 1],
        [0, 60, 1],
        [1, 60, 1],
        [2, 60, 1],
        [3, 60, 1],
        [4, 60, 1],
        [4, 60, 1],
        [5, 62, 1],
        [6, 62, 1],
        [7, 62, 1],
    ]
    notes = np.asarray(notes)
    feel = BarDurationEstimator()._get_binary_or_ternary(notes)
    assert feel == 2

def test_find_feel_fourth():
    notes = [
        [0, 60, 1],
        [0, 60, 1],
        [1, 60, 1],
        [2, 60, 1],
        [3, 60, 1],
        [4, 60, 1],
        [4, 60, 1],
        [5, 60, 1],
        [6, 60, 1],
        [7, 60, 1],
    ]
    notes = np.asarray(notes)
    feel = BarDurationEstimator()._get_binary_or_ternary(notes)
    assert feel == 2

import pytest

@pytest.mark.skip(reason="Not long enough sequence")
def test_find_bar_duration_fourth_offset():
    notes = [
        [0, 60, 1],
        [0, 60, 1],
        [1, 60, 1],
        [2, 60, 1],
        [3, 60, 1],
        [4, 60, 1],
        [4, 60, 1],
        [5, 60, 1],
        [6, 60, 1],
        [7, 60, 1],
        [8, 60, 1],
        [8, 60, 1],
        [1+8, 60, 1],
        [2+8, 60, 1],
        [3+8, 60, 1],
        [4+8, 60, 1],
        [4+8, 60, 1],
        [5+8, 60, 1],
        [6+8, 60, 1],
        [7+8, 60, 1],
    ]
    notes = np.asarray(notes, dtype=float)
    notes[:, 0] += 0.5
    bar_duration, offset = BarDurationEstimator().estimate(notes)
    assert offset == 0.5


def test_get_offset():
    notes = [
        [0, 60, 1],
        [0, 60, 1],
        [1, 60, 1],
        [2, 60, 1],
        [3, 60, 1],
        [4, 60, 1],
        [4, 60, 1],
        [5, 60, 1],
        [6, 60, 1],
        [7, 60, 1],
    ]
    notes = np.asarray(notes, dtype=float)
    notes[:, 0] -= 0.5
    offset = BarDurationEstimator()._get_offset(notes, 2)
    assert (offset % 2) == 1.5

@pytest.mark.skip(reason="Not long enough sequence")
def test_find_bar_duration_fourth_other_offset():
    notes = [
        [0, 60, 1],
        [0, 60, 1],
        [1, 60, 1],
        [2, 60, 1],
        [3, 60, 1],
        [4, 60, 1],
        [4, 60, 1],
        [5, 60, 1],
        [6, 60, 1],
        [7, 60, 1],
    ]
    notes = np.asarray(notes, dtype=float)
    notes[:, 0] -= 0.5
    bar_duration, offset = BarDurationEstimator().estimate(notes)

    assert offset == -0.5
    assert bar_duration == 4, 'Wrong bar duration'

@pytest.mark.skip(reason="Not long enough sequence")
def test_find_bar_duration_three():
    notes = [
        [0, 60, 1],
        [0, 60, 1],
        [1, 60, 1],
        [2, 60, 1],
        [3, 60, 1],
        [3, 60, 1],
        [5, 60, 1],
        [6, 60, 1],
        [6, 60, 1],
    ]
    notes = np.asarray(notes, dtype=float)
    bar_duration, offset = BarDurationEstimator().estimate(notes)

    assert bar_duration == 3, 'Wrong bar duration'
    assert offset == 0, "Wrong offset"

@pytest.mark.skip(reason="Not long enough sequence")
def test_find_bar_duration_three_with_offset():
    notes = [
        [0, 60, 1],
        [0, 60, 1],
        [1, 60, 1],
        [2, 60, 1],
        [3, 60, 1],
        [3, 60, 1],
        [5, 60, 1],
        [6, 60, 1],
        [6, 60, 1],
    ]
    notes = np.asarray(notes, dtype=float)
    notes[:, 0] -= 0.5
    bar_duration, offset = BarDurationEstimator().estimate(notes)
    assert bar_duration == 3, 'Wrong bar duration'
    assert offset == -0.5, "Wrong offset"