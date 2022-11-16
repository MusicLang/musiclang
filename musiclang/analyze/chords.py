
import numpy as np
from .item import Item

def find_bar_duration(notes):
    """
    Find the most probable bar duration
    returns : bar_duration (duration of bar), offset (starting offset of bar)
    """
    notes[:, 0] = 1e-4 * np.floor(notes[:, 0] * 1e4)
    M = 0
    M_arg = None
    for bar_duration in [0.25, 0.5, 1, 1.5, 2, 4]:
        for offset in [-2, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 2]:
            result = get_mean_pitches_every_beat(notes, bar_duration, offset)
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


def get_mean_pitches_every_beat(notes, duration, offset, tol=1e-1):
    """
    Return the mean number of pitches that are played ON specified beat period and offset
    """
    def weight(n):
        result = (120 - np.mean(n)) / 120
        if np.isnan(result):
            return 0
        return result
    min_beat, max_beat = find_min_max_beat(notes)
    pitches_per_beats = [notes[abs(notes[:, 0] - beat) < tol][:, 1].tolist()
                         for beat in np.arange(min_beat + offset, max_beat, duration)]
    nb_pitches_per_beats = np.asarray([len(n) for n in pitches_per_beats])
    weights = np.asarray([weight(n) for n in pitches_per_beats])
    sumweights = np.sum(weights)
    return np.mean(nb_pitches_per_beats)


def get_notes_with_bar(notes, bar_duration, offset):
    """
    Transform notes array in a list of array of notes with
    """
    min_beat, max_beat = find_min_max_beat(notes)
    total_duration = max_beat - min_beat
    nb_bars = int(0.5 + total_duration / bar_duration)
    time = offset
    idx = 0
    new_notes = []
    while time <= max_beat:
        new_notes.append()
        time = time + bar_duration

    return new_notes


def quantize_notes(notes, bar_duration, offset):
    from fractions import Fraction as frac
    tick_value = frac(1, 8)
    new_notes = []
    for note in notes:
        note.start = note.start - offset
        note.end = note.end - offset
        note.start = int(note.start / tick_value)
        note.end = int(note.end / tick_value)

        new_notes.append(note)

    bar_duration_in_ticks = bar_duration / tick_value
    offset_in_ticks = offset / tick_value
    return new_notes, bar_duration_in_ticks, offset_in_ticks, tick_value

def convert_notes_to_items(notes, bar_duration, offset):
    # Quantize
    new_notes = []
    for note in notes:
        start = note[0]
        end = start + note[2]
        vel = int(note[3])
        pitch = int(note[1])
        track = int(note[4])
        new_notes.append(Item("name", start, end, vel=vel, pitch=pitch, track=track))

    # Quantize notes in integer
    new_notes, bar_duration_in_ticks, offset_in_ticks, tick_value = quantize_notes(new_notes, bar_duration, offset)
    max_chords = (new_notes[-1].end // bar_duration_in_ticks) + 1
    return new_notes, bar_duration_in_ticks, offset_in_ticks, max_chords, tick_value

# Convert to items
def convert_notes(notes):
    notes = np.asarray(notes)
    bar_duration, offset = find_bar_duration(notes)

    sequence, bar_duration_in_ticks, offset_in_ticks, max_chords, tick_value = convert_notes_to_items(notes, bar_duration, offset)

    return sequence, bar_duration_in_ticks, offset_in_ticks, max_chords, tick_value


