import numpy as np
from .constants import PROFILES
from .utils_proba import softmax

def _get_pitch_tonality_prob(p, t):
    r, m = t.degree, t.mode
    corr = np.roll(PROFILES[m], r)
    corrcoef = np.corrcoef(corr, p)[1, 0]
    if corrcoef != corrcoef:
        corrcoef = 0
    return (1 + corrcoef)/2

def _get_pitch_chord_prob(p, c):
    pitches = c.pitch_set
    chord = np.zeros(12)
    for pi in pitches:
        chord[pi] = 1
    corrcoef = np.corrcoef(chord, p)[1, 0]
    if corrcoef != corrcoef:
        corrcoef = 0
    return (1 + corrcoef)/2

def _get_pitch_chord_tonality_prob(p, c):
    return _get_pitch_chord_prob(p, c) # * _get_pitch_tonality_prob(p, c.tonality)

def get_chords_emission_matrix(pitch_vectors, **kwargs):
    index = get_chords_index()
    emission = np.zeros((len(pitch_vectors), len(index)))
    for idx1, p in enumerate(pitch_vectors):
        for idx2, c in enumerate(index):
            emission[idx1, idx2] =_get_pitch_chord_tonality_prob(p, c)
    # Normalize
    emission = normalize_columns(emission)
    return emission

def get_chords_prior_matrix(**kwargs):
    index = get_chords_index()
    prior = np.zeros(len(index))
    for idx, chord in enumerate(index):
        base = 1
        if chord.element in [0, 3, 4]:
            base *= 2
        if chord.element in [2, 6]:
            base /= 2
        if chord.tonality.mode == 'mm':
            base /= 2
        if chord.extension != 5 and chord.element != 4:
            base /= 2
        if chord.element == 4 and chord.extension == 7:
            base *= 2
        prior[idx] = base

    prior = prior / np.linalg.norm(prior, ord=1)
    return prior

def get_chords_index():
    from musiclang.core.chord import Chord
    from musiclang.core.tonality import Tonality
    index = [Chord(i, tonality=Tonality(j, mode=mode))[extension] for j in range(12) for i in range(7) for mode in
             ['M', 'm', 'mm'] for extension in [5, 7]]
    return index


def _get_tonality_distance(t1, t2, change_tone_malus=10, power_dist=1, **kwargs):
    from .constants import PATTERNS_DICT, PATTERNS

    r1, m1 = t1.degree, t1.mode
    r2, m2 = t2.degree, t2.mode
    if r1 == r2 and m1 == m2:
        return 0.1 / len(PATTERNS[m1]) ** power_dist

    r2 = (r2 - r1) % 12
    dist = ((PATTERNS_DICT[m1][(r2, m2)] + change_tone_malus)**power_dist) / (len(PATTERNS[m1]) ** power_dist)
    return dist

def _get_chord_distance(c1, c2, power_distance=1, **kwargs):
    if c1.tonality.degree == c2.tonality.degree and c1.tonality.mode == c2.tonality.mode:
        return 0.1
    s1 = c1.pitch_set
    s2 = c2.pitch_set
    max_len = max(len(s1), len(s2))
    return ((max_len - len(s2 & s1))/max_len)**power_distance + 1

def _get_chord_tonality_distance(c1, c2, **kwargs):
    return _get_chord_distance(c1, c2, **kwargs) + _get_tonality_distance(c1.tonality, c2.tonality, **kwargs)


def normalize_columns(x):
    x_norm = np.linalg.norm(x, ord=1, axis=1)
    nonzero_frames = x_norm > 0
    x[nonzero_frames, :] /= x_norm[nonzero_frames, np.newaxis]
    return x


def dist_tonality_chord(tonality, chord, chord_pitch_out_of_key_prob):
    tonality_notes = tonality.scale_set
    chord_notes = chord.pitch_set
    num_pitches_out_of_key = len(chord_notes - tonality_notes)
    num_pitches_in_key = len(chord_notes & tonality_notes)
    mat = ((1 - chord_pitch_out_of_key_prob) ** num_pitches_in_key *
           chord_pitch_out_of_key_prob ** num_pitches_out_of_key)
    return mat


def get_tonality_index():
    from musiclang.core.tonality import Tonality
    index = [Tonality(j, mode=mode) for j in range(12) for mode in
             ['M', 'm', 'mm']]
    return index

def _get_dist_tonality_matrix(tonality_index, chord_index, chord_pitch_out_of_key_prob):
    mat = np.zeros([len(tonality_index), len(chord_index)])

    for idx1, to in enumerate(tonality_index):
        for idx2, ch in enumerate(chord_index):
            mat[idx1, idx2] = dist_tonality_chord(to, ch, chord_pitch_out_of_key_prob)
    mat /= mat.sum(axis=1)[:, np.newaxis]
    return mat

def _key_chord_transition_distribution(
        chord_index, tonality_index, dist_tonality_matrix, key_change_prob, chord_change_prob):
    """Transition distribution between key-chord pairs."""
    mat = np.zeros([len(chord_index), len(chord_index)])

    for i, key_chord_1 in enumerate(chord_index):
        for j, key_chord_2 in enumerate(chord_index):
            if key_chord_1.tonality != key_chord_2.tonality:
                # Key change. Chord probability depends only on key and not previous
                # chord.
                mat[i, j] = (key_change_prob / 11)
                mat[i, j] *= dist_tonality_matrix[tonality_index.index(key_chord_1.tonality), j]

            else:
                # No key change.
                mat[i, j] = 1 - key_change_prob
                if key_chord_1 != key_chord_2:
                    # Chord probability depends on key, but we have to redistribute the
                    # probability mass on the previous chord since we know the chord
                    # changed.
                    current = dist_tonality_matrix[tonality_index.index(key_chord_2.tonality), j]
                    previous = dist_tonality_matrix[tonality_index.index(key_chord_2.tonality), i]

                    mat[i, j] *= (
                        chord_change_prob * (
                            current +
                            previous / (dist_tonality_matrix.shape[1] - 1)))
                else:
                    # No chord change.
                    mat[i, j] *= 1 - chord_change_prob
    return mat

def get_new_chords_transition_matrix(key_change_prob=0.001,
                              chord_change_prob=0.5,
                              chord_pitch_out_of_key_prob=0.01, **kwargs):

    tonality_index = get_tonality_index()
    chord_index = get_chords_index()
    dist_tonality_matrix = _get_dist_tonality_matrix(tonality_index, chord_index, chord_pitch_out_of_key_prob)
    transitions = _key_chord_transition_distribution(chord_index, tonality_index, dist_tonality_matrix, key_change_prob, chord_change_prob)
    return transitions


def get_chords_transition_matrix(temperature=1, **kwargs):

    index = get_chords_index()
    # For each couple calculate transition
    dist_matrix = np.zeros((len(index), len(index)))
    for i1, c1 in enumerate(index):
        for i2, c2 in enumerate(index):
            dist_matrix[i1, i2] = _get_chord_tonality_distance(c1, c2)

    # Normalize the dist matrix by columns
    prob_matrix = np.apply_along_axis(lambda x: softmax(x, temperature=temperature), 1, - dist_matrix.copy())
    return prob_matrix