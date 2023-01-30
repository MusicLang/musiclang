from musiclang.transform.composing import project_on_score_keep_notes
from musiclang.library import *

def test_project_on_score_keep_notes():


    score1 = (I % I.M)(s0 + s0)
    score2 = (I % I.M)(s4) + (IV % I.M)(s4)  # Whatever note, only the harmonic rythm counts here
    expected_score = (I % I.M)(s0) + (IV % I.M)(s4.o(-1))
    new_score = project_on_score_keep_notes(score1, score2)

    assert new_score == expected_score


def test_project_on_score_keep_notes_with_continuation():


    score1 = (I % I.M)(s0 + s0)
    score2 = (I % I.M)(s4.e) + (IV % I.M)(s4.qd)  # Whatever note, only the harmonic rythm counts here
    expected_score = (I % I.M)(s0.e) + (IV % I.M)(l.e + s4.o(-1))
    new_score = project_on_score_keep_notes(score1, score2)

    assert new_score == expected_score


def test_project_on_score_keep_notes_different_durations_keep_min_duration():

    score1 = (I % I.M)(s0 + s0)
    score2 = (I % I.M)(s4.e) + (IV % I.M)(s4.h)  # Whatever note, only the harmonic rythm counts here
    expected_score = (I % I.M)(s0.e) + (IV % I.M)(l.e + s4.o(-1))
    new_score = project_on_score_keep_notes(score1, score2)

    assert new_score == expected_score