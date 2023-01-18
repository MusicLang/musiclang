from musiclang.transform import TransformPipeline, ConcatPipeline, NoteTransformer
from musiclang.library import *
from musiclang.transform import Mask


class Transpose(NoteTransformer):

    def __init__(self, n):
        self.n = n

    def action(self, note, chord=None, instrument=None, **kwargs):

        return note & self.n

def test_transform_pipeline_without_mask():
    transposer = Transpose(2)
    pipeline = TransformPipeline([(
        'transpose', transposer
    )])

    score = (I % I.M)(piano=[s0, s2, s4]) + (V % I.M)(piano=[s0, s2, s4])
    expected_result = (I % I.M)(piano=[s2, s4, s6]) + (V % I.M)(piano=[s2, s4, s6])
    new_score = pipeline(score)
    assert new_score == expected_result

def test_transform_pipeline_without_mask_several():
    transposer = Transpose(2)
    pipeline = TransformPipeline([
        ('transpose', transposer),
        ('transpose', transposer),
    ])

    score = (I % I.M)(piano=[s0, s2, s4]) + (V % I.M)(piano=[s0, s2, s4])
    expected_result = score & 4
    new_score = pipeline(score)
    assert new_score == expected_result

def test_transform_pipeline_with_mask():
    transposer = Transpose(2)
    mask = Mask.Chord() > Mask.Has('ok')

    pipeline = TransformPipeline([(
        'transpose', transposer, mask
    )])

    score = (I % I.M)(piano=[s0, s2, s4]).add_tag('ok') + (V % I.M)(piano=[s0, s2, s4])
    expected_result = (I % I.M)(piano=[s2, s4, s6]) + (V % I.M)(piano=[s0, s2, s4])
    new_score = pipeline(score)
    assert new_score == expected_result


def test_concat_pipeline_without_mask():
    transposer = Transpose(2)
    pipeline = ConcatPipeline([
        ('transpose', transposer),
        ('transpose', transposer),
    ])

    score = (I % I.M)(piano=[s0, s2, s4]) + (V % I.M)(piano=[s0, s2, s4])
    expected_result = score + (score & 2) + ((score & 2) + (score & 4))
    new_score = pipeline(score)
    assert new_score == expected_result


def test_concat_pipeline_without_mask_several():
    transposer = Transpose(2)
    pipeline = ConcatPipeline([(
        'transpose', transposer
    )])

    score = (I % I.M)(piano=[s0, s2, s4]) + (V % I.M)(piano=[s0, s2, s4])
    expected_result = score + (I % I.M)(piano=[s2, s4, s6]) + (V % I.M)(piano=[s2, s4, s6])
    new_score = pipeline(score)
    assert new_score == expected_result


def test_concat_pipeline_with_mask():
    transposer = Transpose(2)
    mask = Mask.Chord() > Mask.Has('ok')

    pipeline = ConcatPipeline([(
        'transpose', transposer, mask
    )])

    score = (I % I.M)(piano=[s0, s2, s4]).add_tag('ok') + (V % I.M)(piano=[s0, s2, s4])
    expected_result = score + (I % I.M)(piano=[s2, s4, s6]) + (V % I.M)(piano=[s0, s2, s4])
    new_score = pipeline(score)
    assert new_score == expected_result
