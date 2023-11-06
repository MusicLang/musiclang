from musiclang.library import *
from musiclang import Score
from musiclang.analyze.score_formatter import ScoreFormatter

expected_text = """
(I % I.m)(
	piano__0=b0.h, 
	piano__1=b1.h, 
	piano__2=b2.h, 
	piano__3=b3.h)+ 
(V['7'] % V.M)(
	piano__0=b0.hd, 
	piano__1=b1.hd, 
	piano__2=b2.hd, 
	piano__3=b3.hd)+ 
(I % I.M)(
	piano__0=b0.hd, 
	piano__1=b1.hd, 
	piano__2=b2.hd, 
	piano__3=b3.hd)+ 
(V['7'] % IV.s.m)(
	piano__0=b0.w, 
	piano__1=b1.w, 
	piano__2=b2.w, 
	piano__3=b3.w)+ 
(I['64'] % I.m)(
	piano__0=b0.h, 
	piano__1=b1.h, 
	piano__2=b2.h, 
	piano__3=b3.h)+ 
(V['7(sus2)'] % II.M)(
	piano__0=b0.h, 
	piano__1=b1.h, 
	piano__2=b2.h, 
	piano__3=b3.h)
"""


def test_score_formatter_simple():
    text = """
    Time Signature: 4/4
    
    m0 c: i b3 II7
    m1 b2 I
    m2 N7
    m3 Cad64 b3 D: V7[sus2]
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text)
    assert score == expected_score


expected_text2 = """
(I % I.M)(
	piano__0=b0, 
	piano__1=b1, 
	piano__2=b2, 
	piano__3=b3)+ 
(V['7'] % I.M)(
	piano__0=b0.h, 
	piano__1=b1.h, 
	piano__2=b2.h, 
	piano__3=b3.h) 
"""


def test_score_formatter_time_signature_68():
    text = """
    Time Signature: 6/8
    m0 C: I b1.66 V7
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text2)
    assert score == expected_score

expected_text2b = """
(I % I.M)(
	piano__0=b0, 
	piano__1=b1, 
	piano__2=b2, 
	piano__3=b3)+ 
(V['7'] % I.M)(
	piano__0=b0.h, 
	piano__1=b1.h, 
	piano__2=b2.h, 
	piano__3=b3.h) 
"""


def test_score_formatter_start_measure1():
    text = """
    Time Signature: 6/8
    m1 C: I b1.66 V7
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text2b)
    assert score == expected_score


expected_text3 = """
(I % I.M)(
	piano__0=b0, 
	piano__1=b1, 
	piano__2=b2, 
	piano__3=b3)+ 
(V['7'] % I.M)(
	piano__0=b0.hd, 
	piano__1=b1.hd, 
	piano__2=b2.hd, 
	piano__3=b3.hd) 
"""


def test_score_formatter_time_signature_22():
    text = """
    Time Signature: 2/2
    m0 C: I b1.5 V7
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text3)
    assert score == expected_score


expected_text4 = """
(I % I.M)(
	piano__0=b0.w, 
	piano__1=b1.w, 
	piano__2=b2.w, 
	piano__3=b3.w)+ 
(V['7'] % I.M)(
	piano__0=b0.hd, 
	piano__1=b1.hd, 
	piano__2=b2.hd, 
	piano__3=b3.hd) 
"""


def test_score_formatter_time_signature_change():
    text = """
    Time Signature: 2/2
    m0 C: I
    Time Signature: 3/4
    m1 V7
    """
    sf = ScoreFormatter(text)
    score = sf.parse(allow_multi_signature=True)
    expected_score = Score.from_str(expected_text4)
    assert score == expected_score


expected_text5 = """
(I % I.M)(
	piano__0=b0.wd, 
	piano__1=b1.wd, 
	piano__2=b2.wd, 
	piano__3=b3.wd)+ 
(V['7'] % I.M)(
	piano__0=b0, 
	piano__1=b1, 
	piano__2=b2, 
	piano__3=b3) 
"""


def test_score_formatter_time_signature_change_complex():
    text = """
    Time Signature: 2/2
    m0 C: I
    Time Signature: 3/4
    m1 b3 V7
    """
    sf = ScoreFormatter(text)
    score = sf.parse(allow_multi_signature=True)
    expected_score = Score.from_str(expected_text5)
    assert score == expected_score


expected_text6 = """
(I % I.M)(
	piano__0=b0.augment(frac(8, 1)), 
	piano__1=b1.augment(frac(8, 1)), 
	piano__2=b2.augment(frac(8, 1)), 
	piano__3=b3.augment(frac(8, 1)))+ 
(V['7'] % I.M)(
	piano__0=b0.w, 
	piano__1=b1.w, 
	piano__2=b2.w, 
	piano__3=b3.w) 
"""


