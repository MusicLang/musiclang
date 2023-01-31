from musiclang.transform import Mask
from musiclang.library import *


def test_mask_chord():
    """
    Mask.Chord() returns false if the object is not a chord
    Otherwise returns true
    """
    mask = Mask.Chord()
    assert not mask((I % I.M))
    assert mask(s0)


def test_mask_melody():
    """
    Mask.Melody() returns false if the object is not a chord
    Otherwise returns true
    """
    mask = Mask.Melody()
    assert not mask(s0 + s1)
    assert mask(s0)
    assert mask(I % I.M)


def test_mask_note():
    """
    Mask.Note() returns false if the object is not a chord
    Otherwise returns true
    """
    mask = Mask.Note()
    assert not mask(s0)
    assert mask((I % I.M))


def test_mask_score():
    """
    Mask.Score() returns false if the object is not a chord
    Otherwise returns true
    """
    mask = Mask.Score()
    assert not mask((I % I.M)(piano=[s0, s2, s4]) + (I % I.M)(piano=[s0, s2, s4]))
    assert mask(s0)


def test_mask_gt_true():

    mask = Mask.Chord() > Mask.Has('ok')
    score = (I % I.M)().add_tag('ok')
    assert mask(score)


def test_mask_gt_false():

    mask = Mask.Chord() > Mask.Has('nok')
    score = (I % I.M)().add_tag('ok')
    assert not mask(score)

def test_mask_and_true():

    mask = Mask.Chord() > (Mask.Has('ok1') & Mask.Has('ok2'))
    score = (I % I.M)().add_tags(['ok1', 'ok2'])
    assert mask(score)

def test_mask_and_false():

    mask = Mask.Chord() > (Mask.Has('ok1') & Mask.Has('ok2'))
    score = (I % I.M)().add_tags(['ok1'])
    assert not mask(score)

def test_mask_or_true():

    mask = Mask.Chord() > (Mask.Has('ok1') | Mask.Has('ok2'))
    score = (I % I.M)().add_tags(['ok1'])
    assert mask(score)

def test_mask_or_false():

    mask = Mask.Chord() > (Mask.Has('ok1') | Mask.Has('ok2'))
    score = (I % I.M)().add_tags(['ok3'])
    assert not mask(score)

def test_mask_hasatleast_true():

    mask = Mask.Chord() > (Mask.HasAtLeast(['ok1', 'ok2' ]))
    score = (I % I.M)().add_tags(['ok1'])
    assert mask(score)

def test_mask_hasatleast_false():

    mask = Mask.Chord() > (Mask.HasAtLeast(['ok1', 'ok2' ]))
    score = (I % I.M)().add_tags(['ok3'])
    assert not mask(score)

def test_not_mask():

    mask = (Mask.Melody() > Mask.Has('ok'))

    melo = (s0 + s1)

    assert not mask(melo)
    assert (~mask)(melo)

def test_bool_mask():
    mask = (Mask.Melody() > Mask.Bool(True))
    melo = (s0 + s1)
    assert mask(melo)

def test_eval_mask():

    mask = Mask.Chord() > (Mask.HasAtLeast(['ok1', 'ok2']))

    repr = str(Mask.eval(str(mask)))