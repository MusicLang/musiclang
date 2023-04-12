from musiclang.library import *

import pytest


def test_normalization_extension():
    chord = (I % I.M)['6{-5}[m3](sus2)[add6]']
    assert chord.extension == '6(sus2)[add6][m3]{-5}'


def test_without_additions_or_replacements():
    chord = (I % I.M)['6']
    assert chord.extension_notes == [s2, s4, s0.o(1)]

def test_unexisting_extension_lead_to_error():
    with pytest.raises(Exception):
        chord = (I % I.M)['22zrahj']

def test_replacement_without_candidate_lead_to_addition():
    chord = (I % I.M)['[#11]']
    assert chord.extension_notes == [s0, s2, s4, h6.o(1)]


def test_sus2_replacement():

    chord = (I % I.M)['(sus2)']
    assert chord.extension_notes == [s0, s1, s4]


def test_remove_fifth():
    chord = (I % I.M)['{-5}']
    assert chord.extension_notes == [s0, s2]


def test_remove_eleventh():
    chord = (I % I.M)['13{-11}[add4]']
    assert chord.extension == '13[add4]{-11}'
    assert chord.extension_notes == [s0, s2, s3, s4, s6, s1.o(1), s5.o(1)]


def test_add2():
    chord = (I % I.M)['[add2]']
    assert chord.extension_notes == [s0, s1, s2, s4]

def test_very_complicated_chord():
    chord = (I % I.M)['9[add2][#11](m3)']
    assert chord.extension_notes == [s0, s1, h3, s4, s6, s1.o(1), h6.o(1)]


def test_very_complicated_chord2():
    chord = (I % I.M)['2[add4][M6](M3)(+)']
    assert chord.extension_notes == [s6.o(-1), s0, h4, s3, h8, h9]

def test_replacement_become_addition():
    chord = (I % I.M)['(M7)']
    assert chord.extension_notes == [s0, s2, s4, h11]


def test_replace_b9():
    chord = (I % I.M)['9(m9)']
    assert chord.extension_notes == [s0, s2, s4, s6, h1.o(1)]


def test_addition_and_replacement():
    chord = (I % I.M)['(sus2)[add6]']
    assert chord.extension_notes == [s0, s1, s4, s5]



def test_addition_and_inversion():
    chord = (I % I.M)['6(sus2)']
    assert chord.extension_notes == [s1, s4, s0.o(1)]



def test_addition_and_inversion_with_octaves():
    chord = (I % I.M)['2(sus2)']
    assert chord.extension_notes == [s6.o(-1), s0, s1, s4]


def test_to_voicing():
    chord = (I % I.M)['(sus2)']
    chord = chord.to_voicing(nb_voices=3, instruments=['cello', 'piano', 'flute'])
    assert chord == (I % I.M)['(sus2)'](cello__0=s0, piano__0=s1, flute__0=s4)



def test_score_to_voicing():
    score = (I % I.M)['(sus2)'] + (V % I.M)['[add9](+)']
    score = score.to_voicing(nb_voices=4, instruments=['cello', 'piano', 'flute', 'piccolo'])
    ch1 = (I % I.M)['(sus2)'](cello__0=s0, piano__0=s1, flute__0=s4, piccolo__0=s0.o(1))
    ch2 = (V % I.M)['[add9](+)'](cello__0=s0, piano__0=s2, flute__0=h8, piccolo__0=s1.o(1))
    assert score == ch1 + ch2

def test_score_to_voicing_with_duration():
    score = (I % I.M)['(sus2)'].w + (V % I.M)['[add9](+)'].augment(frac(6, 1))
    score = score.to_voicing(nb_voices=4, instruments=['cello', 'piano', 'flute', 'piccolo'])
    ch1 = (I % I.M)['(sus2)'](cello__0=s0.w, piano__0=s1.w, flute__0=s4.w, piccolo__0=s0.o(1).w)
    ch2 = (V % I.M)['[add9](+)'](cello__0=s0.augment(frac(6, 1)), piano__0=s2.augment(frac(6, 1)), flute__0=h8.augment(frac(6, 1)), piccolo__0=s1.o(1).augment(frac(6, 1)))
    assert score == ch1 + ch2