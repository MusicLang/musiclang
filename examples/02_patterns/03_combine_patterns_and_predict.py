"""
2.2. Insert counterpoint into a simple idea
===========================================


"""

from musiclang_predict import predict_with_template, MusicLangTokenizer, score_to_template
from transformers import GPT2LMHeadModel
from musiclang.library import *
from musiclang import Score

# Load model and tokenizer
model = GPT2LMHeadModel.from_pretrained('musiclang/musiclang-4k')
tokenizer = MusicLangTokenizer('musiclang/musiclang-4k')

n_bars_pattern = 2  # Number of bars of the pattern we want to generate

# Define the prompt of your idea here, the model will generate an idea that "look" like this (in terms of density, instruments and ranges)

original_idea = (I % I.M)(
                          contrabass__0=(s0 + s2 + s4 + s2).o(-2),
                          viola__0=(s0 + s2 + s4 + s2).o(-1),
                          oboe__0=(s0 + s2 + h3 + s2 + s4 + h6 + s4.h).e
) * n_bars_pattern

# Let's predict an idea that looks like the prompt with MusicLang language model
template = score_to_template(original_idea)
generated_idea = predict_with_template(template, model, tokenizer, temperature=1.0)

# We need to transform our generated idea into a one chord pattern (that lasts n_bars_pattern)
generated_idea = generated_idea.project_on_one_chord()

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
