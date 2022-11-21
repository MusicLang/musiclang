import numpy as np

from .bar_duration import BarDurationEstimator
from .item import Item


def quantize_notes(notes, bar_duration, offset):
    from fractions import Fraction as frac
    tick_value = frac(1, 8)
    tick_value_long = frac(1, 8)
    ratio = int(tick_value_long / tick_value)
    new_notes = []
    for note in notes:
        note.start = note.start - offset
        note.end = note.end - offset
        if (note.end - note.start) <= 1.5 * tick_value:
            note.start = int(note.start / tick_value)
            note.end = int(note.end / tick_value)
        else:
            note.start = ratio * int(note.start / tick_value_long)
            note.end = ratio * int(note.end / tick_value_long)

        new_notes.append(note)

    bar_duration_in_ticks = int(bar_duration / tick_value)
    offset_in_ticks = int(offset / tick_value)

    # Assert that bar duration and offset are indeed multiple of tick value
    assert bar_duration_in_ticks == bar_duration / tick_value
    assert offset_in_ticks == offset / tick_value

    return new_notes, bar_duration_in_ticks, offset_in_ticks, tick_value


def convert_notes_to_items(notes, bar_duration, offset):
    """
    Convert an array of notes into an array of Item objects that represents notes
    and quantize them
    :param notes:
    :param bar_duration:
    :param offset:
    :return:
    """
    # Quantize
    new_notes = []
    anachrusis = notes[:, 0] - offset
    if np.min(anachrusis) < 0:
        # Translate one bar
        notes[:, 0] += bar_duration
    for note in notes:
        start = note[0]
        end = start + note[2]
        vel = int(note[3])
        pitch = int(note[1])
        track = int(note[4])
        channel = int(note[5])
        new_notes.append(Item("name", start, end, vel=vel, pitch=pitch, track=track, channel=channel, voice=0))

    # Quantize notes in integer
    new_notes, bar_duration_in_ticks, offset_in_ticks, tick_value = quantize_notes(new_notes, bar_duration, offset)
    max_chords = (new_notes[-1].end // bar_duration_in_ticks) + 1
    return new_notes, bar_duration_in_ticks, offset_in_ticks, max_chords, tick_value



def convert_notes(notes):
    notes = np.asarray(notes)
    bar_duration, offset = BarDurationEstimator().estimate(notes)
    sequence, bar_duration_in_ticks, offset_in_ticks, max_chords, tick_value = convert_notes_to_items(notes, bar_duration, offset)
    return sequence, bar_duration_in_ticks, offset_in_ticks, max_chords, tick_value


