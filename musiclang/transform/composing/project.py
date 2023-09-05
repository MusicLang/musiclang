from musiclang.write.library import *
import numpy as np

def offset_between_chords(c1, c2):
    """How much should we transpose the melody of the second chord for the s0 of c2 to be the nearest of c1's s0

    Parameters
    ----------
    c1 :
        param c2:
    c2 :
        

    Returns
    -------

    """
    from musiclang.write.constants import DEGREE_TO_SCALE_DEGREE
    offset_degrees = c2.element - c1.element

    c1_degree = c1.tonality.degree if c1.tonality is not None else 0
    c2_degree = c2.tonality.degree if c2.tonality is not None else 0
    c1_octave = c1.full_octave if c1.tonality is not None else 0
    c2_octave = c2.full_octave if c2.tonality is not None else 0
    offset_tonalities = int(np.sign(c2_degree - c1_degree) * DEGREE_TO_SCALE_DEGREE[abs(c2_degree - c1_degree)])
    offset_octave = c1_octave - c2_octave
    offset_octave_chords = c2.octave - c1.octave

    return offset_degrees + offset_tonalities + 7 * (offset_octave + offset_octave_chords)


def project_on_several_chord(score, chords):
    """

    Parameters
    ----------
    score
    chords

    Returns
    -------

    """
    from musiclang import Score
    chord, _, _, _, _ = project_on_one_chord(score)
    _, _, chords_offsets, _, _ = project_on_one_chord(chords)

    projection = chord.to_score().project_on_score(chords, keep_score=False)
    projection = Score([s & (-i) for s, i in zip(projection.chords, chords_offsets)])
    return projection

def project_on_score_keep_notes(score1, score2):
    """
    Project the score1 on the score2 keping the notes as close as possible to the original score
    For example:

    Parameters
    ----------
    score1: Score
            Score to project
    score2: Score
            Score on which to project (the resulting score will have the same chord progression)
    Returns
    -------

    """
    from musiclang import Score
    chord, _, _, _, chords = project_on_one_chord(score1)
    _, _, chords_offsets, _, _ = project_on_one_chord(score2)
    projection = chord.to_score().project_on_score(score2, voice_leading=False)
    projection = Score([s & (-i) for s, i in zip(projection.chords, chords_offsets)])
    return projection


def project_on_one_chord(score):
    """Clever projection of a score in several chords into the first chord
    :return:

    Parameters
    ----------
    score :
        

    Returns
    -------

    """
    chords = score.chords
    first_chord = chords[0]
    all_parts = list(dict.fromkeys([part for chord in score.chords for part in chord.parts]))
    idx_stops = {part: [] for part in all_parts}
    melodies = {part: None for part in all_parts}
    offsets = []
    for chord in chords:
        offset = offset_between_chords(first_chord, chord)
        offsets.append(offset)
        for part in all_parts:
            if part in chord.score.keys():
                start = idx_stops[part][-1][-1] if len(idx_stops[part]) > 0 else 0
                stop = start + chord.score[part].duration
                idx_stops[part].append((start, stop))
                melodies[part] += chord.score[part] & offset
            else:
                start = idx_stops[part][-1][-1] if len(idx_stops[part]) > 0 else 0
                stop = start + chord.duration
                idx_stops[part].append((start, stop))
                melodies[part] += Silence(chord.duration)

    chord = first_chord(**melodies)
    return chord, idx_stops, offsets, melodies, chords


def get_melody_starting_between(melody, start, stop):
    """

    Parameters
    ----------
    melody :
        
    start :
        
    stop :
        

    Returns
    -------

    """

    new_melody = None
    time = 0
    for note in melody.notes:
        if stop > time >= start:
            new_melody += note.copy()
        if time >= stop:
            break
        time += note.duration

    return new_melody

def note_duration_still_playing_at(melody, start):
    """

    Parameters
    ----------
    melody :
        
    start :
        

    Returns
    -------

    """
    result = None
    time = 0

    for note in melody.notes:
        if (time < start) and (time + note.duration > start):
            result = time + note.duration - start
            return result
        if time >= start:
            return result
        time += note.duration

    return result

def note_still_playing_at(melody, start):
    """

    Parameters
    ----------
    melody :
        
    start :
        

    Returns
    -------

    """
    time = 0
    for note in melody.notes:
        if (time < start) and (time + note.duration > start):
            result = time + note.duration - start
            to_return = note.copy()
            to_return.duration = result
            return to_return
        if time >= start:
            return None
        time += note.duration

    return None


