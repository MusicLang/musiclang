from musiclang.transform.composing import create_counterpoint, create_counterpoint_on_score
from musiclang.library import *

def test_create_counterpoint():
    melody1 = s0 + s1 + s2
    melody2 = s0 + s1 + s2  # Parallel unissons, should be resolved

    melody2_corrected = create_counterpoint([melody1], [melody2])

    assert melody2_corrected[0] != s0 + s1 + s2