from .project import project_on_rhythm, project_on_one_chord,\
    get_absolute_voices, reproject_on_multiple_chords, get_absolute_voice
import numpy as np


def create_counterpoint(fixed_voices, voices):
    """
    Create a counterpoint given a list of fixed voices and voices to adapt.
    You should provide all the melodies, the counterpoint only mutate existing voices to fit best the fixed voices.
    It tries to maximize a score, greedily, note per note and voice per voice. This score uses the following rules :

    - No consecutives fifths or octaves or unissons
    - No hidden fifths or octaves
    - No parallel dissonnances
    - No triton (s3 and s6)
    - Try to avoid moving a note too far appart


    Parameters
    ----------
    fixed_voices : list[Melody]
                   Voices that serves as cantus firmus
        
    voices :  list[Melody]
              Voices that will be modified to fit the cantus firmus.
              Only the notes will be changed, never the rythm.
        

    Returns
    -------
    result: list[Melody] shape of voices
            The counterpointed voices

    """

    # Convert fixed_voices in absolute
    fixed_voices = get_absolute_voices(fixed_voices)

    # The list of subjects that will grow with each corrected voice
    melody_subjects = fixed_voices

    result = []
    for voice in voices:
        # Remove absolute, Project all on rythm
        voice = get_absolute_voice(voice)
        subjects = get_projections_on_voice(melody_subjects, voice)
        voice_to_fix = get_array(voice)
        fixed_voice = get_counterpoint(subjects, voice_to_fix)
        melody_fixed = convert_array_to_melody(voice, fixed_voice)
        melody_subjects.append(melody_fixed)
        result.append(melody_fixed)
        # Convert back to melody

    return result


def create_counterpoint_on_score(score, fixed_parts, counterpoint_parts=None):
    """
    Create a counterpoint on parts for a score
    - Put everything on the same chord
    - Call :func:`~create_counterpoint` on melodies
    - Put everything back in the original chord progression

    You should provide all the melodies, the counterpoint only mutate existing voices to fit best the fixed voices.
    It tries to maximize a score, greedily, note per note and voice per voice. This score uses the following rules :

    - No consecutives fifths or octaves or unissons
    - No hidden fifths or octaves
    - No parallel dissonnances
    - No triton (s3 and s6)
    - Try to avoid moving a note too far appart

    Parameters
    ----------
    score: Score
    fixed_parts: list[str]
    Name of parts that are fixed  (eg: piano__0)
    counterpoint_parts: list[str] or None
        Name of parts that will move (eg: piano__1)
        If None, all the remaining voices will be applied a counterpoint on the fixed_parts

    Returns
    -------
    score: Score
           Resulting score

    """
    from musiclang import Score
    if counterpoint_parts is None:
        counterpoint_parts = set(score.instruments) - set(fixed_parts)

    # Deal with bass and chord notes
    chord, _, chords_offsets, _, chords = project_on_one_chord(score)
    fixed_voices = [chord.score[part] for part in fixed_parts]
    moving_voices = [chord.score[part] for part in counterpoint_parts]
    moving_voices = create_counterpoint(fixed_voices, moving_voices)
    for voice, part in zip(moving_voices, counterpoint_parts):
        chord.score[part] = voice
    projection = chord.to_score().project_on_score(score)
    return projection


def create_counterpoint_on_chord(chord, subject_parts, counterpoint_parts):
    """

    Parameters
    ----------
    chord :
        
    subject_parts :
        
    counterpoint_parts :
        

    Returns
    -------

    """
    fixed_voices = [chord.score[chord.parts[idx]] for idx in subject_parts]
    voices = [chord.score[chord.parts[idx]] for idx in counterpoint_parts]
    new_voices = create_counterpoint(fixed_voices, voices)
    return chord(**{**chord.score, **{chord.parts[idx]: voice for idx, voice in zip(counterpoint_parts, new_voices)}})



def get_array_fixed(voice):
    """

    Parameters
    ----------
    voice :
        

    Returns
    -------

    """
    prev = None
    res = []
    for n in voice.notes:
        if n.is_note:
            prev = n.val + 7 * n.octave
            res.append(prev)
        elif n.is_silence:
            res.append(None)
        elif n.is_continuation:
            res.append(prev)
    return res

def get_array(voice):
    """

    Parameters
    ----------
    voice :
        

    Returns
    -------

    """
    return [n.val + 7 * n.octave if n.is_note else None for n in voice.notes]

def get_projections_on_voice(voices, reference):
    """Project all voices on rythm given by reference
    and convert it to array of values

    Parameters
    ----------
    voices :
        param reference:
    reference :
        

    Returns
    -------

    """
    return [get_array_fixed(project_on_rhythm(reference, voice)) for voice in voices]


AUTHORIZED_INTERVALS = [0, 2, 3, 4, 5]
FORBIDDEN_PARALLELS = [0, 4, 3, 7]


def get_future_delta(delta):
    """Explore around (0, 1, -1, 2, -2, etc ...)

    Parameters
    ----------
    delta :
        return:

    Returns
    -------

    """
    if delta == 0:
        return 1
    elif delta > 0:
        return -delta
    else:
        return -delta + 1

def get_delta_list():
    """ """
    deltas = [0, 1, -1, 2, -2, 3, -3, 4, -4]
    #deltas = [0, 1, -2, 2, -2]
    np.random.shuffle(deltas)
    return deltas

def is_dissonnance(n1, n2):
    """

    Parameters
    ----------
    n1 :
        
    n2 :
        

    Returns
    -------

    """
    return interval(n1, n2) not in AUTHORIZED_INTERVALS

