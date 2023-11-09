import time

from musiclang.write.pitches.pitches_utils import get_relative_scale_value
from musiclang import Note, Melody
import numpy as np
from musiclang.library import *
from musiclang import Score
from musiclang.write.out import get_pitches, get_pitches_instruments


def get_candidate(candidates, scale, new_pitch, last_pitch, remove_wrong_writings=True):
    for candidate in candidates:
        candidate_pitch = get_relative_scale_value(candidate, last_pitch, scale)
        candidate_pitch_class = candidate_pitch % 12
        if candidate_pitch_class == new_pitch % 12:
            delta_octave = (new_pitch - candidate_pitch) // 12
            if remove_wrong_writings and (("u" in candidate.type and delta_octave < 0) or ("d" in candidate.type and delta_octave > 0)):
                continue
            return candidate.oabs(delta_octave if "u" in candidate.type else - delta_octave)


    return None


def transform_type_to_relative_note(new_type, scale, new_pitch, last_pitch):
    candidates_up = [Note(new_type + 'u', i, 0, 1) for i in range(len(scale))]
    candidates_down = [Note(new_type + 'd', i, 0, 1) for i in range(len(scale))]
    candidates = candidates_up + candidates_down
    candidate = get_candidate(candidates, scale, new_pitch, last_pitch)
    if candidate is None:
        candidate = get_candidate(candidates, scale, new_pitch, last_pitch, remove_wrong_writings=False)

    return candidate


def transform_note_to_relative_note(note, chord, last_pitch):
    new_pitch = chord.to_pitch(note)
    scale = chord.get_scale_from_type(note.type)
    result_note = transform_type_to_relative_note(note.type, scale, new_pitch, last_pitch)
    new_note = note.copy()
    new_note.type = result_note.type
    new_note.val = result_note.val
    new_note.octave = result_note.octave

    return new_note


def transform_note_to_chord_extension(note, chord):
    pitch = chord.to_pitch(note)
    pitch_class = pitch % 12
    chord_pitches = list(sorted(set(chord.chord_extension_pitches)))
    chord_pitch_classes = [c % 12 for c in chord_pitches]
    extension_val = chord_pitch_classes.index(pitch_class)
    extension_octave = (pitch - chord_pitches[extension_val]) // 12

    real_note = note.copy()
    real_note.type = 'b'
    real_note.val = extension_val
    real_note.octave = extension_octave
    return real_note


def transform_note_to_relative_note_with_chord_note(note, chord, last_pitch, voicing, idx_instrument):
    if not note.is_note:
        return note, last_pitch, voicing
    # First transform to chord extension note if possible
    chord_pitch_classes = list(sorted(set(chord.chord_extension_pitch_classes)))
    new_pitch = chord.to_pitch(note)
    pitch_class = new_pitch % 12
    start = time.time()
    if pitch_class in chord_pitch_classes:
        # Transform to chord extension note
        real_note = transform_note_to_chord_extension(note, chord)

        # If voicing is None, then attribute voicing
        if voicing is None:
            new_note = real_note.copy()
            voicing = new_note.set_duration(1).set_amp('mf')
            new_note.type = "x"
            new_note.val = idx_instrument
            new_note.octave = 0
        else:
            new_note = transform_note_to_relative_note(real_note, chord, last_pitch)

    else:  # It is not a chord extension note
        # Then transform it to relative note
        if last_pitch is None:
            last_pitch = chord.to_pitch(c0)
            base_melody = c0.n
        else:
            base_melody = None
        new_note = transform_note_to_relative_note(note, chord, last_pitch)
        new_note = base_melody + new_note
    return new_note, new_pitch, voicing


