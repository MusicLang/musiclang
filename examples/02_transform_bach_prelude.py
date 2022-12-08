"""
In this example we will play a little bit with a score already written

We will try to change

As usual here is the sore : https://www.mutopiaproject.org/ftp/BachJS/BWV846/wtk1-prelude1/wtk1-prelude1-a4.pdf

To improve the readibility of this tutorial we will write it as a single melody
"""
from musiclang.core.library import *

"""
We will go quickly to write the first bars of the piece.
If you face difficulty to understand that part don't hesitate to return to the first tutorial (01_writing_alla_turca)
"""

melody_1 = (s0 + s2 + (s4 + s0.o(1) + s2.o(1)) * 2).s * 2
melody_2 = (s6.o(-1) + s0 + (s4 + s0.o(1) + s2.o(1)) * 2).s * 2
melody_3 = ((s2 + s4).o(-1) + (s0 + s4 + s6) * 2).s * 2
melody_4 = melody_1

melodies = [melody_1, melody_2, melody_3, melody_4]

# By default chords degrees will resolve in C-major so we don't have to specify it
chords = [I, II, V, I]

# Here we use a little trick to create the score from the list of chords and melodies
base_score = sum([chord(piano__0=melody) for chord, melody in zip(chords, melodies)], None)

"""
This is a good basis to extend it and transform it using standard technics
Let's repeat this chord progression three times with small modification each time :
- The first time plays it normally
- The second time change the progression to prepare a modulation to G major
- The third time plays it on G-major (the fifth degree of C)
- The fourth time plays it on C-minor
- Repeat it one last time in C major
"""

score_1 = base_score

chords_2 = [I, VI.o(-1), V % V.M.o(-1), V.o(-1)]  # You can specify the base octave of a chord or a tonality
score_2 = sum([chord(piano__0=melody) for chord, melody in zip(chords_2, melodies)], None)

score_3 = base_score % V.M.o(-1)  # Use the modulo operator to modulate a score into a new tonality relatively, here G-major

score_4 = base_score % I.m

score_5 = base_score

score = score_1 + score_2 + score_3 + score_4 + score_5

score.to_midi('bach_prelude.mid', tempo=90)

"""
That's it, in this tutorial we have introduced a method to develop a theme harmonically

"""