def get_melody_between(melody, start, stop, continuation=True):
    """

    Parameters
    ----------
    melody :
        
    start :
        
    stop :
        
    continuation :
         (Default value = True)

    Returns
    -------

    """
    melody_between = get_melody_starting_between(melody, start, stop)
    if continuation:
        note_still_playing = note_duration_still_playing_at(melody, start)
        if note_still_playing is not None:
            note_still_playing = Continuation(note_still_playing)
    else:
        note_still_playing = note_still_playing_at(melody, start)

    new_melody = None

    if note_still_playing is not None:
        new_melody = note_still_playing
    if melody_between is not None:
        new_melody += melody_between.copy()
    duration = stop - start
    delta_duration = new_melody.duration - duration
    assert delta_duration >= 0, "Delta duration should be positive, error of implementation"
    assert (new_melody.notes[-1].duration - delta_duration) > 0, "Error of implementation {} {}".format(start, stop)
    new_melody.notes[-1].duration = new_melody.notes[-1].duration - delta_duration
    return new_melody



def reproject_on_multiple_chords(chords, new_chord, idx_stops, offsets, offset=True):
    """

    Parameters
    ----------
    chords :
        
    new_chord :
        
    idx_stops :
        
    offsets :
        
    offset :
         (Default value = True)

    Returns
    -------

    """
    new_score = None
    # Put everything back on same melody
    #accs = {key: 0 for key in idx_stops.keys()}
    for idx, chord in enumerate(chords):
        # Get each part of chord
        res_chord = {}
        for part in chord.parts:
            start, stop = idx_stops[part][idx]
            melody = get_melody_between(new_chord.get_part(part), start, stop)
            res_chord[part] = melody
            if offset:
                res_chord[part] = res_chord[part] & - offsets[idx]

        new_score += chord(**res_chord)

    return new_score

def parse_relative_to_absolute(melody, chord=None):
    """

    Parameters
    ----------
    melody :

    Returns
    -------

    """
    result = []
    prev = None
    idx = 0
    for note in melody.copy().notes:
        idx += 1
        if note.type in ['su', 'sd']:
            to_add = prev.add_interval(note)
            to_add.duration = note.duration
            result.append(to_add)
            prev = to_add.copy()
        elif chord is not None and note.type in ['bu', 'bd', 'cu', 'cd', 'b', 'c', 'hu', 'hd']:
            last_pitch = chord.to_pitch(prev) if prev is not None else None
            to_add = chord.parse(chord.to_pitch(note, last_pitch=last_pitch))
            to_add.duration = note.duration
            to_add.amp = note.amp
            result.append(to_add)
            prev = to_add.copy()
        elif note.type in ['s', 'a', 'd']:
            result.append(note.copy())
            prev = note.copy()
        elif note.type in ['r', 'l']:
            result.append(note.copy())
        elif note.type in ['h']:
            # FIXME : Should not convert chromatic to scale note, write a separate function for compatibility with
            # counterpoint module
            DICT_NOTES = {0: 0,
                          1: 1,
                          2: 1,
                          3: 2,
                          4: 2,
                          5: 3,
                          6: 3,
                          7: 4,
                          8: 5,
                          9: 5,
                          10: 6,
                          11: 6
                          }
            new_note = note.copy()
            new_note.type = "s"
            new_note.val = DICT_NOTES[new_note.val]
            result.append(new_note)
        else:
            raise Exception('Could not handle type in project rhythm : {}'.format(note.type))

    from musiclang import Melody
    return Melody(result)


def is_continuation(note, silence_as_continuation=True):
    """

    Parameters
    ----------
    note :
        
    silence_as_continuation :
         (Default value = True)

    Returns
    -------

    """
    if silence_as_continuation:
        return note.type == "l" or note.type == "r"
    else:
        return note.type == "l"

def is_rest(note):
    """

    Parameters
    ----------
    note :
        

    Returns
    -------

    """
    return note.type == "r"

def is_in_time(start, end, time):
    """

    Parameters
    ----------
    start :
        
    end :
        
    time :
        

    Returns
    -------

    """
    return (start <= time) and (end > time)


