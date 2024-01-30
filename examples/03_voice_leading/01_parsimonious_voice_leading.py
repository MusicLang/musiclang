"""
3.1 Parsimonious voice leading
===============================

In this example we will demonstrate some parsimonious voice leading capabilities of musiclang.
We are gonna arrange a chord progression to minimize the distance between the notes of the chords.
- We have as inputs a score of chord-scales (Chord degree inside a tonality)
- We apply the Score.get_parsimonious_voice_leading method to arrange each chord to minimize sequential movement.
It will modify the inversion of the chord-scale (eg : '', '6', '64') and the base octave of the chord-scale

"""

from musiclang.library import *
from musiclang import Score

# Suppose we have a simple chord progression

chord_progression_score = (I % I.M).h + (V % I.M).h + (IV % I.M).h + (I % I.M).h + (V % VI.m).h + (I % VI.m).h + (V % I.M).h + (I % I.M).h

# We can apply parsimonious voice leading to this chord progression

score = chord_progression_score.get_parsimonious_voice_leading()

# Display the chords
print('Chord sequence arranged with parsimonious voice leading :')
print(score.to_chords())

# Voice each chord with an open voicing using bass notes:

score = score(piano__0=b0.o(-1), piano__1=b2.o(-1), piano__2=b1)

score.to_midi('pattern.mid')