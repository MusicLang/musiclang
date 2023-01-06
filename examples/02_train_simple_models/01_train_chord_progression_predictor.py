import os
from musiclang.predict.predictors import WindowedPredictor, HierarchicalChordPredictor
from musiclang.predict.tokenizers import ChordTokenizer, ChordDetokenizer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

data_path = '../data/training_data'

"""
In this tutorial we will train our first machine learning model that will be able to predict the next chord of a song.
If you want to fully understand this example it is strongly advised to have some basic knowledge on machine learning
models and the scikit-learn python package. But we will try to go on each step slowly.

Our goal : 
Train a simple autoregressive model that will predict the next chord using a context window
To achieve that we will use the "WindowedPredictor" object of MusicLang. To be more precise the steps are the following:
- Tokenize our scores to extract only chord information on a given score using the ChordTokenizer
- Choose a machine learning model
- Train the model on our corpus
- Predict the next chords in a given progression
"""

# First instantiate our chord tokenizer
tokenizer = ChordTokenizer()

# Tokenize all our scores
print('Tokenize dataset ...')
data = tokenizer.tokenize_directory(data_path)

import lightgbm
print('Number of examples : ', str(len(data)))
print('Training ...')
clf = RandomForestClassifier(n_estimators=30, max_depth=None, n_jobs=1)
print(clf)
predictor = WindowedPredictor(clf, memory=3, vector_size=15, window=3)
import numpy as np
print(np.mean(predictor.cross_val_score(data, cv=2)))
#exit()
predictor.fit(data)
predictor.save('../data/chord_predictor.pickle')

from musiclang.write.library import *
chord_progression = (I % I.M) + (I['6'] % I.M) + (IV % I.M) + (VII['7'] % V.m)

# Tokenize the chord progression
tokens = tokenizer.tokenize(chord_progression)

# Predict next two chords
for i in range(10):
    predicted_token = predictor.predict(tokens)
    tokens.append(predicted_token)

# Convert tokens to a score
detokenizer = ChordDetokenizer()
score = detokenizer.detokenize(tokens)


print(tokens)
#score.to_voicings().show('midi')