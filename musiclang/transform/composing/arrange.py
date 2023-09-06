
from .project import get_melody_between, project_on_rhythm, get_absolute_voice, get_nearest_note_in_context

def arrange_melody_with_chords(melody, patterns, score, inst):
    """

    Parameters
    ----------
    melody :
        
    patterns :
        
    score :
        
    inst :
        

    Returns
    -------

    """
    time = 0
    new_score = []
    for pattern, chord in zip(patterns, score.chords):
        submelody = get_melody_between(melody, time, time + pattern.duration)
        submelody = submelody & - chord.scale_degree
        submelody = modify_melody_to_be_on_chord(submelody, pattern, chord)
        new_chord = chord.copy()(**{**chord.score, inst: submelody})
        new_score.append(new_chord)
        time += pattern.duration
        assert submelody.duration == pattern.duration, "Wrong duration {} {}".format(submelody.duration, pattern.duration)
        assert new_chord.duration == pattern.duration

    from musiclang import Score
    new_score = Score(new_score)
    assert new_score.duration == sum([p.duration for p in patterns])
    return new_score


def modify_melody_to_be_on_chord(melody, rythm, chord, dict_notes=None):
    """Modify the melody to be on notes specified

    Parameters
    ----------
    rythm :
        return:
    melody :
        
    chord :
        
    dict_notes :
         (Default value = None)

    Returns
    -------

    """

    melody = get_absolute_voice(melody)
    if dict_notes is not None:
        assert all([d.duration == 1 for d in dict_notes.keys()]), "Dict notes should be quarter notes in this method"
    new_melody = []

    projected_rythm = project_on_rhythm(melody, rythm)
    for note, rythm_note in zip(melody.notes, projected_rythm.notes):
        # Get note playing at
        # get nearest dict_notes
        rythm_note = rythm_note.set_duration(1)
        new_melody.append(get_nearest_note_in_context(rythm_note, note, chord, dict_notes=dict_notes))
    from musiclang import Melody
    return Melody(new_melody)





