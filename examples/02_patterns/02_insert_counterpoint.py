"""
2.2. Insert counterpoint into a simple idea
===========================================

In this example we will demonstrate some counterpoint capabilities of musiclang.
We will use the example generated in the previous example and add a counterpoint to the flute voice.
For that we will use the flute voice delayed by one beat and transposed down by a fourth and assign it to the harpsichord.
We will then apply counterpoint correction to the counterpoint to make it more musical.
"""

from musiclang.library import *
from musiclang import Score

# 1. Create the base score (See previous example)
flute_melody = (s0 + s2 + s4 + s3 + s4 + s3 + s2 + s4).e  # We will need it later

chord = (I % I.M)(
    harpsichord__0=(s0 + s2 + s4 + s2).o(-1),
    flute__0=flute_melody,
)
pattern = chord.to_pattern()
# Let project this pattern in an ascending chord progression with chord inversions :
# A minor chord progression this time
chord_progression = [
        (I % II.m).h,
        (V % II.mm).h['6'].o(-1),
        (I % II.m).w,
        (I % II.m).w['6'],
        (I % II.m).h['64'],
        (I % II.m).h.o(1),
        (V % II.mm)['7(sus4)'].set_duration(4),
        (V % II.mm)['7'].set_duration(4),
        (I % II.m).w.o(1),
        (V % IV.M).w,
        (IV % IV.M).w,
        (V % II.m)['7'].w
    ]

score = Score.from_pattern(pattern, chord_progression,
                           chord_rhythm=True)  # this forces the pattern to continue on chord change (instead of restarting)


# 2. Create the counterpoint in another harpsichord voice

counterpoint_melody = flute_melody & -2 # Transpose down by a fourth and double the durations

# We delay by one beat, we repeat the pattern as long as the chord progression
chord_progression_duration = int(sum([chord.duration for chord in chord_progression]))
counterpoint = (I%I.M)(harpsichord__1=r.h) + (I % I.M)(harpsichord__1=counterpoint_melody) * chord_progression_duration

# 3. Insert the counterpoint into the base score
score = counterpoint.project_on_score(score, voice_leading=True, keep_score=True)

# 4. Get a more musical counterpoint
score = score.get_counterpoint(fixed_parts=['harpsichord__0', 'flute__0']) # We fix the harpsichord and flute voices

score.to_midi('pattern.mid', tempo=120, time_signature=(4, 4))