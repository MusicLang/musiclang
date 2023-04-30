from fractions import Fraction as frac
import musiclang.library as L

def realize_tags(note, last_note=None, next_note=None):
    """
    Given the tags of a given note returns a new melody with the realized tags
    Parameters
    ----------
    note
    last_note
    next_note

    Returns
    -------

    """
    import musiclang.library as L
    new_note = note.copy()
    duration = note.duration
    if 'accent' in note.tags:
        new_note = accent(new_note, last_note, next_note)

    if 'mordant' in note.tags:
        new_note = mordant(new_note, last_note, next_note)

    if 'inv_mordant' in note.tags:
        new_note = inv_mordant(new_note, last_note, next_note)

    if 'chroma_mordant' in note.tags:
        new_note = chroma_mordant(new_note, last_note, next_note)


    if 'inv_chroma_mordant' in note.tags:
         new_note = inv_chroma_mordant(new_note, last_note, next_note)

    if 'grupetto' in note.tags:
        new_note = grupetto(new_note, last_note, next_note)

    if 'inv_grupetto' in note.tags:
        new_note = inv_grupetto(new_note, last_note, next_note)

    if 'chroma_grupetto' in note.tags:
        new_note = chroma_grupetto(new_note, last_note, next_note)

    if 'inv_chroma_grupetto' in note.tags:
        new_note = inv_chroma_grupetto(new_note, last_note, next_note)

    if 'roll' in note.tags:
        new_note = roll(new_note, last_note, next_note)

    if 'roll_fast' in note.tags:
        new_note = roll_fast(new_note, last_note, next_note)

    if 'suspension_prev' in note.tags:
        new_note = suspension(new_note, last_note, next_note)

    if 'suspension_prev_repeat' in note.tags:
        new_note = suspension_prev_repeat(new_note, last_note, next_note)

    if 'retarded' in note.tags:
        new_note = retarded(new_note, last_note, next_note)


    if 'interpolate' in note.tags:
        new_note = interpolate(new_note, last_note, next_note)

    assert new_note.duration == note.duration, f"{new_note} {new_note.duration} {note.duration} {note.tags}"
    new_note = new_note.clear_note_tags()
    return new_note



def accent(new_note, last_note, next_note):
    new_note.amp = min(120, new_note.amp + 10)
    return new_note