def transform_melody_to_relative(melody, chord, idx_instrument, prev_voicing=None):
    last_pitch = None
    new_melody = None
    voicing = None
    new_melody = []
    for note in melody.notes:
        new_note, last_pitch, voicing = transform_note_to_relative_note_with_chord_note(note, chord,
                                                                                        last_pitch, voicing,
                                                                                        idx_instrument)
        if isinstance(new_note, Note):
            new_melody.append(new_note)
        else:
            new_melody += new_note.notes

    new_melody = Melody(new_melody)
    if voicing is None:
        voicing = prev_voicing

    return new_melody, voicing


def exclude_instruments(chord, nb, ascending=True):
    instruments = chord.instruments
    pitches = [np.mean([chord.to_pitch(n) for n in chord.score[ins].notes if n.is_note]) for ins in instruments]
    if ascending:
        instruments = sorted(zip(instruments, pitches), key=lambda x: x[1])
    else:
        instruments = sorted(zip(instruments, pitches), key=lambda x: -x[1])
    if nb > 0:
        instruments = instruments[:-nb]
    parts = [i[0] for i in instruments]
    new_chord = chord(**{instr: item for instr, item in chord.score.items() if instr in parts})

    return new_chord, parts


def inverse_recursive_correct_octave(chord):
    """
    Transform a chord to a chord with bass pitch between -6 and 6
    Parameters
    ----------
    chord

    Returns
    -------

    """
    bass_pitch = chord.bass_pitch
    if bass_pitch > 6:
        chord = chord.o(-1)
        for voice, melody in chord.score.items():
            chord.score[voice] = melody.o(1)
        return inverse_recursive_correct_octave(chord)
    elif bass_pitch <= -6:
        chord = chord.o(1)
        for voice, melody in chord.score.items():
            chord.score[voice] = melody.o(-1)
        return inverse_recursive_correct_octave(chord)
    else:
        new_chord = chord.copy()
        return new_chord

def recursive_correct_octave(chord):
    """
    Transform chord and melodies to normalize chord octaves
    Parameters
    ----------
    chord

    Returns
    -------

    """
    bass_pitch = chord.bass_pitch
    if bass_pitch > 6:
        chord = chord.o(-1)
        for voice, melody in chord.score.items():
            chord.score[voice] = melody.o(1)
        return recursive_correct_octave(chord)
    elif bass_pitch <= -6:
        chord = chord.o(1)
        for voice, melody in chord.score.items():
            chord.score[voice] = melody.o(-1)
        return recursive_correct_octave(chord)
    else:
        new_chord = chord.copy()
        new_chord.octave = 0
        return new_chord

def transform_chord_to_relative(chord, nb_instruments_excluded=0, ascending=True):
    chord = recursive_correct_octave(chord)
    chord, parts = exclude_instruments(chord, nb_instruments_excluded, ascending=ascending)
    voicings = []
    prev_voicing = b0.o(-2)
    score_dict = {}
    instruments = [instr.split('__')[0] for instr in parts]
    nb_instruments = len(chord.score.items())
    for idx, part in enumerate(parts):
        melody = chord.score[part]
        new_melody, voicing = transform_melody_to_relative(melody, chord, idx, prev_voicing)
        voicings.append(voicing)
        prev_voicing = voicing
        score_dict[f'v__{idx}'] = new_melody

    result_score = NC(**score_dict)
    bar_duration = result_score.duration

    return result_score, voicings, instruments, bar_duration