def project_on_rhythm(rhythm, melody, chord=None):
    """
    Given a rhythm (A Melody object) project the given melody on this rhythm

    Parameters
    ----------
    rhythm : Melody
        
    melody : Melody
        

    Returns
    -------

    """
    new_melody = None

    melody_without_relative = parse_relative_to_absolute(melody.copy(), chord)
    notes_ends = np.cumsum([note.duration for note in melody_without_relative.notes]).tolist()
    notes_starts = [0] + notes_ends[:-1]
    notes_times = [(note, start, end) for note, start, end in zip(melody_without_relative.notes, notes_starts, notes_ends)]

    time = 0
    previous_note = None

    for rhythm_note in rhythm.notes:
        # Find first note
        candidates = [note for note, start, end in notes_times if is_in_time(start, end, time)]
        if len(candidates) > 0:
            candidate = candidates[0]
            if candidate.type == 'l':
                if previous_note is None:
                    to_add = Continuation(rhythm_note.duration)
                else:
                    to_add = previous_note.copy()
                    to_add.duration = rhythm_note.duration
            elif rhythm_note.type == 'l':
                to_add = Continuation(rhythm_note.duration)
            else:
                to_add = candidate.copy()
                to_add.duration = rhythm_note.duration
            new_melody += to_add
            if to_add.type != 'l':
                previous_note = to_add.copy()
        else:
            new_melody += Silence(rhythm_note.duration)
        time = time + rhythm_note.duration

    return new_melody


def get_nearest_note(candidates, note):
    """

    Parameters
    ----------
    candidates :
        
    note :
        

    Returns
    -------

    """
    candidate_val = min(candidates, key=lambda x: abs(x.val - note.val))
    return get_nearest_val(note, candidate_val.val)

def get_nearest_val(n, new_val):
    """

    Parameters
    ----------
    n :
        
    new_val :
        

    Returns
    -------

    """
    delta_val = (new_val - n.val) % 7
    notes_candidate = [n.add_value(delta_val, 0), n.add_value(delta_val, -1), n.add_value(delta_val, 1)]
    candidate = min(notes_candidate, key=lambda x: note_distance_abs(n, x))
    return candidate


def note_distance_abs(n1, n2):
    """

    Parameters
    ----------
    n1 :
        
    n2 :
        

    Returns
    -------

    """
    return abs(n2.scale_pitch - n1.scale_pitch)


def note_distance(n1, n2):
    """

    Parameters
    ----------
    n1 :
        
    n2 :
        

    Returns
    -------

    """
    return n1.val - n2.val


def get_nearest_note_in_context(rhythm_note, note, chord, dict_notes=None):
    """

    Parameters
    ----------
    rhythm_note :
        
    note :
        
    chord :
        
    dict_notes :
         (Default value = None)

    Returns
    -------

    """
    if dict_notes is None:
        dict_notes = {}
    candidates = get_notes_candidate_in_context(rhythm_note, chord, dict_notes=dict_notes)
    if len(candidates) == 0:
        return note
    elif note.is_note:
        return get_nearest_note(candidates, note)
    else:
        return note


def get_notes_candidate_in_context(rhythm_note, chord, dict_notes=None):
    """

    Parameters
    ----------
    rhythm_note :
        
    chord :
        
    dict_notes :
         (Default value = None)

    Returns
    -------

    """
    if dict_notes is None:
        dict_notes = {}
    rhythm_note = rhythm_note.set_duration(Q)
    if rhythm_note in dict_notes.keys():
        return dict_notes[rhythm_note]
    else:
        if rhythm_note.val == CHORD_NOTE.val:
            return chord.possible_notes
        elif rhythm_note.val == SCALE_NOTE.val:
            return chord.scale_notes
        elif rhythm_note.val == TONIC.val:
            return [Note("s", 0, 0, 1)]
        elif rhythm_note.val == TONIC_OR_FIFTH.val:
            return [Note("s", 0, 0, 1), Note("s", 4, 0, 1)]
        elif rhythm_note.val == SCALE_DISSONNANCE.val:
            return chord.scale_dissonances
    return [rhythm_note]





def get_absolute_voice(voice):
    """Transform a relative melody to an absolute one

    Parameters
    ----------
    voice :
        return:

    Returns
    -------

    """
    return parse_relative_to_absolute(voice)

def get_absolute_voices(voices):
    """

    Parameters
    ----------
    voices :
        

    Returns
    -------

    """
    return [get_absolute_voice(voice) for voice in voices]