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