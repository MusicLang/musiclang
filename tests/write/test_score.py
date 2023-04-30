from musiclang.write.library import *



def test_score_equals():
    score1 = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    score2 = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    assert score1 == score2

def test_score_not_equals():
    score1 = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    score2 = I(piano__0=s0 + s1 + s1, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    assert score1 != score2

def test_score_equals_invert_order():
    score1 = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    score2 = I(violin__0=s0 + s1 + s4, piano__0=s0 + s1 + s2) + II(piano__0=s1 + s2)
    assert score1 == score2

def test_get_score_between():
    score = I(piano__0=s0 + s1 + s2) + II(piano__0=s1 + s2)
    subscore = score.get_score_between(start=1, end=4)
    expected_result = I(piano__0=s1 + s2) + II(piano__0=s1)
    assert subscore == expected_result


def test_complex_simple_score_between():
    score = I(piano__0=s0 + s1 + s2) + II(piano__0=s1 + s2)
    subscore = score.get_score_between(start=0, end=6)
    expected_result = score
    assert subscore == expected_result

def test_complex_out_of_bound_score_between():
    score = I(piano__0=s0 + s1 + s2) + II(piano__0=s1 + s2)
    subscore = score.get_score_between(start=0, end=7)
    expected_result = score
    assert subscore == expected_result

def test_complex_out_of_bound_and_complex_score_between():
    score = I(piano__0=s0 + s1 + s2) + II(piano__0=s1 + s2)
    subscore = score.get_score_between(start=1, end=7)
    expected_result =  I(piano__0=s1 + s2) + II(piano__0=s1 + s2)
    assert subscore == expected_result


def test_multi_instrument_complex_score_between():
    score = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    subscore = score.get_score_between(start=1, end=4)
    expected_result =  I(piano__0=s1 + s2, violin__0=s1 + s4) + II(piano__0=s1)
    assert subscore == expected_result

def test_multi_instrument_2_score_between():
    score = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    subscore = score.get_score_between(start=0, end=3)
    expected_result =  I(piano__0=s0 +s1 + s2, violin__0=s0 + s1 + s4)
    assert subscore == expected_result

def test_multi_instrument_3_score_between():
    score = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    subscore = score.get_score_between(start=3, end=6)
    expected_result =  II(piano__0=s1 + s2)
    assert subscore == expected_result


def test_multi_instrument_1_2_quarters_score_between():
    score = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)
    subscore = score.get_score_between(start=1, end=2)
    expected_result =  I(piano__0=s1, violin__0=s1)
    assert subscore == expected_result

def test_octaver():

    score = I(piano__0=s0 + s1 + s2, violin__0=s0 + s1 + s4) + II(piano__0=s1 + s2)

    score2 = score.octaver(piano__0=-1, violin__0=1)
    expected = I(piano__0=(s0 + s1 + s2).o(-1), violin__0=(s0 + s1 + s4).o(1)) + II(piano__0=(s1 + s2).o(-1))
    assert score2 == expected

def test_normalize_instruments():

    score = (I % I.M)(piano__0=s0.h) + (V % V.M)(piano__0=s1 + s2, violin__1=s3 + s1)
    expected_score = (I % I.M)(piano__0=s0.h, violin__1=r.h) + (V % V.M)(piano__0=s1 + s2, violin__1=s3 + s1)
    assert score.normalize_instruments() == expected_score

def test_remove_silenced_instruments():

    score = (I % I.M)(piano__0=s0.h, violin__1=r + r) + (V % V.M)(piano__0=s1 + s2, violin__1=s3 + s1)
    expected_score = (I % I.M)(piano__0=s0.h) + (V % V.M)(piano__0=s1 + s2, violin__1=s3 + s1)
    assert score.remove_silenced_instruments() == expected_score


def test_project_pattern_voicing():
    from musiclang import Score

    pattern = (I % I.M)(x0 + su1 + su2 + su1, x1.e + bu1.e + bd1 + bu1 + bd1)
    voicing = [b0, b1]
    expected_result = (I % I.M)(piano__0=b0 + su1 + su2 + su1, piano__1=b1.e + bu1.e + bd1 + bu1 + bd1)
    # By voicing
    result_voicing = pattern.project_pattern(voicing)
    assert expected_result == result_voicing

def test_project_pattern_score_restart():
    # By Score
    pattern = (I % I.M)(x0 + su1 + su2 + su1, x1.e + bu1.e + bd1 + bu1 + bd1)
    expected_result = ((I % II.M)(
	piano__0=b0 + su1,
	piano__1=b1.e + bu1.e + bd1)+
    (II % II.M)(
	piano__0=b0 + su1,
	piano__1=b1.e + bu1.e + bd1))

    score_voicing = (I % II.M)(b0.h, b1.h) + (II % II.M)(b0.h, b1.h)

    result_score = pattern.project_pattern(score_voicing, restart_each_chord=True)
    assert expected_result == result_score


def test_project_pattern_score_no_restart():
    # By Score
    pattern = (I % I.M)(x0 + su1 + su2 + su1, x1.e + bu1.e + bd1 + bu1 + bd1)
    expected_result = ((I % II.M)(
	piano__0=b0 + su1,
	piano__1=b1.e + bu1.e + bd1)+
(II % II.M)(
	piano__0=su2 + su1,
	piano__1=bu1 + bd1))

    score_voicing = (I % II.M)(b0.h, b1.h) + (II % II.M)(b0.h, b1.h)

    result_score = pattern.project_pattern(score_voicing, restart_each_chord=False)
    assert expected_result == result_score


def test_project_pattern_score_repeat_if_necessary():
    # By Score
    pattern = (I % I.M)(x0 + su1, x1.e + bu1.e + bd1)
    expected_result = ((I % II.M)(
	piano__0=b0 + su1 + b0 + su1,
	piano__1=b1.e + bu1.e + bd1 + b1.e + bu1.e + bd1))

    score_voicing = (I % II.M)(b0.w, b1.w)

    result_score = pattern.project_pattern(score_voicing, restart_each_chord=False)
    assert expected_result == result_score

from musiclang.library import *

def test_split_too_long_chords():
    score = None + (I %V.M)(s0.augment(7) + s1.augment(2), s4.augment(9))

    splitted_score = score.split_too_long_chords(8)

    print(splitted_score)

    expected_score = (
    (I % V.M)(
        piano__0=s0.augment(frac(7, 1)) + s1,
        piano__1=s4.augment(frac(8, 1)))+
    (I % V.M)(
        piano__0=l,
        piano__1=l)
    )
    assert splitted_score == expected_score