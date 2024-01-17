

from musiclang import Score
from musiclang.library import *
import tempfile
def test_start_with_silence():

    # Test with a midi file that starts with silence (anachrusis)
    score = (I% I.M)(r + s0 + s2 + s4)  + (I % I.M)(s0 + s0 + s2 + s4)
    with tempfile.NamedTemporaryFile(suffix='.mid') as f:
        output_path = f.name
        score.to_midi(output_path, time_signature=(4, 4))

        # Reload with musiclang
        score = Score.from_midi(output_path, tokenize_before=True)
        assert score[0].score['piano__0'] == r + s0 + s2 + s4
        assert score[1].score['piano__0'] == s0 + s0 + s2 + s4