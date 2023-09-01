import pandas as pd
import numpy as np

COLUMNS_CHORDS = ['chord_degree', 'tonality_degree', 'tonality_mode']
COLUMNS_MELODY = ['note_type', 'note_val', 'note_octave']
COLUMNS_RYTHM = ['note_duration', 'silence', 'continuation']
COLUMNS_HARMONIC_RYTHM = ['chord_duration', 'dummy']


def merge_and_update(left, right, on):
    """Merge two sequences by updating when it is possible
    If the right array does not have an entry for the left row, use the previous value of the column

    Parameters
    ----------
    left :
        Sequence that should be updated
    right :
        Sequence acting as the updater
    on :
        str or list, on which columns to perform the left join

    Returns
    -------

    """
    if isinstance(on, str) or isinstance(on, int):
        on = [on]
    new_columns = list(set(right.columns) - set(on))
    final = left.merge(right, on=on, how='left')
    colsx = [col + '_x' for col in new_columns]
    colsy = [col + '_y' for col in new_columns]
    for col in new_columns:
        final[col] = final[col + '_y'].fillna(final[col + '_x'])
    final = final.drop(colsx + colsy, axis=1)
    return final



# Find markov path of chords

def find_words_proba(df, columns, n=4):
    """Find the markov distribution with word of size n

    Parameters
    ----------
    df :
        param columns:
    n :
        return: (Default value = 4)
    columns :
        

    Returns
    -------

    """
    from collections import Counter
    sequence = df[columns]
    # Merge n times
    series = [sequence.add_suffix(f'_{i}').reindex(np.roll(sequence.index, -i)).reset_index(drop=True) for i in
              range(n)]
    df1 = pd.concat(series, axis=1)
    probas = df1.values.tolist()
    nb = len(probas)
    counts = dict(Counter([tuple(m) for m in probas]))
    probas = {key: val / nb for key, val in counts.items()}
    return probas


def find_transitions_proba(df, columns, n=4):
    """

    Parameters
    ----------
    df :
        
    columns :
        
    n :
         (Default value = 4)

    Returns
    -------

    """
    from collections import Counter
    sequence = df[columns]
    assert sequence.isnull().sum().sum() == 0
    sequence = sequence.reset_index(drop=True)
    # Merge n times
    series1 = [sequence.add_suffix(f'_{i}_A').reindex(np.roll(sequence.index, -i)).reset_index(drop=True) for i in
               range(n)]
    series2 = [sequence.add_suffix(f'_{i}_B').reindex(np.roll(sequence.index, -i)).reset_index(drop=True) for i in
               range(n, 2 * n)]
    series = series1 + series2
    df1 = pd.concat(series, axis=1)
    other_columns = [col for col in df1.columns if col.endswith('_B')]
    groups_columns = [col for col in df1.columns if col.endswith('_A')]
    assert df1.isnull().sum().sum() == 0
    all_columns = list(df1.columns)
    df1['count'] = 1
    global_counts = df1.groupby(groups_columns)['count'].count()
    probas = df1.groupby(all_columns)['count'].count()
    probs = probas / global_counts
    # Get dict of dict indexed by A
    groups = probs.groupby(level=list(range(len(columns) * n)))
    res = {}
    for group in groups.groups:
        res[group] = probs.loc[group].to_dict()

    return res


def sample_markov_path(words, transitions, first=None, m=10, n=1):
    """Sample m transitions from a markov path

    Parameters
    ----------
    words :
        
    transitions :
        
    first :
         (Default value = None)
    m :
         (Default value = 10)
    n :
         (Default value = 1)

    Returns
    -------

    """

    def split(a, n):
        """

        Parameters
        ----------
        a :
            
        n :
            

        Returns
        -------

        """

        parts = len(a) // n
        k, m = divmod(len(a), parts)
        return [a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(parts)]

    def _sample_at_random(D):
        """

        Parameters
        ----------
        D :
            

        Returns
        -------

        """
        return random.choices(list(D.keys()), weights=D.values(), k=1)[0]

    import random
    if first is None:
        previous = _sample_at_random(words[n])
    else:
        previous = first

    N = len(previous) // n
    result = split(previous, N)
    for i in range(m):
        new_sample = _sample_at_random(transitions[n][previous])
        previous = tuple(new_sample)
        N = len(previous) // n
        result += split(new_sample, N)

    return result


