"""
5. Generate music from a chord progression
=================================

/!\ You need to install musiclang-predict library to run this example !
```
pip install musiclang-predict
```

We condition the model output on a chord progression
"""
# Predict a song

from musiclang_predict import MusicLangPredictor

nb_tokens = 1024
temperature = 0.9  # Don't go over 1.0, at your own risks !
top_p = 1.0 # <=1.0, Usually 1 best to get not too much repetitive music
seed = 16  # change here to change result, or set to 0 to unset seed
time_signature=(4, 4)

chord_progression = "Am CM Dm E7 Am" # 1 chord = 1 bar
ml = MusicLangPredictor('musiclang/musiclang-v2')
soundtrack = ml.predict_chords(
    chord_progression,
    time_signature=time_signature,
    temperature=temperature,
    topp=top_p,
    rng_seed=seed # set to 0 to unset seed
)

soundtrack.to_midi('song.mid', tempo=120, time_signature=time_signature)