from musiclang import Metric
from musiclang.library import *
import pytest

def test_basic_metric_instantiation_ok():

    metric = Metric([1, 0, 0, 0], signature=(4, 4), tatum=1)
    assert metric.tatum == 1
    assert metric.signature == (4, 4)
    assert metric.nb_bars == 1
    assert metric.array == [1, 0, 0, 0]



def test_error_if_array_does_not_match_duration_():

    with pytest.raises(ValueError):
        metric = Metric([1, 0, 0], signature=(4, 4), tatum=1)


def test_strong_beat_four_four_():

    metric = Metric([1, 0, 0, 0], signature=(4, 4), tatum=1)
    assert metric.beat_type(0) == Metric.STRONG
    assert metric.beat_type(1) == Metric.WEAK
    assert metric.beat_type(0.5) == Metric.SYNCOPATION


def test_apply_melody_with_expand():
    melody = s0
    metric = Metric([1, 0, 1, 0], signature=(4, 4), tatum=1)
    res = metric.apply_to_melody(melody, expand=True)
    assert res == s0.h + s0.h


def test_apply_melody_with_expand_two_notes():
    melody = s0 + s1.e
    metric = Metric([1, 0, 1, 0], signature=(4, 4), tatum=1)
    res = metric.apply_to_melody(melody, expand=True)
    assert res == s0.h + s1.h


def test_apply_melody_without_expand():

    melody = s0
    metric = Metric([1, 0, 1, 0], signature=(4, 4), tatum=1)
    res = metric.apply_to_melody(melody, expand=False)
    assert res == s0.h + r.h


def test_canon():
    metric = Metric([1, 0, 1, 0], signature=(4, 4), tatum=1)
    canon = metric.canon(2)
    assert canon.array == [0, 0, 1, 0]

def test_circular_shift():
    metric = Metric([1, 0, 1, 0], signature=(4, 4), tatum=1)
    canon = metric.circular_shift(2)
    assert canon.array == [1, 0, 1, 0]