def find_distribution(df, columns, n=2):
    """Calculate the words and transitions of words distribution for given columns

    Parameters
    ----------
    df :
        param columns:
    n :
        return: (Default value = 2)
    columns :
        

    Returns
    -------

    """
    words_probs = find_words_proba(df, columns, n=n)
    transitions_probs = find_transitions_proba(df, columns, n=n)

    return words_probs, transitions_probs


def find_chords_distribution(df):
    """Find the chords and chords transitions probabilities of a sequence

    Parameters
    ----------
    df :
        return:

    Returns
    -------

    """
    chords = df.groupby('chord_idx').first()

    N = [1, 2, 3, 4]
    words_result = {}
    transitions_result = {}
    for n in N:
        words_probs, transitions_probs = find_distribution(chords, COLUMNS_CHORDS, n=n)
        words_result[n] = words_probs
        transitions_result[n] = transitions_probs
    return words_result, transitions_result


def find_rythm_distribution(df):
    """Find the rythm and rythm transitions probabilities of a sequence

    Parameters
    ----------
    df :
        return:

    Returns
    -------

    """

    df = df.sort_values(['instrument', 'start'], ascending=True)
    N = [1, 2, 3, 4]
    words_result = {}
    transitions_result = {}
    for n in N:
        words_probs, transitions_probs = find_distribution(df, COLUMNS_RYTHM, n=n)
        words_result[n] = words_probs
        transitions_result[n] = transitions_probs
    return words_result, transitions_result


def find_melody_distribution(df):
    """Find the melody and melody transitions probabilities of a sequence

    Parameters
    ----------
    df :
        return:

    Returns
    -------

    """
    df = df.sort_values(['instrument', 'start'], ascending=True)
    N = [1, 2, 3, 4]
    words_result = {}
    transitions_result = {}
    for n in N:
        words_probs, transitions_probs = find_distribution(df, COLUMNS_MELODY, n=n)
        words_result[n] = words_probs
        transitions_result[n] = transitions_probs
    return words_result, transitions_result


def find_harmonic_rythm_distribution(df):
    """Find the harmonic rythm and harmonic rythm transitions probabilities of a sequence

    Parameters
    ----------
    df :
        return:

    Returns
    -------

    """
    df['chord_duration_max'] = df.groupby('chord_idx')['chord_relative_end'].transform('max')
    df['chord_duration_min'] = df.groupby('chord_idx')['chord_relative_start'].transform('min')
    df['chord_duration'] = df['chord_duration_max'] - df['chord_duration_min']
    chords = df.groupby('chord_idx').first()
    chords['dummy'] = 0
    chords = chords[['chord_duration', 'dummy']]
    N = [1, 2, 3, 4]
    words_result = {}
    transitions_result = {}
    for n in N:
        words_probs, transitions_probs = find_distribution(chords, COLUMNS_HARMONIC_RYTHM, n=n)
        words_result[n] = words_probs
        transitions_result[n] = transitions_probs
    return words_result, transitions_result


def find_distributions(df):
    """

    Parameters
    ----------
    df :
        

    Returns
    -------

    """
    Pc, Tc = find_chords_distribution(df)
    Pr, Tr = find_rythm_distribution(df)
    Pm, Tm = find_melody_distribution(df)
    Ph, Th = find_harmonic_rythm_distribution(df)
    
    return Pc, Tc, Pr, Tr, Pm, Tm, Ph, Th

