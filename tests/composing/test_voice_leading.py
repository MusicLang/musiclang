from musiclang.library import *
from musiclang.transform.composing import VoiceLeading



def test_voice_leading_use_fixed_voices():
    score = (I % I.M)(cello=s0, violin=s1) * 2
    vl = VoiceLeading(
        fixed_voices=['cello__0'],
        seed=5,
        method='voices_and_rules',
        max_iter=10,
        max_iter_rules=10,
        temperature=4,
        min_temp=1,
        max_norm=3
    )
    new_score = vl.optimize(
        score,
        )


    assert new_score == (I % I.M)(cello=s0, violin=s3) + (I % I.M)(cello=s0, violin=s1)


def test_voice_leading_use_types():
    score = (I % I.M)(cello=s0, violin=h2) + (I % I.M)(cello=s0, violin=h2)
    vl = VoiceLeading(
        types=['s'],
        seed=1,
        method='rules',
        max_iter=100,
        max_iter_rules=10,
        temperature=4,
        min_temp=1,
        max_norm=1
    )
    new_score = vl.optimize(score)

    assert new_score == (I % I.M)(cello__0=s5.o(-1), violin__0=h2)+ (I % I.M)(cello__0=s0,	violin__0=h2)

def test_voice_leading_correct_parallel_dissonnances():
    score = (I % I.M)(cello=s0, violin=s1) + (I % I.M)(cello=s0, violin=s1)
    vl = VoiceLeading(
        seed=3,
        fixed_voices=['violin__0'],
        method='rules',
        max_iter=100,
        max_iter_rules=10,
        temperature=4,
        min_temp=1,
        max_norm=3
    )
    new_score = vl.optimize(score)

    assert new_score == (I % I.M)(	cello__0=s5.o(-1),	violin__0=s1)+ (I % I.M)(cello__0=s0,	violin__0=s1)

def test_voice_leading_silences_works():
    score = (I % I.M)(cello=s0, violin=r) + (I % I.M)(cello=s0, violin=r)
    vl = VoiceLeading(
        seed=3,
        fixed_voices=['violin__0'],
        method='rules',
        max_iter=100,
        max_iter_rules=10,
        temperature=4,
        min_temp=1,
        max_norm=1
    )
    new_score = vl.optimize(score)

    assert new_score == (I % I.M)(cello__0=s4.o(-1), violin__0=r)+ (I % I.M)(cello__0=s5.o(-1),	violin__0=r)