class PatternExtractor:
    """
    Extract a pattern that can be auto reharmonized from a chord
    """

    def __init__(self, nb_excluded_instruments=0,
                 fixed_bass=True, voice_leading=True,
                 melody=False,
                 instruments=None,
                 voicing=None
                 ):
        """

        Parameters
        ----------
        nb_excluded_instruments: int
            Number of instruments to exclude from the pattern (starting from highest pitched instrument)
        fixed_bass: bool
            If True, the bass is fixed but the other instruments can be reharmonized
        voice_leading: bool
            If True, the voice leading will be optimized
        melody: bool
            If True, the pattern will extract only the melody
        instruments: list
            List of instruments to use for the pattern
        voicing
        """
        self.nb_excluded_instruments = nb_excluded_instruments
        self.fixed_bass = fixed_bass
        self.voice_leading = voice_leading
        self.instruments = instruments
        self.voicing = voicing
        self.melody = melody

    def extract(self, chord):

        if self.melody:
            result_score, voicing, instruments, bar_duration = transform_chord_to_relative(chord,
                                                                                            len(chord.score.items()) - 1,
                                                                                                ascending=False)
        else:
            start = time.time()
            result_score, voicing, instruments, bar_duration = transform_chord_to_relative(chord,
                                                                                            self.nb_excluded_instruments,
                                                                                            ascending=True)

        if self.instruments is not None:
            instruments = self.instruments[:len(instruments)] + instruments[len(self.instruments):]
        if self.voicing is not None:
            voicing = self.voicing[:len(voicing)] + voicing[len(self.voicing):]

        dict_pattern = {
            "orchestra": {
                "bar_duration": bar_duration,
                "nb_instruments": len(instruments),
                "pattern": result_score
            },
            "voicing": [note for note in voicing],
            "fixed_bass": self.fixed_bass and not self.melody,
            "voice_leading": self.voice_leading,
            "instruments": instruments
        }

        return dict_pattern

