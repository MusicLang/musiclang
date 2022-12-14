from madmom.io.midi import MIDIFile
from .chord_recognition import infer_chords_hierarchy, sequence_note_pitch_vectors
from .chords import convert_notes
from .utils import chord_to_pitches
from .utils_proba import get_scale_prior_matrix, get_scale_index,get_chord_index, \
    get_scale_emission_matrix, get_scale_transition_matrix, get_chord_emission_matrix
from .direct_chord_estimation import get_new_chords_transition_matrix
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


def infer_score_with_chords_durations(sequence, chords, instruments):
    import time
    start_time = time.time()
    # Split each chord, instrument, voice
    time_start = 0
    time_end = 0
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
    print('OFFSET CALC : ', time.time() - start_time)
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
    print('OFFSET CHORD : ', time.time() - start_time)
    return score


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


def proba_chord_from_pitches(pitch_vector, chord):
    """
    Get a probability estimator of a chord (set of pitches) given a pitch vector
    """
    chord_pitches = - 1 * np.ones(12)
    for idx in chord:
        chord_pitches[idx] = 1 / len(chord) ** 0.4

    return np.dot(chord_pitches, pitch_vector)


def proba_chords_from_pitches(pitch_vector):
    """
    Get probas of all potential chord with this particular pitch vector
    """
    from .constants import ALL_CHORDS
    return np.asarray([proba_chord_from_pitches(pitch_vector, c) for c in ALL_CHORDS])


def top_n_most_probable(pitch_vectors, n):
    """
    Return the 3 most probables chord for each pitch vector
    """
    from .constants import ALL_CHORDS
    chords = []
    probas = []

    for i, pc in enumerate(pitch_vectors):
        probs = proba_chords_from_pitches(pc)
        sort_probs = np.argsort(-probs)[:n]
        chords.append([(ALL_CHORDS[i]) for i in sort_probs])
        probas.append([probs[i] for i in sort_probs])
    return chords, probas


def prio_best(el):
    bests = [0, 4, 3, 1, 5, 2, 6]
    return bests.index(el)

def prio_modes(el):
    if el in ['m', 'M']:
        return 0
    else:
        return 1

def find_best(chords, probas, scale, threshold=0.9):
    """
    Return first chord that matches the scale except if proba of chord > threshold
    then returns this one.

    If no chord is matching the scale and no chord over threshold, returns the most probable chord
    """
    chords_probas = [(c, p) for c, p in zip(chords, probas)]
    chords_probas = list(sorted(chords_probas, key=lambda x: (-x[1], prio_modes(x[0].tonality.mode), prio_best(x[0].element))))

    for c, p in chords_probas:
        if p > threshold:
            return c
        if c.tonality.degree == scale[0] and c.tonality.mode == scale[1]:
            return c

    return chords[0]


def assign_with_most_probable_chords(pitch_vectors, scales):
    """
    For each pitch vector and scale associated with this pitch vector
    Find the most probable chord with tonality
    Returns the chords
    """
    chordss, probass = top_n_most_probable(pitch_vectors, 3)
    result_degrees = []
    for chords, probas, scale in zip(chordss, probass, scales):
        chord_degrees = infer_chords_degrees(chords, [scale] * len(chords))
        result_degrees.append((chord_degrees, probas, scale))

    final_result = []
    for chords, probs, scale in result_degrees:
        final_result.append(find_best(chords, probs, scale))

    return final_result



def infer_chords(sequence, bar_duration_in_ticks, max_chords, **kwargs):

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

    scales_reverse = logviterbi(emission[::-1],
                        prior,
                        transitions,
                        scale_index
                        )[::-1]

    # Infer cho
    chords_degrees = assign_with_most_probable_chords(pitch_vectors, scales)
    return chords_degrees

def infer_chords_direct_method(sequence, bar_duration_in_ticks, max_chords, **kwargs):
    from .direct_chord_estimation import get_chords_transition_matrix, get_chords_emission_matrix, get_chords_prior_matrix, get_chords_index
    from musiclang.core.library import I, II, III, IV, V, VI, VII
    beats = [(bar_duration_in_ticks * i) for i in range(max_chords)]
    pitch_vectors = sequence_note_pitch_vectors(sequence, beats)

    emission = get_chords_emission_matrix(pitch_vectors, **kwargs)
    transitions = get_new_chords_transition_matrix(**kwargs)
    prior = get_chords_prior_matrix()
    index = get_chords_index()

    print('Starting Viterbi algorithm')
    chords = logviterbi(np.log(emission + 100),
                        np.log(prior),
                        np.log(transitions),
                        index
                        )

    return chords


def infer_voices_per_instruments(sequence, instruments):
    # Get all tracks
    tracks = list(set([int(s.track) for s in sequence]))
    # Separate voices for each tracks
    sequence_result = []
    # Merge tracks with same instruments together
    for track in tracks:
        # Get notes
        notes = [s.array() for s in sequence if s.track == track]
        new_notes = separate_voices(notes)
        sequence_result += new_notes

    # # Remove tracks information
    # for idx, s in enumerate(sequence_result):
    #     sequence_result[idx].track = sequence_result[idx].channel
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


