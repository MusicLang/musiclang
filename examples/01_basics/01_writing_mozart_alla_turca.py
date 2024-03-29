"""
1. Writing Mozart "Alla turca"
==============================

In this short example we will write the first four bars of Mozart rondo alla turca with MusicLang.
It will show you the basic of writing a simple score with MusicLang

You can find the sheet music in pdf here if you want to follow with the score :
https://www.mutopiaproject.org/ftp/MozartWA/KV331/KV331_3_RondoAllaTurca/KV331_3_RondoAllaTurca-a4.pdf

"""

# We import the musiclang library
from musiclang.write.library import *

"""
First we have to choose the tonality of our piece
For Mozart Rondo Alla Turca, it is in A minor
"""
Am = TONALITY_A.m

"""
If we look at the four first bars we see that the accompaniment is playing an A minor chord.
It is also the first degree of our tonality, so we can write :
"""
chord_1 = I % Am

"""
This chord will be use later to give contexts to what we are currently writing.
Now let's write the melody.

In MusicLang we specify everything relatively to a chord and a tonality. We will call it a "chord scale".
A melody has no concrete interpretation until it is played in the context of a chord. 

We derived two kind of symbols to write these melodies :
- scale notes s0, s1, s2, s3, s4, s5, s6, s7 which corresponds to the seven notes of a chord scale (0-indexed)
- chromatic notes h0, ..., h11 which corresponds to the twelve notes of a chromatic scales starting at the root of a chord

The chromatic notes are usually used to write accidents (notes that do not belong to the chord scale)

By default the minor mode (notated m) is the harmonic minor mode
So the chord scales notes of the first degree will be A,B,C,D,E,F,G#
"""
# Melody starts with an anachrusis which is also the main pattern of the score
melody_1 = (s1 + s0 + s6.o(-1) + s0).s

"""
We have to discuss two things here : 

- We used 's' to say it is a sixteenth note, by default it is a quarter
    You can use any duration (w, h, q, e, s, t) 
    which respectively refers to whole, half, quarter, eight, sixteenth, thirty-seconds
        - You can also use dots (eg: qd for writing a dotted quarter note).
        - You can write n-uplets (eg: e3 for a triolet)
        - You can specify a custom duration using note.augment(fraction) method

- We use the 'o' symbol to transpose one octave down the s6 note (the G# in our context)

Ok, now we proceed to write the melodies of the other bars which are somehow derived from this pattern :
"""

# We use the '&' symbol to transpose a melody diatonically (here by two steps)
# We use the 'r' to mark the silence (rest)
melody_2 = s2.e + r.e + (melody_1 & 2)

# We can replace a pitch to write the D# in the 3rd bar
# It will only affect the pitch itself, not the duration or any other property
melody_3 = (melody_2 & 2).replace_pitch(s3, h6)

# If we want to repeat a note or a melody sequentially we can use the * operator
melody_4 = (melody_1 * 2).o(1)

"""
Now we need to transcribe the left hand pattern. 
MusicLang only understand voices that play one note at a time
so the standard pattern to write multi notes voices is to split it into several voices as a dict of voices.

We use a convention to name the voices : <instrument>__<idx of voice> (0-indexed, note the double __)
The instrument will be parsed and used automatically if it belongs to the standard GM-midi instrument (lower case with _
to mark spaces).
We will use piano__0 for the melody, so let's use piano__1, piano__2, piano__3 to write the left hand :

"""

accompaniment = {
    'piano__1': (s0.o(-1).e + r.qd).p,  # We can use r to mark a silence (rest)
    'piano__2': (r.e + s2.e * 3).o(-1).p,
    'piano__3': (r.e + s4.e * 3).o(-1).p
}
accompaniment_2 = {
    'piano__1': (s0.e + r.e + s0.e + r.e).o(-1),
    'piano__2': (r.e + s2.e + r.e + s2.e).o(-1),
    'piano__3': (r.e + s4.e + r.e + s4.e).o(-1)
}

accompaniment_end = {
    'piano__1': s0.e.o(-1),
    'piano__2': s2.e.o(-1),
    'piano__3': s4.e.o(-1)
}

"""
Well, now we have everything to write the first four bars
We now have to apply our melodies in the context of a chord scale.
It works by calling the chord with named arguments corresponding to the voices used
"""

score = chord_1(piano__0=melody_1) + \
        chord_1(piano__0=melody_2, **accompaniment) + \
        chord_1(piano__0=melody_3, **accompaniment) + \
        chord_1(piano__0=melody_4, **accompaniment_2) + \
        chord_1(piano__0=s2.e.o(1), **accompaniment_end)  # Just to end the phrase

"""
Now you can enjoy the first four bars of mozart in midi format, let's save it !

I encourage you to try playing a little with the score created. Why not changing the tonality,
the melody, the chords or even the instruments ? You will see that the whole point of this library is its modularity.
"""
score.to_midi('test.mid')
