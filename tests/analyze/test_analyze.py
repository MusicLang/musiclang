from musiclang import Score
from musiclang.library import *
import os

import pytest

@pytest.mark.filterwarnings("ignore")
@pytest.mark.skip()
def test_read_file():

    filename = os.path.join(os.path.dirname(__file__), '../../examples/data/moonlight.mid')
    score = Score.from_midi(filename)

    assert score.chords[0].to_chord() == (I % II.b.m)
