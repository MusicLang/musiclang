"""
4. Predict New Music
====================

/!\ You need to install musiclang-predict library to run this example !
```
pip install musiclang-predict
```

In this example we will see how we can use MusicLang foundation LM model to predict four bars of music

"""
# Predict a song

from musiclang_predict import predict, MusicLangTokenizer
from transformers import GPT2LMHeadModel

model = GPT2LMHeadModel.from_pretrained('musiclang/musiclang-4k')
tokenizer = MusicLangTokenizer('musiclang/musiclang-4k')

# Predict a 8 bar song in 4/4 time signature with this model
soundtrack = predict(model, tokenizer, chord_duration=4, nb_chords=4)
soundtrack.to_midi('song.mid', tempo=120, time_signature=(4, 4))