from musiclang.library import *
from musiclang import Score
import numpy as np

def test_parsimonious_voice_leading_up():
    chord_progression = [
        (I % II.M).h,
        (V % II.M).h['6'].o(-1),
        (I % II.M).w,
        (I % II.M).w['6'],
        (I % II.M).h['64'],
        (I % II.M).h.o(1),
        (V % II.M).set_duration(8),
        (I % II.M).h.o(1),
        (I % II.M).q['64'],
        (I % II.M).q['6'],
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
    score = Score(chord_progression).get_parsimonious_voice_leading(directions='up')
    assert np.diff([c.bass_pitch for c in score.chords]).min() >= 0


def test_parsimonious_voice_leading_down():
    chord_progression = [
        (I % II.M).h,
        (V % II.M).h['6'].o(-1),
        (I % II.M).w,
        (I % II.M).w['6'],
        (I % II.M).h['64'],
        (I % II.M).h.o(1),
        (V % II.M).set_duration(8),
        (I % II.M).h.o(1),
        (I % II.M).q['64'],
        (I % II.M).q['6'],
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
    score = Score(chord_progression).get_parsimonious_voice_leading(directions='down')
    assert np.diff([c.bass_pitch for c in score.chords]).max() <= 0

def test_parsimonious_voice_leading():
    chord_progression = [
        (I % V.M).h,
        (V % V.M),
        ]
    score = Score(chord_progression).get_parsimonious_voice_leading()
    assert score == Score([(I % V.M).h, (V % V.M)['6'].o(-1)])