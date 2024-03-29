from musiclang import Score, Tonality
import numpy as np
from scipy.spatial.distance import cdist

from musiclang.analyze.chord_inference_utils import TEMPLATES, COEFFS, CHROMA_VECTORS_MATRIX, PITCH_CLASSES_DICT, \
    CHORD_TYPE_TO_PITCHES, CHORD_TYPES

EXTENSION_DICT = {(0, 3): '', (1, 3): '6', (2, 3): '64', (0, 4): '7', (1, 4): '65', (2, 4): '43',
                  (3, 4): '2'}
def max_correlation_index(input_matrix, template_matrix, bass_notes, use_first_max=False):

    # Add a small bonus to the bass note

    for i, bass_note in enumerate(bass_notes):
        if bass_note is not None:
            input_matrix[i, int(bass_note)] += 0.2


    # Calculate correlations
    correlations = 1 - cdist(input_matrix, template_matrix, 'correlation')
    # Multiply the correlations by coefficients
    correlations *= COEFFS

    # Find index of max correlation for each row
    if use_first_max:
        max_corr_indices = np.argmax(correlations, axis=1)
        chord_type = max_corr_indices % len(TEMPLATES)
        chord_root = max_corr_indices // len(TEMPLATES)
        return chord_root, chord_type

    temp_len = len(TEMPLATES)
    max_corr_indicess = [(correlations[i] == np.max(correlations[i, :])).nonzero()[0].tolist() for i in
                         range(len(correlations))]
    chord_typess = [[i // temp_len for i in max_corr_indices] for max_corr_indices in max_corr_indicess]
    chord_rootss = [[i % temp_len for i in max_corr_indices] for max_corr_indices in max_corr_indicess]

    return chord_rootss, chord_typess


def filter_notes(notes, start, end):
    pass


def get_chroma_vectors(notes, bars):
    drums_array = notes[:, 5] == 9
    # Remove drums
    notes = notes[~drums_array]
    times_array = np.asarray([notes[:, 0], notes[:, 0] + notes[:, 2]])
    pitches_class_array = notes[:, 1] % 12
    # Convert pitch class array to a 12xnb_notes matrix with each row being the indexes of the pitch class
    pitches_class_matrix = np.asarray(
        [[1.0 * ((i % 12) == pitch_class) for i in range(12)] for pitch_class in pitches_class_array])
    starts = np.asarray([bar[0] for bar in bars])
    ends = np.asarray([bar[1] for bar in bars])
    # Create a nb_notesxnb_bars array with each cell being the intersection length between the note and the bar
    intersections = np.maximum(0,
                               np.minimum(times_array[1, :, None], ends[None, :]) - np.maximum(times_array[0, :, None],
                                                                                               starts[None, :])).T
    bar_chroma_vectors = intersections.dot(pitches_class_matrix)
    # Normalize each rows
    try:
        normalizer = bar_chroma_vectors.sum(axis=1)[:, None]
    except:
        bar_chroma_vectors = np.zeros((len(bars), 12))
        normalizer = bar_chroma_vectors.sum(axis=1)[:, None]

    normalizer[normalizer == 0] = 1
    bar_chroma_vectors = bar_chroma_vectors / normalizer
    return bar_chroma_vectors


def get_bass_note_bar(notes, bars):
    """
    Return the bass note of each bar
    Parameters
    ----------
    notes
    bars

    Returns
    -------

    """
    drums_array = notes[:, 5] == 9
    notes = notes[~drums_array]
    start_times, end_times = notes[:, 0], notes[:, 0] + notes[:, 2]
    bass_notes = []
    for bar in bars:
        start, end = bar
        bar_notes = notes[((start_times >= start) & (start_times < end)) | ((end_times > start) & (end_times < end))]

        if len(bar_notes) == 0:
            bass_notes.append(None)
        else:
            min_pitch = np.min(bar_notes[:, 1]) % 12
            bass_notes.append(min_pitch)
    return bass_notes


def dynamic_programming_for_chord_inference(lists):


    n = len(lists)
    m = max(len(lst) for lst in lists)
    dp = [[float('inf')] * m for _ in range(n)]
    indices = [[0] * m for _ in range(n)]

    for i, s in enumerate(lists[0]):
        dp[0][i] = 0  # No string changes needed at the start

    for i in range(1, n):
        for j in range(len(lists[i])):
            # FIXME : Better cost function to include relative minor/major and key distances
            for k in range(len(lists[i - 1])):
                if lists[i][j] != lists[i - 1][k]:  # If the strings are different, we need a change
                    cost = 1
                else:
                    cost = 0

                if dp[i][j] > dp[i - 1][
                    k] + cost:  # If we found a better (smaller) cost, update the dp and indices array
                    dp[i][j] = dp[i - 1][k] + cost
                    indices[i][j] = k

    res = [0] * n
    min_cost, min_index = min(
        (cost, index) for index, cost in enumerate(dp[-1]))  # Find the smallest cost in the last row
    res[-1] = min_index  # The last index is the one with the smallest cost

    for i in range(n - 2, -1, -1):  # Backtrack to find the indices for the other lists
        res[i] = indices[i + 1][res[i + 1]]

    return res


def get_pitch_tonality_vector(tonality_root, tonality_mode):
    tonality = set([s % 12 for s in Tonality(tonality_root, tonality_mode).scale_pitches])
    pitch_vector = [1.0 * (i in tonality) for i in range(12)]
    return pitch_vector


def optimal_chord_inference(candidates, bass_notes=None, bars=None):
    """
    List of candidates per bar

    Parameters
    ----------
    candidates

    Returns
    -------

    """
    from musiclang import Chord
    candidates_nb = [[(c[1] + 3 * (c[2] == 'm')) % 12 for c in candidate] for candidate in candidates]

    indexes = dynamic_programming_for_chord_inference(candidates_nb)
    chords_props = [candidates[i][indexes[i]] for i in range(len(indexes))]

    if bars is None:
        bars = [None] * len(chords_props)
    if bass_notes is None:
        bass_notes = [None] * len(chords_props)

    chords = []
    for (roman, tonality_root, tonality_mode, extension), bar, bass_note in zip(chords_props, bars, bass_notes):
        chord = Chord(roman, tonality=Tonality(tonality_root, tonality_mode))[extension]
        if bar is not None:
            chord = chord.set_duration(bar[1] - bar[0])

        if bass_note is not None:
                chord = get_chord_extended_from_bass_note(bass_note, chord)
        chords.append(chord)

    return chords


def get_chord_extended_from_bass_note(bass_note, chord):
    extension = chord.extension
    chord_pitches = [pitch % 12 for pitch in chord.chord_pitches]
    nb_notes = len(chord_pitches)
    if bass_note in chord_pitches:
        bass_idx = chord_pitches.index(bass_note)
        extension = EXTENSION_DICT[(bass_idx, nb_notes)]
    else:
        extension = ''

    new_extension = extension + (
        chord.extension[1:] if chord.extension.startswith('7') else chord.extension)

    chord.extension = new_extension

    return chord.copy()

def fast_chord_inference(notes, bars):
    """
    Return the chord progression of the song, one chord per bar
    It uses dynamic programming to find the roman numeral chord progression that minimize the number of tonality changes
    Parameters
    ----------
    notes
    bars

    Returns
    -------

    """

    notes = np.asarray(notes.copy().values)

    bar_chroma_vectors = get_chroma_vectors(notes, bars)
    # Get the lowest note of each bar
    bass_notes = get_bass_note_bar(notes, bars)

    chord_rootss, chord_typess = max_correlation_index(bar_chroma_vectors, CHROMA_VECTORS_MATRIX, bass_notes, use_first_max=False)

    candidates = []
    for chord_roots, chord_types, bar, chroma in zip(chord_rootss, chord_typess, bars, bar_chroma_vectors):
        all_sub_candidates = []
        for chord_type, chord_root in zip(chord_roots, chord_types):
            from musiclang import Tonality, Chord
            # Get the list of roman numeral candidates
            pitches = tuple(
                sorted([(chord_root + pitch) % 12 for pitch in CHORD_TYPE_TO_PITCHES[CHORD_TYPES[chord_type]]]))
            subcandidates = PITCH_CLASSES_DICT[pitches]
            # Filter only maximum correlation candidates
            pitch_vectors = np.asarray([get_pitch_tonality_vector(tonality_root, tonality_mode)
                                        for (roman, tonality_root, tonality_mode, extension) in subcandidates])
            correlations = np.asarray([np.correlate(chroma, pitch_vector) for pitch_vector in pitch_vectors])
            # Get the list of maximum correlation candidates (there can be several)
            max_correlations = np.where(correlations == correlations.max())[0]
            subcandidates = [subcandidates[i] for i in max_correlations]
            all_sub_candidates += subcandidates

        if len(all_sub_candidates) == 0:
            all_sub_candidates = [(0, 0, 'M', '')]
        candidates.append(all_sub_candidates)


    # Choose the candidate chord path that minimize the number of tonality changes
    chords = optimal_chord_inference(candidates, bass_notes=bass_notes, bars=bars)
    chords = Score(chords)
    return chords
