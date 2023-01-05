"""
In this tutorial we will read an existing midi file and let MusicLang perform an automatic transcription
We will then explore this transcription
"""
from musiclang import Score

score = Score.from_midi('../data/moonlight.mid')  # Insert your favourite midi file here
# Display the first four chords
print('MusicLang score :')
print(score[:4])

# Display the analysis
print('Roman analysis : ')
print(score.config['annotation'])

# Convert the score as valid musiclang python code
print('Saving it to code in "beethoven_musiclang.py" ...')
score.to_code_file('beethoven_musiclang.py')

# Save the score in pickle to reuse it later
score.to_pickle('beethoven.pickle')


"""
Convert it to a pandas dataframe to do some analytics (we called it a "sequence" in musiclang) ...
"""
df = score.to_sequence()


# For example compute the value counts of tonalities mode
print('Value counts of tonalities mode per chord : ')
print(df.groupby('chord_idx').first()['tonality_mode'].value_counts())

"""
We can also transform our sequence, let's change all the modes to be major :
"""

df['tonality_mode'] = 'M'

"""
Finally let's convert it back to a score to hear it
"""
from musiclang import Score
score_result = Score.from_sequence(df)

score_result.show('midi', tempo=score.config['tempo'])
