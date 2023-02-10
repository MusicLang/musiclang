"""
4. Predict New Music
====================

In this example we are gonna see how we can use the predict module to extends an already existing chord progression
- We will create a small chord progression
- We will use an already trained WindowedPredictor to predict the next three chords of our song

"""


from musiclang.predict.predictors import WindowedPredictor
from musiclang.predict.tokenizers import ChordTokenizer, ChordDetokenizer
from musiclang.write.library import *


tokenizer = ChordTokenizer()
print('loading model')
predictor = WindowedPredictor.load('../data/model.pickle')

chord_progression = (I % I.M) + (VI['6'] % I.M) + (II['2'] % I.M)
# Tokenize the chord progression
tokens = tokenizer.tokenize(chord_progression)

# Predict next two chords
for i in range(10):
    predicted_token = predictor.predict(tokens)
    tokens.append(predicted_token)

print(tokens)
# Convert tokens to a score
detokenizer = ChordDetokenizer()
score = detokenizer.detokenize(tokens)
print(score)
score.to_voicing().show('midi')