def mordant(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(1, 4)
    if duration >= frac(1, 2):
        new_note = new_note.set_duration(mordant_duration) + L.su1.set_duration(
            mordant_duration) + new_note.set_duration(new_note.duration - 2 * mordant_duration)
    return new_note

def inv_mordant(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(1, 4)
    if duration >= frac(1, 2):
        new_note = new_note.set_duration(mordant_duration) + L.sd1.set_duration(
            mordant_duration) + new_note.set_duration(new_note.duration - 2 * mordant_duration)
    return new_note


def chroma_mordant(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(1, 4)
    if duration >= frac(1, 2):
        new_note = new_note.set_duration(mordant_duration) + L.hu1.set_duration(
            mordant_duration) + new_note.set_duration(new_note.duration - 2 * mordant_duration)
    return new_note

def inv_chroma_mordant(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(1, 4)
    if duration >= frac(1, 2):
        new_note = new_note.set_duration(mordant_duration) + L.hd1.set_duration(
            mordant_duration) + new_note.set_duration(new_note.duration - 2 * mordant_duration)
    return new_note


def grupetto(new_note, last_note, next_note):
    duration = new_note.duration
    if duration >= frac(1):
        mordant_duration = frac(1, 2)
        new_note = new_note.n + L.su1.set_duration(mordant_duration) + new_note.set_duration(mordant_duration) \
                   + L.sd1.set_duration(mordant_duration) + L.su1.set_duration(duration - 3 * mordant_duration)
    elif duration >= frac(1, 2):
        mordant_duration = frac(2, 3) * frac(1, 4)
        new_note = new_note.n + L.su1.set_duration(mordant_duration) + new_note.set_duration(mordant_duration) \
                   + L.sd1.set_duration(mordant_duration) + L.su1.set_duration(duration - 3 * mordant_duration)
    return new_note

def inv_grupetto(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(2, 3) * frac(1, 4)
    if duration >= frac(1, 2):
        new_note = new_note.n + L.sd1.set_duration(mordant_duration) + new_note.set_duration(mordant_duration) \
                   + L.su1.set_duration(mordant_duration) + L.sd1.set_duration(duration - 3 * mordant_duration)

    return new_note

def chroma_grupetto(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(2, 3) * frac(1, 4)
    if duration >= frac(1, 2):
        new_note = new_note.n + L.hu1.set_duration(mordant_duration) + new_note.set_duration(mordant_duration) \
                   + L.hd1.set_duration(mordant_duration) + L.hu1.set_duration(duration - 3 * mordant_duration)
    return new_note


def inv_chroma_grupetto(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(2, 3) * frac(1, 4)
    if duration >= frac(1, 2):
        new_note = new_note.n + L.hd1.set_duration(mordant_duration) + new_note.set_duration(mordant_duration) \
                   + L.hu1.set_duration(mordant_duration) + L.hd1.set_duration(duration - 3 * mordant_duration)

    return new_note


def roll(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(1, 4)
    nb_rolls = int(duration / mordant_duration)
    melody = None
    for i in range(nb_rolls):
        if (i % 2) == 0:
            melody += new_note.set_duration(mordant_duration)
        else:
            melody += L.su1.set_duration(mordant_duration)

    if nb_rolls != (duration / mordant_duration):
        melody += L.l(duration - nb_rolls * mordant_duration)
    new_note = melody

    return new_note

def roll_fast(new_note, last_note, next_note):
    duration = new_note.duration
    mordant_duration = frac(1, 6)
    nb_rolls = int(duration / mordant_duration)
    melody = None
    for i in range(nb_rolls):
        if (i % 2) == 0:
            melody += new_note.set_duration(mordant_duration)
        else:
            melody += L.su1.set_duration(mordant_duration)

    if nb_rolls != (duration / mordant_duration):
        melody += L.l(duration - nb_rolls * mordant_duration)
    new_note = melody
    return new_note


def suspension(new_note, last_note, next_note):
    duration = new_note.duration
    if last_note:
        new_note = L.l.set_duration(duration / 2) + new_note.set_duration(duration / 2)

    return new_note


def suspension_prev_repeat(new_note, last_note, next_note):
    duration = new_note.duration
    if last_note:
        new_note = last_note.set_duration(duration / 2) + new_note.set_duration(duration / 2)

    return new_note

def retarded(new_note, last_note, next_note):
    duration = new_note.duration
    retarded_duration = frac(1, 12)
    new_note = L.l.set_duration(retarded_duration) + new_note.set_duration(duration - retarded_duration)
    return new_note


def interpolate(new_note, last_note, next_note):
    """
    Interpolate note of the scale between current note and next_note
    Parameters
    ----------
    new_note: Current note to modify
    last_note: Previous note in the melody
    next_note: Next note in the melody

    Returns
    -------

    """
    from musiclang import Note
    if next_note is None or not next_note.is_note or not new_note.is_note:
        return new_note
    
    first_val = new_note.val if new_note.type == 's' else int(7 * new_note.val/12)
    first_val += 7 * new_note.octave
    second_val = next_note.val if next_note.type == 's' else int(7 * next_note.val / 12)
    second_val += 7 * next_note.octave
    delta_scale = second_val - first_val
    if delta_scale == 0:
        return new_note
    duration = frac(new_note.duration, int(abs(delta_scale)))

    up = delta_scale > 0
    temp_note = L.su1.set_duration(duration) if up else L.sd1.set_duration(duration)
    melody = None
    for i in range(first_val, second_val, 1 if up else -1):
        if i == first_val:
            melody += new_note.set_duration(duration)
        else:

            melody += temp_note
    melody =  melody.set_amp(new_note.amp)
    return melody
