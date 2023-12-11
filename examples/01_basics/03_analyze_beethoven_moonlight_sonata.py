"""
3. Analyze Beethoven Moonlight Sonata
=====================================

In this tutorial we will read an existing midi file and let MusicLang perform an automatic transcription
We will then look to this transcription
"""
from musiclang import Score

score = Score.from_midi('../data/moonlight.mid')  # Insert your favourite midi file here
# Display the first four chords
print('MusicLang score :')
print(score[:4])

# Save the score as valid musiclang language in a text file
print('Saving it to code in "beethoven_musiclang.py" ...')
score.to_text_file('beethoven.txt')

# Save the score in pickle to reuse it later
score.to_pickle('beethoven.pickle')

"""
Save it to midi
"""

score.to_midi('beethoven.mid', tempo=score.config['tempo'])
