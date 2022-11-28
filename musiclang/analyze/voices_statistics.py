import numpy as np
from musiclang.core.pitches.pitches_utils import note_to_pitch_result

def get_mean_pitch_all_voices(score):
    voices = score.instruments
    result = {}
    for voice_name in voices:
        notes = []
        for chord in score:
            if voice_name in chord.score:
                notes += [note_to_pitch_result(n, chord) for n in chord.score[voice_name].notes if n.is_note]

        result[voice_name] = np.mean(notes)

    return result


def get_nb_notes_all_voices(score):
    voices = score.instruments
    result = {}
    for voice_name in voices:
        notes = 0
        for chord in score:
            if voice_name in chord.score:
                notes += len([n for n in chord.score[voice_name].notes if n.is_note])
        result[voice_name] = notes

    return result