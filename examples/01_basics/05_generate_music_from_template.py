"""
5. Generate music from a template
=================================

/!\ You need to install musiclang-predict library to run this example !
```
pip install musiclang-predict
```

We use the capabilities of analysis of MusicLang to generate music from a template
It will predict new music from the same chord progression, instrumentation and other musical features as note density
velocities and pitch range for all instruments.

We use the 4 first chords of a midi file
"""
# Predict a song

from musiclang_predict import midi_file_to_template, predict_with_template, MusicLangTokenizer
from transformers import GPT2LMHeadModel

# Load model and tokenizer
model = GPT2LMHeadModel.from_pretrained('musiclang/musiclang-4k')
tokenizer = MusicLangTokenizer('musiclang/musiclang-4k')

template = midi_file_to_template('template.mid', chord_range=(0, 4)) # Put your midi template here
soundtrack = predict_with_template(template, model, tokenizer)
soundtrack.to_midi('song.mid', tempo=template['tempo'], time_signature=template['time_signature'])