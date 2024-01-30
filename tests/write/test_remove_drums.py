
from musiclang.library import *
from musiclang import Score

def test_get_drums():
    drums = (I % I.M)(s0, s1, drums_0=bd) + (I % I.M)(s0, s1) + (I % I.M)(s0, s1, drums_0=bd)
    only_drums = drums.get_instrument_names(['drums_0'])
    assert only_drums == (I % I.M)(drums_0=bd) + (I % I.M)(drums_0=r) + (I % I.M)(drums_0=bd)


def test_remove_drums():
    all_drums = (I % I.M)(s0, s1, drums_0=bd) + (I % I.M)(drums_0=bd) + (I % I.M)(s0, s1, drums_0=bd)
    drums_removed = all_drums.remove_drums()
    assert drums_removed == (I % I.M)(s0, s1) + (I % I.M)(piano__0=r, piano__1=r) + (I % I.M)(s0, s1)