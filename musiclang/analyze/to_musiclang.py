"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

from .voice_separation import separate_voices
from musiclang.write.note import Silence, Continuation
from musiclang.write.constants import OCTAVES


def infer_score_with_chords_durations(sequence, chords, instruments):
    """Get the score from a note sequence, the chords with durations and the instruments assigned to each tracks

    Parameters
    ----------
    sequence :
        param chords:
    instruments :
        return:
    chords :
        

    Returns
    -------

    """
    # Split each chords, instruments, voices
    time_start = 0
    time_end = 0
    score = None
    continuations = {}
    offsets_voices = {}  # Store the offset of voice to deduplicate voice idx between tracks
    offsets_voices_raw = {}  # Store the offset of voice to deduplicate voice idx between tracks
    tracks = list(set([s.track for s in sequence]))

    for channel, instrument in instruments.items():
        for track_idx in tracks:
            track_notes = [n for n in sequence if n.track == track_idx]
            voices = {n.voice for n in track_notes}
            offsets_voices[track_idx] = offsets_voices_raw.get(channel, 0)
            if channel not in offsets_voices_raw.keys():
                offsets_voices_raw[channel] = max(voices) + 1
            else:
                offsets_voices_raw[channel] += max(voices) + 1

    for idx, chord in enumerate(chords):
        time_start = 0 if idx == 0 else time_start + chords[idx - 1].duration
        time_end += chord.duration
        chord_notes = [n for n in sequence if time_start <= n.start < time_end]
        chord_dict = {}
        for track in tracks:
            track_notes = [n for n in chord_notes if n.track == track]
            voices = {n.voice for n in track_notes}
            for voice in voices:
                voice_notes = [n for n in track_notes if n.voice == voice]
                if len(voice_notes) > 0:
                    instrument = instruments[voice_notes[0].channel]
                    voice_name = instrument + '__' + str(offsets_voices[track] + int(voice))
                    cont = continuations.get(voice_name, None)
                    chord_dict[voice_name], cont = _parse_voice(voice_notes, chord,
                                                            time_start, time_end, 1, cont)
                    if cont is not None:
                        continuations[voice_name] = cont
                    chord_dict[voice_name] = chord_dict[voice_name].o(- OCTAVES.get(instrument, 0))

        score += chord(**chord_dict)
    return score


def infer_score(sequence, chords, instruments, bar_duration_in_ticks, offset_in_ticks, tick_value):
    """

    Parameters
    ----------
    sequence :
        
    chords :
        
    instruments :
        
    bar_duration_in_ticks :
        
    offset_in_ticks :
        
    tick_value :
        

    Returns
    -------

    """

    # Split each chord, instrument, voice
    time_start = 0
    time_end = bar_duration_in_ticks
    score = None
    continuations = {}

    # Get all track, voices
    offsets_voices = {}
    offsets_voices_raw = {}
    tracks = list(set([s.track for s in sequence]))
    for channel, instrument in instruments.items():
        for track_idx in tracks:
            track_notes = [n for n in sequence if n.track == track_idx]
            voices = {n.voice for n in track_notes}
            offsets_voices[track_idx] = offsets_voices_raw.get(channel, 0)
            if channel not in offsets_voices_raw.keys():
                offsets_voices_raw[channel] = max(voices) + 1
            else:
                offsets_voices_raw[channel] += max(voices) + 1


    for chord in chords:
        chord_notes = [n for n in sequence if time_start <= n.start < time_end]
        chord_dict = {}
        for track in tracks:
            track_notes = [n for n in chord_notes if n.track == track]
            voices = {n.voice for n in track_notes}
            for voice in voices:
                voice_notes = [n for n in track_notes if n.voice == voice]
                if len(voice_notes) > 0:
                    instrument = instruments[voice_notes[0].channel]
                    voice_name = instrument + '__' + str(offsets_voices[track] + int(voice))
                    cont = continuations.get(voice_name, None)
                    chord_dict[voice_name], cont = _parse_voice(voice_notes, chord,
                                                            time_start, time_end, tick_value, cont)
                    if cont is not None:
                        continuations[voice_name] = cont
                    chord_dict[voice_name] = chord_dict[voice_name].o(- OCTAVES.get(instrument, 0))


        score += chord(**chord_dict)
        time_start += bar_duration_in_ticks
        time_end += bar_duration_in_ticks

    return score



def infer_voices_per_tracks(sequence):
    """Separate voices of each tracks

    Parameters
    ----------
    sequence :
        return: sequence_result: New sequence with assigned "voice" property

    Returns
    -------
    type
        sequence_result: New sequence with assigned "voice" property

    """
    # Get all tracks
    tracks = list(set([int(s.track) for s in sequence]))
    # Separate voices for each tracks
    sequence_result = []
    for track in tracks:
        # Get notes
        notes = [s.array() for s in sequence if s.track == track]
        new_notes = separate_voices(notes)
        sequence_result += new_notes

    sequence_result = list(sorted(sequence_result, key=lambda x: x.start))
    return sequence_result


"""
Utils
"""


def _parse_voice(voice_notes, chord, bar_time_start, bar_time_end, tick_value, cont):
    """Parse a single voice to a musicLang melody between start time and end time

    Parameters
    ----------
    voice_notes :
        list of notes from sequence that represents a voice
    chord :
        chord on which to parse the melody (to get the references pitches)
    bar_time_start :
        Time start
    bar_time_end :
        Time end
    tick_value :
        Unit of time
    cont :
        Is there a continuation to take in account and to add to melody

    Returns
    -------
    type
        melody : musiclang.Melody : parsed melody,

    """
    def _parse_note(note, duration, chord, tick_value):
        """

        Parameters
        ----------
        note :
            
        duration :
            
        chord :
            
        tick_value :
            

        Returns
        -------

        """
        value = chord.parse(note.pitch - 60)
        value = value.augment(duration)
        value.amp = note.vel
        return value.augment(tick_value)

    melody = None
    return_cont = None
    local_time_end = voice_notes[0].start
    if cont is not None:
        melody += cont
        local_time_end = bar_time_start + (cont.duration / tick_value)

    elif local_time_end > bar_time_start:
        melody += Silence((local_time_end - bar_time_start) * tick_value)

    for note in voice_notes:
        overlap = local_time_end - note.start
        if overlap > 0:
            melody.notes[-1].duration -= overlap * tick_value
            if melody.notes[-1].duration == 0:
                melody.notes.pop()
            duration = note.end - note.start
            melody += _parse_note(note, duration, chord, tick_value)
        elif overlap < 0:
            melody += Silence(- overlap * tick_value)
            duration = note.end - note.start
            if duration > 0:
                melody += _parse_note(note, duration, chord, tick_value)
        else:
            duration = note.end - note.start
            if duration > 0:
                melody += _parse_note(note, duration, chord, tick_value)

        local_time_end = note.end
        # Find scale note
    if local_time_end < bar_time_end:
        melody += Silence((bar_time_end - local_time_end) * tick_value)
    if local_time_end > bar_time_end:
        return_cont = Continuation((local_time_end - bar_time_end) * tick_value)
        melody.notes[-1].duration -= (local_time_end - bar_time_end) * tick_value
        if melody.notes[-1].duration == 0:
            melody.notes.pop()

    assert melody.duration == (bar_time_end - bar_time_start) * tick_value

    return melody, return_cont




