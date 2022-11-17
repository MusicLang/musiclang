import numpy as np


from musiclang.analyze.utils import get_mean_pitches_every_beat, find_bar_duration


def test_get_mean_pitches_every_beat():


    notes = [
        [0, 60],
        [0, 62],
        [1, 64]

    ]
    duration = 1
    offset = 0
    notes = np.asarray(notes)
    mean_pitches = get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=False)
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
    mean_pitches = get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=False)
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
    mean_pitches = get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=False)
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
    mean_pitches = get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=False)
    assert mean_pitches == 1


def test_find_bar_duration_fourth():
    notes = [
        [0, 60],
        [0, 64],
        [1, 62],
        [2, 62],
        [3, 62],
        [4, 60],
        [4, 64],
        [5, 62],
        [6, 62],
        [7, 62],
    ]
    notes = np.asarray(notes)

    bar_duration, offset = find_bar_duration(notes, weights=False)

    assert bar_duration == 4
    assert offset == 0


def test_find_bar_duration_fourth_offset():
    notes = [
        [0, 60],
        [0, 64],
        [1, 62],
        [2, 62],
        [3, 62],
        [4, 60],
        [4, 64],
        [5, 62],
        [6, 62],
        [7, 62],
    ]
    notes = np.asarray(notes, dtype=float)
    notes[:, 0] += 0.5
    bar_duration, offset = find_bar_duration(notes, weights=False)

    assert bar_duration == 4
    assert offset == 0.5


def test_find_bar_duration_fourth_other_offset():
    notes = [
        [0, 60],
        [0, 64],
        [1, 62],
        [2, 62],
        [3, 62],
        [4, 60],
        [4, 64],
        [5, 62],
        [6, 62],
        [7, 62],
    ]
    notes = np.asarray(notes, dtype=float)
    notes[:, 0] -= 0.5
    bar_duration, offset = find_bar_duration(notes, weights=False)

    assert bar_duration == 4
    assert offset == -0.5


def test_find_bar_duration_three():
    notes = [
        [0, 60],
        [0, 64],
        [1, 62],
        [2, 62],
        [3, 60],
        [3, 64],
        [5, 62],
        [6, 62],
        [6, 62],
    ]
    notes = np.asarray(notes, dtype=float)
    bar_duration, offset = find_bar_duration(notes, weights=False)

    assert bar_duration == 3
    assert offset == 0

def test_find_bar_duration_three():
    notes = [
        [0, 60],
        [0, 64],
        [1, 62],
        [2, 62],
        [3, 60],
        [3, 64],
        [5, 62],
        [6, 62],
        [6, 62],
    ]
    notes = np.asarray(notes, dtype=float)
    notes[:, 0] -= 0.5
    bar_duration, offset = find_bar_duration(notes, weights=False)
    assert bar_duration == 3
    assert offset == -0.5