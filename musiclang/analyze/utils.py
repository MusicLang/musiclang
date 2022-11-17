from .constants import *

def chord_to_pitches(chord):
    """
    Translate chord from chord recognizer to musiclang chords
    :param chord: Chord from chord_recognition module
    :return:
    """
    if chord == NO_CHORD:
        return []
    name, chord_kind = chord.split(':')
    root = PITCH_CLASS_DICT[name]
    pitches = CHORD_KIND_PITCHES[chord_kind]
    pitches = [(pitch + root) % 12 for pitch in pitches]
    return frozenset(pitches)



def softmax(x, temperature=1.0):
    """
    Normalized Softmax function with temperature
    :param x: float, numpy array
    :param temperature: float
    :return: float, np.array
    """
    tx = x/temperature
    y = np.exp((tx - np.max(tx)))
    f_x = y / np.sum(y)
    return f_x


def find_bar_duration(notes, weights=True):
    """
    Find the most probable bar duration
    returns : bar_duration (duration of bar), offset (starting offset of bar)
    """
    notes[:, 0] = 1e-4 * np.floor(notes[:, 0] * 1e4)
    M = -2**31
    M_arg = None
    for bar_duration in [0.25, 0.5, 1, 1.5, 2, 3, 4, 6]:
        for offset in [-2, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 2]:
            if abs(offset) >= bar_duration:
                continue
            #result = get_mean_pitches_every_beat(notes, bar_duration, offset, weights=weights)
            result = get_mean_negative_cuts_every_beat(notes, bar_duration, offset)
            if result > M:
                M = result
                M_arg = bar_duration, offset

    bar_duration, offset = M_arg
    print(f'Bar duration : {bar_duration}, Offset : {offset}')
    return bar_duration, offset


def get_bar_note_density(notes, bar_duration):
    """
    Get mean number of note for specific bar duration
    """
    min_beat, max_beat = find_min_max_beat(notes)
    total_duration = max_beat - min_beat
    nb_bars = total_duration / bar_duration
    nb_notes = notes.shape[0]
    return nb_notes / nb_bars


def find_min_max_beat(notes):
    """
    Return the beat of the first and last note
    """
    min_beat, max_beat = int(np.min(notes[:, 0])), int(np.max(notes[:, 0]))
    return min_beat, max_beat



def get_mean_negative_cuts_every_beat(notes, duration, offset, tol=1e-1):
    min_beat, max_beat = find_min_max_beat(notes)
    beats = np.arange(offset, max_beat + offset + 1, duration)
    beats = beats[beats >= min_beat]
    ends = notes[:, 0] + notes[:, 2]
    starts = notes[:, 0]
    cuts_per_beats = [notes[(starts < beat - tol) & (ends > beat + tol)][:, 1].tolist()
                         for beat in beats]
    nb_cuts_per_beatss = np.asarray([len(n) for n in cuts_per_beats])
    if len(nb_cuts_per_beatss) == 0:
        return 0
    else:
        return - np.mean(nb_cuts_per_beatss)

def get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1, weights=True):
    """
    Return the mean number of pitches that are played ON specified beat period and offset with tolerance
    """

    min_beat, max_beat = find_min_max_beat(notes)
    beats = np.arange(offset, max_beat + offset + 1, duration)
    beats = beats[beats >= min_beat]
    pitches_per_beats = [notes[abs(notes[:, 0] - beat) <= tol][:, 1].tolist()
                         for beat in beats]
    nb_pitches_per_beats = np.asarray([len(n) for n in pitches_per_beats])

    if len(nb_pitches_per_beats) == 0:
        return 0
    else:
        return np.mean(nb_pitches_per_beats)