def is_forbidden_parallel(last_interval, subject, candidate):
    """

    Parameters
    ----------
    last_interval :
        
    subject :
        
    candidate :
        

    Returns
    -------

    """
    new_interval = interval(subject, candidate)
    return new_interval in FORBIDDEN_PARALLELS and last_interval == new_interval

def is_parallel_dissonnance(last_interval, subject, candidate):
    """

    Parameters
    ----------
    last_interval :
        
    subject :
        
    candidate :
        

    Returns
    -------

    """
    return is_dissonnance(subject, candidate) and last_interval not in AUTHORIZED_INTERVALS


def nb_forbidden_parallel(last_intervals, subject_notes, candidate):
    """

    Parameters
    ----------
    last_intervals :
        
    subject_notes :
        
    candidate :
        

    Returns
    -------

    """
    count = 0
    for s, inter in zip(subject_notes, last_intervals):
        if s is None:
            continue
        elif inter is None:
            continue
        elif is_forbidden_parallel(inter, s, candidate):
            count += 1
    return count

def nb_parallel_dissonnances(last_intervals, subject_notes, candidate):
    """

    Parameters
    ----------
    last_intervals :
        
    subject_notes :
        
    candidate :
        

    Returns
    -------

    """
    count = 0
    for s, inter in zip(subject_notes, last_intervals):
        if s is None:
            continue
        elif inter is None:
            continue
        elif is_parallel_dissonnance(inter, s, candidate):
            count += 1
    return count



def is_triton(candidate, subject_note):
    """

    Parameters
    ----------
    candidate :
        
    subject_note :
        

    Returns
    -------

    """
    return {candidate % 7, subject_note % 7} == {3, 6}

def scorer(subject_notes, note, delta, last_intervals, last_notes):
    """

    Parameters
    ----------
    subject_notes :
        
    note :
        
    delta :
        
    last_intervals :
        

    Returns
    -------

    """

    not_silenced_subject_notes = [s for s in subject_notes if s is not None]
    candidate = note + delta
    NB_DISSONNANCES = sum([1 * is_dissonnance(candidate, s) for s in not_silenced_subject_notes])
    NB_FORBIDDEN_PARALLELS = nb_forbidden_parallel(last_intervals[-1], subject_notes, candidate)
    NB_PARALLEL_DISSONNANCES = nb_parallel_dissonnances(last_intervals[-1], subject_notes, candidate)
    NB_TRITON = sum([1 * is_triton(candidate, s) for s in not_silenced_subject_notes])
    DISTANCE = abs(delta)
    LAST_NOTE_SAME = 1.0 * (candidate == last_notes[-1]) if len(last_notes) > 0 else 0.0
    score = 10 - 3.0 * NB_DISSONNANCES
    score += - 2.0 * NB_TRITON
    score += - 4 * NB_FORBIDDEN_PARALLELS - 4 * NB_PARALLEL_DISSONNANCES - 0.5 * DISTANCE
    score += - 2.0 * LAST_NOTE_SAME
    return score

def get_counterpoint_for_one_note(subjects_notes, note, last_intervals, last_notes, delta=0):
    """

    Parameters
    ----------
    subjects_notes :
        
    note :
        
    last_intervals :
        
    delta :
         (Default value = 0)

    Returns
    -------

    """

    deltas = get_delta_list()
    scores = [scorer(subjects_notes, note, delta, last_intervals, last_notes) for delta in deltas]
    max_score, max_score_idx = np.max(scores), np.argmax(scores)
    best_delta = deltas[max_score_idx]

    chosen_candidate = note + best_delta
    assert len(subjects_notes) == len(last_intervals[-1]), "{} {}".format(len(subjects_notes), len(last_intervals[-1]))
    last_intervals.append([interval(s, chosen_candidate, replace=old_inter) for s, old_inter in zip(subjects_notes, last_intervals[-1])])
    return chosen_candidate, last_intervals, max_score



def interval(n1, n2, replace=None):
    """

    Parameters
    ----------
    n1 :
        
    n2 :
        
    replace :
         (Default value = None)

    Returns
    -------

    """
    if n1 is None or n2 is None:
        if replace:
            return replace
        return None
    return abs(n2 - n1) % 7


def clear_list_intervals(intervals):
    """

    Parameters
    ----------
    intervals :
        

    Returns
    -------

    """
    if len(intervals) > 0:
        return intervals[-3:]
    return intervals


def get_counterpoint(subjects, to_fix):
    """Given a list of subjects modify the voice to best fit a counterpoint

    Parameters
    ----------
    fixed_voices :
        param voice:
    subjects :
        
    to_fix :
        

    Returns
    -------

    """
    subjects = np.asarray(subjects)
    last_intervals = [[None for s in subjects]]
    result = []
    total_score = 0
    last_notes = []
    for i, n in enumerate(to_fix):
        if n is None:
            result.append(None)
        else:
            new_note, last_intervals, max_score = get_counterpoint_for_one_note(subjects[:, i].tolist(), n, last_intervals, last_notes)
            result.append(new_note)
            total_score += max_score
            last_notes.append(new_note)

        last_intervals = clear_list_intervals(last_intervals)

    return result


def convert_array_to_melody(rythm, notes):
    """

    Parameters
    ----------
    rythm :
        
    notes :
        

    Returns
    -------

    """
    new_melody = None
    for idx, note in enumerate(rythm.notes):
        to_add = note.copy()
        if note.is_note:
            to_add.val = 0
            to_add.type = "s"
            to_add.octave = 0
            to_add.octave = notes[idx] // 7
            to_add.val = notes[idx] % 7

        new_melody += to_add

    return new_melody