class PatternFeatureExtractor:

    """
    Extract features from a pattern dictionary.
    Returns a dictionary with the features
    """
    def __init__(self):
        pass

    def add_metadata(self, dict_pattern, chord_idx, chord, nb_excluded_instruments, melody):
        metadata = {
            "chord_idx": chord_idx,
            "chord": chord.to_chord(),
            "melody": melody,
            "degree": chord.degree,
            "tonality_degree": chord.tonality.degree,
            "extension": str(chord.extension),
            "tonality_mode": chord.tonality.mode,
            "nb_instruments": dict_pattern["orchestra"]["nb_instruments"],
            "nb_excluded_instruments": nb_excluded_instruments,
            "bar_duration": dict_pattern["orchestra"]["bar_duration"],
            "instruments": dict_pattern["instruments"]
        }

        ## ADD PROPERTIES TO DATA
        dict_pattern['metadata'] = metadata
        return dict_pattern


    def get_durations_of_notes(self, pattern):
        return [float(note.duration) for key, instr in pattern.items() for note in instr.notes if note.type not in ['l', 'r']]

    def min_pitch(self, data, score, pitches):
        min_pitch = min(pitches)
        return min_pitch

    def max_pitch(self, data, score, pitches):
        max_pitch = max(pitches)
        return max_pitch

    def average_pitch(self, data, score, pitches):
        if len(pitches) == 0:
            return 0
        average_pitch = np.mean(pitches)
        return average_pitch

    def max_leap(self, data, score, pitches_instrs):
        leaps = [np.max(np.abs(np.diff(np.asarray(pitches)))) for pitches in pitches_instrs if len(pitches) > 1]
        if len(leaps) == 0:
            return 0
        max_leap = max(leaps)

        return max_leap

    def std_leap(self, data, score, pitches_instrs):
        leaps = [np.std(np.asarray(pitches)) for pitches in pitches_instrs if len(pitches) > 1]
        if len(leaps) == 0:
            return 0
        average_leap = np.mean(leaps)
        return average_leap

    def std_duration(self, data, score):
        pattern = data['orchestra']['pattern']
        durations = self.get_durations_of_notes(pattern)
        if len(durations) < 2:
            return 0
        std_duration = np.std(durations)
        return std_duration

    def average_duration(self, data, score):
        pattern = data['orchestra']['pattern']
        durations = self.get_durations_of_notes(pattern)
        if len(durations) < 1:
            return 0
        average_duration = np.mean(durations)
        return average_duration

    def notes_per_quarter(self, data, score):
        pattern = data['orchestra']['pattern']
        area = pattern.duration
        notes = [note for key, instr in pattern.items() for note in instr.notes if note.type not in ['l', 'r']]
        nb_notes = len(notes)

        return nb_notes / area

    def notes_per_quarter_per_instrument(self, data, score):
        pattern = data['orchestra']['pattern']
        area = pattern.duration * len(pattern.items())
        notes = [note for key, instr in pattern.items() for note in instr.notes if note.type not in ['l', 'r']]
        nb_notes = len(notes)

        return nb_notes / area

    def note_density(self, data, score):
        pattern = data['orchestra']['pattern']
        area = pattern.duration * len(pattern.items())
        if area == 0:
            return 0
        notes = [note for key, instr in pattern.items() for note in instr.notes]
        note_area = sum([note.duration for note in notes if note.type not in ['l', 'r']])
        return note_area / area

    def chromatic_density(self, data, score):
        pattern = data['orchestra']['pattern']
        area = pattern.duration * len(pattern.items()) * data['metadata']['note_density']
        if area == 0:
            return 0
        notes = [note for key, instr in pattern.items() for note in instr.notes]
        chromatic_area = sum([note.duration for note in notes if note.type[0] == 'h'])
        return chromatic_area / area

    def scale_density(self, data, score):
        pattern = data['orchestra']['pattern']
        area = pattern.duration * len(pattern.items()) * data['metadata']['note_density']
        if area == 0:
            return 0
        notes = [note for key, instr in pattern.items() for note in instr.notes]
        scale_area = sum([note.duration for note in notes if note.type[0] == 's'])
        return scale_area / area

    def dissonance_density(self, data, score):
        return data['metadata']['scale_density'] + data['metadata']['chromatic_density']

    def consonance_density(self, data, score):
        return 1 - data['metadata']['dissonance_density']

    def chord_density(self, data, score, all_notes):
        pattern = data['orchestra']['pattern']
        area = pattern.duration * len(pattern.items()) * data['metadata']['note_density']
        if area == 0:
            return 0
        notes = all_notes
        chord_area = sum([note.duration for note in notes if note.type[0] in ['x', 'b']])
        return chord_area / area

    def get_features(self, data):
        pattern = data['orchestra']['pattern']
        all_notes = [note for key, instr in pattern.items() for note in instr.notes]
        score = data['orchestra']['pattern'].project_pattern(data['voicing'])
        pitches = get_pitches(score)
        pitches_instrs = get_pitches_instruments(score)

        data['metadata']['min_pitch'] = float(self.min_pitch(data, score, pitches))
        data['metadata']['max_pitch'] = float(self.max_pitch(data, score, pitches))
        data['metadata']['note_density'] = float(self.note_density(data, score))
        data['metadata']['std_duration'] = float(self.std_duration(data, score))
        data['metadata']['notes_per_quarter'] = float(self.notes_per_quarter(data, score))
        data['metadata']['notes_per_quarter_per_instrument'] = float(self.notes_per_quarter_per_instrument(data, score))
        data['metadata']['average_duration'] = float(self.average_duration(data, score))
        data['metadata']['std_leap'] = float(self.std_leap(data, score, pitches_instrs))
        data['metadata']['max_leap'] = float(self.max_leap(data, score, pitches_instrs))
        data['metadata']['average_pitch'] = float(self.average_pitch(data, score, pitches))
        data['metadata']['chromatic_density'] = float(self.chromatic_density(data, score))
        data['metadata']['scale_density'] = float(self.scale_density(data, score))
        data['metadata']['chord_density'] = float(self.chord_density(data, score, all_notes))
        data['metadata']['dissonance_density'] = float(self.dissonance_density(data, score))
        data['metadata']['consonance_density'] = float(self.consonance_density(data, score))

    def extract(self, data, chord, chord_idx=0, nb_excluded_instruments=0, melody=False):
        pattern = self.add_metadata(data,
                                    chord_idx=chord_idx,
                                    chord=chord,
                                    nb_excluded_instruments=nb_excluded_instruments,
                                    melody=melody)

        # Extract features from the score
        self.get_features(pattern)
        features = {}

        # Extract

        return pattern