def test_score_formatter_multi_bars():
    text = """
    Time Signature: 2/2
    m0 C: I
    m2 V7
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text6)
    assert score == expected_score


expected_text7 = """
(I % I.M)(
	piano__0=b0.w, 
	piano__1=b1.w, 
	piano__2=b2.w, 
	piano__3=b3.w)+ 
(I % I.M)(
	piano__0=b0.w, 
	piano__1=b1.w, 
	piano__2=b2.w, 
	piano__3=b3.w)
"""

def test_score_ignore_var():
    text = """
    Time Signature: 4/4
    m0 C: I
    m0var1 c: III
    m0var2 c: III
    m1 I
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text7)
    assert score == expected_score


expected_text8 = """
(I % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w)+
(I % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w)
"""


def test_score_repeated_bar():
    text = """
    Time Signature: 4/4
    m0 C: I
    m1 = m0
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text8)
    assert score == expected_score


expected_text9 = """
(I % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w)+
(V % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) +
(I % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) +
(V % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) +
(VI % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) 
	
"""


def test_score_multi_repeat():
    text = """
    Time Signature: 4/4
    m0 C: I
    m1 V
    m2-3 = m0-1
    m4 vi
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text9)
    assert score == expected_score


expected_text10 = """
(I % I.M)(
	piano__0=b0.h,
	piano__1=b1.h,
	piano__2=b2.h,
	piano__3=b3.h)+
(V % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) +
(I % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) +
(VI % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) 
"""

def test_score_pickup_bar():
    text = """
    Time Signature: 4/4
    m0 C: b3 I
    m1 V
    m2 I
    m3 vi
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text10)
    assert score == expected_score


expected_text11 = """
(I % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w,
	violin__0=r.w
	) +
(V % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w,
	violin__0=r.w
	) +
(I % I.M)(
    piano__0=b0.o(-2).w,
    piano__1=b2.o(-1).w,
    piano__2=b3.w,
    violin__0=b1.o(1).w,
    piano__3=r.w
    )+
(VI % I.M)(
    piano__0=b0.o(-2).w,
    piano__1=b2.o(-1).w,
    piano__2=b3.w,
    violin__0=b1.o(1).w,
    piano__3=r.w
    )
"""
def test_score_change_voicing():
    text = """
    Time Signature: 4/4
    m0 C: I
    m1 V
    !instruments piano    piano    piano violin
    !voicing     b0.o(-2) b2.o(-1) b3    b1.o(1)
    m2 I
    m3 vi
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text11)
    assert score == expected_score


expected_text12 = """
(I % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) +
(V % I.M)(
	piano__0=b0.w,
	piano__1=b1.w,
	piano__2=b2.w,
	piano__3=b3.w) +
(I % I.M)(
    piano__0=b0.o(-2).w,
    piano__1=b2.o(-1).w,
    piano__2=b3.w,
    violin__0=b1.o(1).w)+
(VI % I.M)(
    piano__0=b0.o(-2).w,
    piano__1=b2.o(-1).w,
    piano__2=b3.w,
    violin__0=b1.o(1).w)
"""
def test_voice_leading_work():
    text = """
    !voice_leading
    Time Signature: 4/4
    m0 C: I
    m1 V
    !instruments piano    piano    piano violin
    !voicing     b0.o(-2) b2.o(-1) b3    b1.o(1)
    m2 I
    m3 vi
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    not_expected_score = Score.from_str(expected_text12)
    assert score != not_expected_score

expected_text13 = """
(I % I.M)(
	piano__0=b0.o(-2).w,
	violin__0=b0.h + b0.h) +
(V % I.M)(
	piano__0=b0.o(-2).w,
	violin__0=b0.w)
"""
def test_rhythm():
    text = """
    Time Signature: 4/4
    !instruments piano violin
    !voicing  b0.o(-2) b0
    !rhythm violin x.x.|x...
    m0 C: I
    m1 V
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text13)
    assert score == expected_score



expected_text14 = """
(I % I.M)(
	piano__0=b0.o(-2).w,
	violin__0=b0.w) +
(V % I.M)(
	piano__0=b0.o(-2).w,
	violin__0=b0.w)+
(I % I.M)(
	piano__0=b0.o(-2).w,
	violin__0=b0.h + b0.h) +
(V % I.M)(
	piano__0=b0.o(-2).w,
	violin__0=b0.w)
"""
def test_rhythm_change():
    text = """
    Time Signature: 4/4
    !instruments piano violin
    !voicing  b0.o(-2) b0
    m0 C: I
    m1 V
    !rhythm violin x.x.|x...
    m2 C: I
    m3 V
    """
    sf = ScoreFormatter(text)
    score = sf.parse()
    expected_score = Score.from_str(expected_text14)
    assert score == expected_score