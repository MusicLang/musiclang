"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
from musiclang import Melody


def put_on_same_chord(score):
    """Take the first chord as reference,
    Put everything into the first chord preserving the note value (It will change the piece to a static harmony)

    Parameters
    ----------
    score : Score
            Input score
        

    Returns
    -------


    """
    from musiclang import Silence
    first_chord = score[0]
    instruments = score.instruments
    parts = {ins: None for ins in instruments}

    for chord in score.chords:
        duration = chord.duration
        for instrument in instruments:
            parts[instrument] += chord.score.get(instrument, Silence(duration))

    return first_chord(**parts)


def repeat_until_duration(score, duration):
    """
    Repeat the score until score last at least duration
    returns a score exactly of length duration
    Parameters
    ----------
    score
    duration

    Returns
    -------
    """
    if score.duration < duration:
        # How much time we need to repeat at least
        nb_times = int(duration / score.duration) + 1
        score = score * nb_times
    score = score.get_score_between(0, duration)
    return score

def project_on_score(score, score2, keep_score=False):
    """Project harmonically the score onto the score2
    Algorithm : For each chord of score2 : get chords that belongs to score1 and reproject on chord of score2

    Parameters
    ----------
    score : Score
            Score to project on the chords of score2
    score2 : Score
        Score that contains the harmony
    keep_score : Score (Default value = False)
        Keep the voices of score2 ? (Default value = False)

    Returns
    -------
    new_score: Score
              The score projected on score2 chord progression

    """

    start_time = 0
    new_score = None
    #
    instruments1 = [(ins.split('__')[0], int(ins.split('__')[1])) for ins in score.instruments]

    for idx, chord2 in enumerate(score2):
        # Get all segments of chord
        end_time = start_time + chord2.duration

        subscore1 = score.get_score_between(start_time, end_time)
        if subscore1 is None:
            break

        subscore = subscore1.put_on_same_chord()
        #assert subscore.duration == chord2.duration, "Wrong duration when projecting"


        if keep_score:
            chord_score = chord2.score
            chord_score.update(subscore.score)
        else:
            chord_score = subscore.score
        new_score += chord2(**chord_score)

        start_time = end_time

    return new_score



def get_melody_between(voice, start, end):
    """
    Get the melody between start and end
    Parameters
    ----------
    voice
    start
    end

    Returns
    -------

    """
    time = 0
    new_voice = []
    to_break = False
    for note in voice:
        add_continuation = False
        note_duration = note.duration
        new_note = note.copy()
        if time >= end:
            break
        if (time < start) and (time + note_duration <= start):
            time += new_note.duration
            continue
        if time + note_duration >= end:
            new_note.duration = end - time
            to_break = True
        if time < start:
            new_note.duration = new_note.duration - (start - time)
            time += start - time
            add_continuation = True

        if add_continuation:
            from ..note import Continuation
            new_voice.append(Continuation(new_note.duration))
        else:
            new_voice.append(new_note)

        if new_note.duration < 0:
            raise Exception('Get a negative duration in get_chord_between')

        time += new_note.duration

        if to_break:
            break
    new_voice = Melody(new_voice)
    return new_voice

def get_chord_between(chord, start, end, complete_if_missing=False):
    """Get the chord with melodies that are between start and end

    Parameters
    ----------
    chord :
        chord on which to extract subchord melodies
    start :
        Start time (relative to chord)
    end :
        End time (relative to chord)
    complete_if_missing :
        If True, complete the chord with silence if the chord is not complete (Default value = False)
    Returns
    -------
    type
        chord, Chord, modified chord

    """
    new_parts = {ins: None for ins in chord.instruments}
    total_duration = end - start
    for part in chord.score.keys():
        new_voice = get_melody_between(chord.score[part], start, end)
        if complete_if_missing and new_voice.duration < total_duration:
            from ..note import Silence
            new_voice += Silence(total_duration - new_voice.duration)
        new_parts[part] = new_voice
        if complete_if_missing:
            assert new_voice.duration == total_duration, f"Wrong duration {new_voice.duration} for {part}"

    if len(new_parts.keys()) == 0:
        from ..note import Silence
        return chord(**{'piano__0': Silence(end - start)})
        # if new_voice.duration != chord.duration:
        #    from pdb import set_trace; set_trace()
    return chord(**new_parts)


def get_score_between(score, start=None, end=None):
    """Get the score with melodies that are between start and end

    Parameters
    ----------
    score :
        initial score
    start :
        Start time (relative to score) (Default value = None)
    end :
        End time (relative to score) (Default value = None)

    Returns
    -------
    type
        score, Score, modified score

    """
    start = start if start is not None else 0
    end = end if end is not None else score.duration
    new_score = None
    time = 0
    for chord in score.chords:
        chord_start = time
        chord_end = time + chord.duration
        if chord_end <= start:
            time += chord.duration
            continue
        elif chord_start >= end:
            # We are already arrived at the end of time
            break
        elif chord_end < end and chord_start >= start:
            # Perfect case we just copy the full chord
            new_score += chord.copy()
        else:
            # In all other cases we have to cut the chord
            new_start = start - time
            new_end = end - time
            new_chord = score.get_chord_between(chord, new_start, new_end)
            new_score += new_chord

        time += chord.duration

    return new_score
