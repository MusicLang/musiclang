import numpy as np

from .random_melody import generate_random_melody
from musiclang.composing.arrange import arrange_melody_with_chords

def generate_random_score(duration, instruments, candidate_chords):
    """Generate a score with given duration and instruments and candidate chords

    Parameters
    ----------
    duration :
        param instruments:
    candidate_chords :
        return:
    instruments :
        

    Returns
    -------

    """
    melody, patterns = generate_random_melody(duration)
    assert sum(patterns, None).duration == duration
    score = sum([np.random.choice(candidate_chords) for i in range(len(patterns))], None)
    fixed_voice = []
    for idx, inst in enumerate(instruments):
        melody, patterns2 = generate_random_melody(duration)
        fixed_voice.append(melody)

    for inst, voice in zip(instruments, fixed_voice):
        score = arrange_melody_with_chords(voice, patterns, score, inst)

    return score