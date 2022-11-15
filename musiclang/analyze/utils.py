from .constants import *

def chord_to_pitches(chord):
    if chord == NO_CHORD:
        return []
    name, chord_kind = chord.split(':')
    root = PITCH_CLASS_DICT[name]
    pitches = CHORD_KIND_PITCHES[chord_kind]
    pitches = [(pitch + root) % 12 for pitch in pitches]
    return frozenset(pitches)



def softmax(x, temperature=1.0, axis=None):
    tx = x/temperature
    y = np.exp((tx - np.max(tx)))
    f_x = y / np.sum(y)
    return f_x
