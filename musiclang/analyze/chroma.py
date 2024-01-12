from scipy.optimize import linear_sum_assignment
import numpy as np


def modulo_distance(a, b, modulo=12):
    """Calculate the distance in modulo space."""
    return min(abs(a - b), modulo - abs(a - b))


def optimal_assignment(A, B):
    """Find the optimal assignment between elements of A and B to minimize the sum of distances."""
    # Create a cost matrix with dimensions len(A) x len(B)
    cost_matrix = np.zeros((len(A), len(B)))

    # Fill the cost matrix with distances
    for i, a_elem in enumerate(A):
        for j, b_elem in enumerate(B):
            cost_matrix[i, j] = modulo_distance(a_elem, b_elem)

    # Use linear_sum_assignment to find the optimal assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Calculate the total cost of the optimal assignment
    total_cost = cost_matrix[row_ind, col_ind].sum()

    return (row_ind, col_ind), total_cost


def optimal_assignment_extended(A, B):
    """Find the optimal assignment between elements of A and every element of B."""
    # Number of times we need to duplicate the columns of the cost matrix
    duplication_factor = len(A) // len(B) + (1 if len(A) % len(B) > 0 else 0)

    # Create an expanded cost matrix
    expanded_cost_matrix = np.zeros((len(A), len(B) * duplication_factor))

    # Fill the expanded cost matrix with distances
    for i, a_elem in enumerate(A):
        for j, b_elem in enumerate(B * duplication_factor):
            expanded_cost_matrix[i, j] = modulo_distance(a_elem, B[j % len(B)])

    # Use linear_sum_assignment to find the optimal assignment
    row_ind, col_ind = linear_sum_assignment(expanded_cost_matrix)

    # Map the results back to the original elements of B
    original_col_ind = [index % len(B) for index in col_ind]

    # Calculate the total cost of the optimal assignment
    total_cost = expanded_cost_matrix[row_ind, col_ind].sum()

    return list(zip(row_ind, original_col_ind)), total_cost


def project_to_modulo_space(values, modulo=12):
    """Project the given values to their classes in Z/moduloZ."""
    return [value % modulo for value in values]


def find_nearest_value(original_value, assigned_class, modulo=12):
    """Find the nearest value in Z that is in the assigned class of Z/moduloZ."""
    base_value = original_value - original_value % modulo + assigned_class
    if original_value % modulo > modulo / 2:
        base_value += modulo
    return base_value


def optimal_assignment_with_projection(A, B):
    # Project A to Z/12Z
    projected_A = project_to_modulo_space(A)

    # Apply the extended assignment algorithm
    assignment, _ = optimal_assignment_extended(projected_A, B)
    # Map back to the nearest values in Z
    final_assignment = [(A[i], find_nearest_value(A[i], B[j])) for i, j in assignment]

    return final_assignment


def plot_chroma(chroma, t_start=None, t_end=None):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np

    Cs = chroma.to_numpy()
    t = chroma.columns.to_numpy().astype(float)

    fig, ax = plt.subplots()

    # Calculate the differences in the time vector for widths
    t_diff = np.diff(t, append=t[-1] + 1)

    # Plot each rectangle
    for i in range(Cs.shape[0]):
        for j in range(Cs.shape[1]):
            if Cs[i, j] == 1:
                rect = patches.Rectangle((t[j], i), t_diff[j], 1, linewidth=0, edgecolor='none', facecolor='black')
                ax.add_patch(rect)

    # Set the limits and aspect ratio
    ax.set_xlim([t[0], t[-1] + 1])
    ax.set_ylim([0, Cs.shape[0]])
    ax.set_aspect('auto')
    plt.grid()
    plt.show()


"""
Transform functions from musiclang to chromagrams and inverse
"""

import pandas as pd
def musiclang_to_chromagram(score, quantization=None):
    """
    Transform a musiclang score to a chromagram

    Parameters
    ----------
    score: musiclang.Score
    quantization: frac or None : Fraction of a beat to quantize to

    Returns
    -------
    Cs : chroma matrix
    t : time vector
    time_signature : time signature of the score

    """
    def chroma_matrix(A):
        A['pitch_class'] = pd.Categorical(A['pitch_class'], categories=list(range(12)))
        B = pd.crosstab(A['pitch_class'], A['time'], dropna=False)

        # Replace NaNs with 0s and convert to integers
        B = (B.fillna(0).astype(int) > 0).astype(int)

        # Sort the columns if needed
        B = B.sort_index(axis=1)
        return B

    time_signature = score.config['time_signature']
    seq = score.to_sequence()

    seq = seq[~seq['instrument'].str.startswith('drums')]
    seq = seq[seq['pitch'].notnull()]
    seq['pitch_class'] = seq['pitch'] % 12
    # Step 1: Create a DataFrame of time ranges
    if quantization is None:
        start_times = seq['start'].unique()
    else:
        start_times = np.arange(0, seq['end'].max(), quantization)

    times_df = pd.DataFrame(start_times, columns=['time']).merge(seq, how='cross')
    times_df = times_df[(times_df['start'] <= times_df['time']) &
                        (times_df['end'] > times_df['time'])
                        ]
    times_df = times_df[['time', 'pitch_class']]
    # Create a chromagram
    chroma = chroma_matrix(times_df)

    Cs = chroma.to_numpy().T
    t = chroma.columns.to_numpy().astype(float)

    return Cs, t, time_signature


def chroma_to_musiclang(Cs, t):
    """
    Transform a chromagram to a musiclang score

    Parameters
    ----------
    chroma

    Returns
    -------

    """
    from musiclang import Score
    from musiclang.library import I


    # Calculate the differences in the time vector for widths
    t_diff = np.diff(t, append=t[-1] + 1)

    chord = (I % I.M)

    score = []
    for idx, duration in enumerate(t_diff):
        chromas = np.argwhere(Cs[idx])[:, 0]
        chord_pitches = [chord.parse(chroma) for chroma in chromas]
        score.append(chord(*chord_pitches).set_duration(duration))

    return Score(score)

def chromagram_to_musiclang(Cs, t, base_voicing, time_signature, repeat_notes=False, reparse=True):
    """
    Transform a chromagram to a musiclang score using the base_voicing as a starting point

    Parameters
    ----------
    chroma: (Cs, t) tuple : Cs is the chroma matrix, t is the time vector
    base_voicing : list of pitches to use as a starting point

    Returns
    -------
    score : musiclang.Score
    """
    from musiclang.library import I
    from musiclang import Score
    from musiclang.transform.melody import ContinuationWhenSameNote

    t_diff = np.diff(t, append=t[-1] + 1)

    chord = (I % I.M)

    base_octaves = [b // 12 for b in base_voicing]
    score = []
    for idx, duration in enumerate(t_diff):
        chromas = np.argwhere(Cs[idx])[:, 0].tolist()
        assignment = optimal_assignment_with_projection(base_voicing, list(chromas))

        # Change the octave to limit to +1, -1 relative to base

        result = [l[1] for l in assignment]

        result_octaves = [l // 12 for l in result]
        for idx, (base_octave, result_octave) in enumerate(zip(base_octaves, result_octaves)):
            if base_octave - result_octave > 1:
                result[idx] += 12
            elif result_octave - base_octave > 1:
                result[idx] -= 12

        base_voicing = result

        chord_pitches = [chord.parse(chroma) for chroma in result]
        score.append(chord(*chord_pitches).set_duration(duration))


    score = Score(score, time_signature=time_signature)

    if not repeat_notes:
        score = ContinuationWhenSameNote()(score)

    if reparse:
        score = score.reparse()


    return score


