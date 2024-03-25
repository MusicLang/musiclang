"""
4. Predict New Music
====================

Warning :  You need to install musiclang-predict library to run this example !
```
pip install musiclang-predict
```

In this example we will see how we can use MusicLang foundation LM model to predict four bars of music

"""
# Predict a song
from musiclang_predict import MusicLangPredictor

nb_tokens = 1024
temperature = 0.9  # Don't go over 1.0, at your own risks !
top_p = 1.0 # <=1.0, Usually 1 best to get not too much repetitive music
seed = 16  # change here to change result, or set to 0 to unset seed

ml = MusicLangPredictor('musiclang/musiclang-v2')
soundtrack = ml.predict(
    nb_chords=4,
    temperature=temperature,
    topp=top_p,
    rng_seed=seed # change here to change result, or set to 0 to unset seed
)

# Predict a 8 bar song in 4/4 time signature with this model
soundtrack.to_midi('song.mid', tempo=120)