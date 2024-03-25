"""
2.3. Combine patterns and predict
==================================

In this example we are going to combine the previous examples to :
- generate a new idea with MusicLang language model
- extract a pattern from this idea
- Project the pattern on a chord progression
"""

from musiclang.library import *
from musiclang import Score
from musiclang_predict import MusicLangPredictor

temperature = 0.9  # Don't go over 1.0, at your own risks !
top_p = 1.0 # <=1.0, Usually 1 best to get not too much repetitive music
seed = 0  # change here to change result, or set to 0 to unset seed
time_signature=(4, 4)
ml = MusicLangPredictor('musiclang/musiclang-v2')
generated_idea = ml.predict(
    nb_chords=3,
    temperature=temperature,
    topp=top_p,
    rng_seed=seed # set to 0 to unset seed
)

# We need to transform our generated idea into a one chord pattern (that lasts n_bars_pattern)
generated_idea = generated_idea[-1:].project_on_one_chord()  # For example take last bar of the idea

# Apply the same process than in 01_pattern extraction

pattern = generated_idea.chords[0].to_pattern(drop_drums=False)
# Let project this pattern in an ascending chord progression with chord inversions :
# A musical chord progression is applied
chord_progression = [
        (I % II.M).h,
        (V % II.M).h['6'].o(-1),
        (I % II.M).w,
        (I % II.M).w['6'],
        (I % II.M).h['64'],
        (I % II.M).h.o(1),
        (V % II.M).set_duration(8),
        (I % II.M).h.o(1),
        (I % II.M).q['64'],
        (I % II.M).q['6'],
        (I % II.m).h,
        (V % II.mm).h['6'].o(-1),
        (I % II.m).w,
        (I % II.m).w['6'],
        (I % II.m).h['64'],
        (I % II.m).h.o(1),
        (V % II.mm)['7(sus4)'].set_duration(4),
        (V % II.mm)['7'].set_duration(4),
        (I % II.m).w.o(1),
        (V % IV.M).w,
        (IV % IV.M).w,
        (V % II.m)['7'].w
    ]

score = Score.from_pattern(pattern, chord_progression,
                           chord_rhythm=True)  # this forces the pattern to continue on chord change (instead of restarting)

score.to_midi('pattern.mid')
