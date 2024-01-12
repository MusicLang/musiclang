"""
2.1 Extract a pattern from a chord
=================================

We use the capabilities of analysis of MusicLang to apply a musical template to a chord progression.
We will here define a simple two voices pattern that will be moved in a chord scale progression with inversions.
This feature of musiclang allows to create complex sequences from a simple idea.
"""

from musiclang.library import *
from musiclang import Score

# Suppose we have a simple chord lasting four beats with a simple two voices pattern :

chord = (I % I.M)(
    harpsichord__0=(s0 + s2 + s4 + s0).o(-1),
    flute__0=(s0 + s2 + s4 + s3 + s4 + s3 + s2 + s4).e,
)


# We can extract a pattern from this chord with the method `to_orchestra` :
pattern = chord.to_pattern()

# Let project this pattern in an ascending chord progression with chord inversions :
# The chord progression in D : I V6 I I6 I64 I V with a specific rhythm
chord_progression = [
        (I % II.M).h,
        (V % II.M).h['6'].o(-1),
        (I % II.M).w,
        (I % II.M).w['6'],
        (I % II.M).h['64'],
        (I % II.M).h.o(1),
        (V % II.M).set_duration(8)
    ]

score = Score.from_pattern(pattern, chord_progression,
                           chord_rhythm=True)  # this forces the pattern to continue on chord change (instead of restarting)

score.to_midi('pattern.mid', tempo=120, time_signature=(4, 4))