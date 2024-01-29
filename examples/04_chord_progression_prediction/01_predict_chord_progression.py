"""
4.1 Predict chord progressions
===============================

/!\ You need to install musiclang_predict to run this example. (pip install musiclang-predict

In this example we will demonstrate how to predict chord progressions from a transformer model.

"""

from musiclang.library import *
from musiclang_predict import MusicLangTokenizer
from musiclang import Score


from transformers import AutoTokenizer, AutoModelForCausalLM
from musiclang_predict import predict_chords

# Load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained("musiclang/musiclang-chord-v2-4k")
model = AutoModelForCausalLM.from_pretrained("musiclang/musiclang-chord-v2-4k")


# We can predict a chord progression from a score prompt, here a simple i i6 to be continued
prompt = (I %I.m) + (I % I.m)['6']
score = predict_chords(model, tokenizer, nb_chords=32, temperature=1.0, prompt=prompt)

# Create a simple voicing from the predicted chord progression and save it
score2 = score(b0.o(-2), b0.o(-1), b2, b1.o(1), b3.o(1))
score2.to_midi('result_basic.mid')

# Create a simple bass score
bass_score = score(cello=b0.o(-1).h).to_scale_note()

# Create a simple pattern score with parsimonious voice leading on the chord progression
chord_progression_score = score(french_horn=b2.q + l.e + su1.e,
                                violin=b1.o(1).q + r,
                                flute=b3.o(1).e + bd1.e + bu1.e + l.e)
score2 = chord_progression_score.get_parsimonious_voice_leading()  # See example 3.1 for more details

# Add bass score that respects roman numeral progression
score2 = bass_score.project_on_score(score2, keep_pitch=True, voice_leading=False, keep_score=True)

# If you want add a little counterpoint to avoid potential parallel fifths and octaves
#score2 = score2.get_counterpoint(['cello__0'])

score2.to_midi('result_with_pattern.mid', tempo=100)