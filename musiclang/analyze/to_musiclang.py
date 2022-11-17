from madmom.io.midi import MIDIFile
from .chord_recognition import infer_chords_hierarchy, sequence_note_pitch_vectors
from .chords import convert_notes
from .utils import chord_to_pitches
from .utils_proba import get_scale_prior_matrix, get_scale_index,get_chord_index, \
    get_scale_emission_matrix, get_scale_transition_matrix, get_chord_emission_matrix
from .chord_recognition import infer_chords_for_sequence
from .inference import infer_chords_degrees
from .viterbi import logviterbi
from .voice_separation import separate_voices
from musiclang.core.out.constants import REVERSE_INSTRUMENT_DICT
from musiclang.core.note import Silence, Continuation
from musiclang.core.constants import OCTAVES
from mido import tempo2bpm
import numpy as np
import time


def _get_beat_value(mf):
    beat_value = 4/mf.time_signatures[0][2]
    return beat_value

def infer_score(sequence, chords, instruments, bar_duration_in_ticks, offset_in_ticks, tick_value):

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
        # FIXME : Make sure no overlapping instruments between tracks
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



def infer_chords(sequence, bar_duration_in_ticks, offset_in_ticks, max_chords):

    # Offset is already taken in account
    beats = [(bar_duration_in_ticks * i) for i in range(max_chords)]
    pitch_vectors = sequence_note_pitch_vectors(sequence, beats)

    emission = get_scale_emission_matrix(pitch_vectors)
    transitions = get_scale_transition_matrix()
    prior = get_scale_prior_matrix()
    scale_index = get_scale_index()

    scales = logviterbi(emission,
                        prior,
                        transitions,
                        scale_index
                        )

    chords = infer_chords_for_sequence(sequence,
                                       bar_duration_in_ticks,
                                       max_chords,
                                       key_chord_loglik=None,
                                       key_chord_transition_loglik=None,
                                       key_change_prob=0.001,
                                       chord_change_prob=0.5,
                                       chord_pitch_out_of_key_prob=0.01,
                                       chord_note_concentration=100.0,
                                       add_key_signatures=False)
    chords_degrees = infer_chords_degrees(chords, scales)
    return chords_degrees

def infer_voices_per_instruments(sequence):
    # Get all tracks
    tracks = list(set([int(s.track) for s in sequence]))
    # Separate voices for each tracks
    sequence_result = []
    for track in tracks:
        # Get notes
        notes = [s.array() for s in sequence if s.track == track]
        new_notes = separate_voices(notes)
        sequence_result += new_notes

    # Resort notes by onset
    sequence_result = list(sorted(sequence_result, key=lambda x: x.start))
    return sequence_result



"""
Utils
"""


def _parse_voice(voice_notes, chord, bar_time_start, bar_time_end, tick_value, cont):
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
            duration = note.end - note.start
            melody += _parse_note(note, duration, chord, tick_value)
        elif overlap < 0:
            melody += Silence(- overlap * tick_value)
            duration = note.end - note.start
            melody += _parse_note(note, duration, chord, tick_value)
        else:
            duration = note.end - note.start
            melody += _parse_note(note, duration, chord, tick_value)

        local_time_end = note.end
        # Find scale note
    if local_time_end < bar_time_end:
        melody += Silence((bar_time_end - local_time_end) * tick_value)
    if local_time_end > bar_time_end:
        return_cont = Continuation((local_time_end - bar_time_end) * tick_value)
        melody.notes[-1].duration -= (local_time_end - bar_time_end) * tick_value

    assert melody.duration == (bar_time_end - bar_time_start) * tick_value

    return melody, return_cont


def _parse_note(note, duration, chord, tick_value):
    value = chord.parse(note.pitch - 60)
    value = value.augment(duration)
    value.amp = note.vel
    return value.augment(tick_value)






def _infer_instruments(mf):
    channel_inst = {}
    for track in mf.tracks:
        for note in track:
            if note.type == 'program_change':
                channel_inst[note.channel] = REVERSE_INSTRUMENT_DICT[note.program]
    return channel_inst


