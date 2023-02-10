from musiclang.transform.library import ReverseMelody
from musiclang.library import *

def test_reverse_melody_on_chord():

    reverser = ReverseMelody()
    score = (I % I.M)(s0 + s1 + s2)

    result = reverser(score)
    expected_score = (I % I.M)(s2 + s1 + s0)

    assert result == expected_score



def test_reverse_melody_on_score():

    reverser = ReverseMelody()
    score = (I % I.M)(s0 + s1 + s2) + (V % I.M)(violin__1=s0 + s1)

    result = reverser(score)
    expected_score = (I % I.M)(s2 + s1 + s0) + (V % I.M)(violin__1=s1 + s0)

    assert result == expected_score


def test_reverse_melody_on_melody():

    reverser = ReverseMelody()
    melody = s1 + s2.h + s3
    result = reverser(melody)
    expected_melody = s3 + s2.h + s1

    assert result == expected_melody