"""
In this tutorial we will read an existing midi file and let MusicLang perform an automatic transcription
We will then explore this transcription
"""
from musiclang import Score

score = Score.from_midi('data/moonlight.mid')  # Insert your favourite midi file here

# Display the first four chords
print('MusicLang score :')
print(score[:4])

# Display the analysis
print('Roman analysis : ')
print(score.config['annotation'])

# Convert the score as valid musiclang python code
print('Saving it to code in "beethoven_musiclang.py" :')
score.to_code_file('beethoven_musiclang.py')

# Save the score in pickle to reuse it later
score.to_pickle('beethoven.pickle')


"""
Convert it to dataframe to do some analytics ...
"""

df = score.to_sequence()

# Pitch repartition

#df['pitch']


"""
Do some simple transformations on the dataframe and save it back to 
"""

df['tonality_mode'] = 'M'

"""
Now we have put every tonality in the piece in major mode, save it to midi to hear it
"""

from musiclang import Score

score_result = Score.from_sequence(df)

score_result.to_midi('moonlight_in_major_mode.mid', tempo=score.config['tempo'])
