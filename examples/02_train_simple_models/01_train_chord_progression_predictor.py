"""
1. Train a model to predict the next chord of a chord progression
=================================================================

In this tutorial we will train our first machine learning model that will be able to predict the next chord of a song.
If you want to fully understand this example it is strongly advised to have some basic knowledge on machine learning
models and the scikit-learn python package. But we will try to go on each step slowly.

This classifier uses a simple autoregressive model that will predict the next chord using a context window
To achieve that we will use the "WindowedPredictor" object of MusicLang. To be more precise the steps are the following:
- Tokenize our scores to extract only chord information on a given score using the ChordTokenizer
- Choose a machine learning model
- Train the autoregressive model on our corpus
- Predict the next chords in a given progression
"""

import numpy as np
from musiclang.write.library import *
from musiclang.predict.predictors import WindowedPredictor
from musiclang.predict.tokenizers import ChordTokenizer, ChordDetokenizer
from sklearn.ensemble import RandomForestClassifier

train_data_path = '../data/train_data'
test_data_path = '../data/test_data'

print('Tokenize training and testing set ...')
tokenizer = ChordTokenizer()
train_data = tokenizer.tokenize_directory(train_data_path)
test_data = tokenizer.tokenize_directory(test_data_path)
print('Number of examples : ', str(len(train_data)))
clf = RandomForestClassifier(n_estimators=20, max_depth=None, n_jobs=1)
predictor = WindowedPredictor(clf, memory=3, vector_size=5, window=3)
print('Training the model ...')
predictor.fit(train_data)

print('Evaluating on test data')
print('Accuracy : ', predictor.eval(test_data))
print('Saving the model ..')
predictor.save('../data/chord_predictor.pickle')

print('Create and tokenize a chord progression ...')
chord_progression = (I % I.M) + (I['6'] % I.M) + (IV % I.M) + (VII['7'] % V.m)
tokens = tokenizer.tokenize(chord_progression)

# Predict next five chords of the progression
for i in range(5):
    predicted_token = predictor.predict(tokens)
    tokens.append(predicted_token)

# Convert tokens to a score
detokenizer = ChordDetokenizer()
score = detokenizer.detokenize(tokens)

print('Resulting score (Chord progression + predicted chords) : ')
print(score)