def sample_score(Pc, Tc, Pr, Tr, Pm, Tm, Ph, Th, duration=10, n_c=1, n_h=1, n_r=1, n_m=4):
    """

    Parameters
    ----------
    Pc :
        
    Tc :
        
    Pr :
        
    Tr :
        
    Pm :
        
    Tm :
        
    Ph :
        
    Th :
        
    duration :
         (Default value = 10)
    n_c :
         (Default value = 1)
    n_h :
         (Default value = 1)
    n_r :
         (Default value = 1)
    n_m :
         (Default value = 4)

    Returns
    -------

    """
    import pandas as pd
    def _sample_with_duration_constraint(P, T, idx_duration, duration, n=1):
        """

        Parameters
        ----------
        P :
            
        T :
            
        idx_duration :
            
        duration :
            
        n :
             (Default value = 1)

        Returns
        -------

        """
        import numpy as np
        # Sample harmonic rythm
        m = 10
        while True:
            path = sample_markov_path(P, T, first=None, m=m, n=n)
            array_duration = np.asarray([p[idx_duration] for p in path])
            sample_duration = np.sum(array_duration)
            if sample_duration > duration:
                cumsum = np.cumsum(array_duration)
                idx_break = np.argmax(cumsum >= duration)
                to_remove = cumsum[idx_break] - duration
                path[idx_break] = list(path[idx_break])
                path[idx_break][idx_duration] = path[idx_break][idx_duration] - to_remove
                path[idx_break] = tuple(path[idx_break])
                path = path[:idx_break + 1]
                break
            elif sample_duration == duration:
                break
            else:
                m = 2 * m
        return path

    path_h = _sample_with_duration_constraint(Ph, Th, 0, duration, n=n_h)
    path_c = sample_markov_path(Pc, Tc, first=None, m=len(path_h), n=n_c)
    path_r = _sample_with_duration_constraint(Pr, Tr, 0, duration, n=n_r)
    path_m = sample_markov_path(Pm, Tm, first=None, m=len(path_r), n=n_m)

    path_c = path_c[:len(path_h)]
    path_m = path_m[:len(path_r)]
    assert len(path_h) == len(path_c), (len(path_h), len(path_c))
    assert len(path_r) == len(path_m), (len(path_r), len(path_m))
    # Create melody serie
    melody_df = pd.DataFrame(path_m, columns=COLUMNS_MELODY)
    rythm_df = pd.DataFrame(path_r, columns=COLUMNS_RYTHM)
    harmonic_rythm_df = pd.DataFrame(path_h, columns=COLUMNS_HARMONIC_RYTHM)
    chords_df = pd.DataFrame(path_c, columns=COLUMNS_CHORDS)

    notes = pd.concat([melody_df, rythm_df], axis=1)
    notes.loc[notes['silence'] == True, 'note_type'] = 'r'
    notes.loc[notes['continuation'] == True, 'note_type'] = 'l'
    notes.loc[notes['silence'] == True, 'note_val'] = 0
    notes.loc[notes['continuation'] == True, 'note_val'] = 0
    notes.loc[notes['silence'] == True, 'note_octave'] = 0
    notes.loc[notes['continuation'] == True, 'note_octave'] = 0
    notes['end'] = notes['note_duration'].cumsum()
    notes['start'] = notes['end'].shift(1).fillna(0)

    chords = pd.concat([harmonic_rythm_df, chords_df], axis=1)
    chords['chord_idx'] = np.arange(0, len(chords))
    chords['chord_end'] = chords['chord_duration'].cumsum()
    chords['chord_start'] = chords['chord_end'].shift(1).fillna(0)
    # Create chord serie
    merged = notes.merge(chords, how='cross')
    # Filter null intersection
    null_intersection = (merged['end'] <= merged['chord_start']) | (merged['start'] >= merged['chord_end'])
    merged = merged[~null_intersection]
    # Merge notes and chords and then fix durations
    merged['start_removal'] = (merged['chord_start'] - merged['start']).abs() * (
                merged['start'] < merged['chord_start'])
    merged['end_removal'] = (merged['end'] - merged['chord_end']).abs() * (merged['chord_end'] < merged['end'])
    merged['start'] += merged['start_removal']
    merged['end'] -= merged['end_removal']
    merged.loc[merged['start_removal'] > 0, 'note_type'] = 'l'
    # Add missing columns to be parsed by engine
    merged['tonality_octave'] = 0
    merged['chord_extension'] = 5
    merged['instrument'] = 'piano__0'
    merged['note_amp'] = 100
    merged['note_duration'] = merged['end'] - merged['start']
    merged = merged.sort_values('start')

    return merged
