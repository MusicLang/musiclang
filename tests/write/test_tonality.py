from musiclang import Tonality


def test_tonalities_equal():

    t1 = Tonality(0,  mode="m", octave=0)
    t2 = Tonality(0,  mode="m", octave=0)
    assert t1 == t2
    assert t1 == t1.copy()


def test_tonalities_degree_not_equal():

    t1 = Tonality(0,  mode="m", octave=0)
    t2 = Tonality(1, mode="m", octave=0)
    assert t1 != t2


def test_abs_degree():
    t1 = Tonality(2, mode="m", octave=0)
    assert t1.abs_degree == 2


def test_tonalities_mode_not_equal():

    t1 = Tonality(0,  mode="m", octave=0)
    t2 = Tonality(1,  mode="M", octave=0)
    assert t1 != t2

def test_tonalities_octave_not_equal():

    t1 = Tonality(0,  mode="m", octave=0)
    t2 = Tonality(1,  mode="m", octave=1)
    assert t1 != t2



def test_tonality_addition_octave():
    t1 = Tonality(5,  mode="M", octave=0)
    t2 = Tonality(6,  mode="m", octave=0)
    result = t1 + t2
    assert result == Tonality(11, mode="m", octave=0)

def test_enharmonic_equalities():
    # #Fifths == fifths
    assert Tonality(4, mode="m", octave=1) == Tonality(4,  mode="m", octave=1)


def test_tonality_addition_thirds():
    # For simplification : III# of C is considered as E not E#, idem for VII#
    t1 = Tonality(2, mode="M", octave=1)
    t2 = Tonality(1,  mode="m", octave=0)
    result = t1 + t2
    assert result == Tonality(3, mode="m", octave=1)


def test_tonality_addition_with_accidents():
    # For simplification : III# of C is considered as E not E#, idem for VII#
    t1 = Tonality(2, mode="m", octave=1)
    t2 = Tonality(2, mode="m", octave=0)
    result = t1 + t2
    assert result == Tonality(4, mode="m", octave=1)


def test_tonality_to_scale_pitches():
    t1 = Tonality(1, mode="m", octave=1)
    scale_pitches = t1.scale_pitches

    assert scale_pitches == [13, 15, 16, 18, 20, 21, 24]


def test_abs_degree_of_mode():
    T = Tonality(1, mode="locrian", octave=0)
    assert T.abs_degree == 1

def test_abs_degree_of_sum_of_mode():
    T = Tonality(1, mode="locrian", octave=0)
    assert (T + T).abs_degree == 2

def test_tonality_to_scale_pitches_mode():
    t1 = Tonality(0,  mode="dorian", octave=0)
    scale_pitches = t1.scale_pitches

    assert scale_pitches == [0, 2, 3, 5, 7, 9, 10]


# "", b, n, s : b force to be minor interval, n : major interval, "" normal mode interval
# 3s.M = E

def test_change_mode():
    t1 = Tonality(2,  mode="m", octave=0)
    new_mode = "locrian"
    t2 = t1.change_mode(new_mode)
    assert t2.scale_pitches[0] == t1.scale_pitches[0]