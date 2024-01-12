
from musiclang.library import *
from musiclang import Score


def test_to_pattern():
    # 1. Create the base score (See previous example)
    flute_melody = (s0 + s2 + s4 + s3 + s4 + s3 + s2 + s4).e  # We will need it later

    chord = (I % I.M)(
        harpsichord__0=(s0 + s2 + s4 + s2).o(-1),
        flute__0=flute_melody,
    )
    pattern = chord.to_pattern()

    assert pattern[0]['pattern'] == (x0 + bu1 + bu1 + bd1)
    assert pattern[0]['instrument'] == 'harpsichord'
    assert pattern[0]['note'] == 'lowest_note'