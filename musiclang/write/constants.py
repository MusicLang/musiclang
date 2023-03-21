"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

ELEMENT_TO_STR = {
    0: "I",
    1: "II",
    2: "III",
    3: "IV",
    4: "V",
    5: "VI",
    6: "VII"
}

DEGREE_TO_STR = {
    0: "I",
    1: "II.b",
    2: "II",
    3: "III.b",
    4: "III",
    5: "IV",
    6: "IV.s",
    7: "V",
    8: "VI.b",
    9: "VI",
    10: "VII.b",
    11: "VII"
}

DEGREE_TO_SCALE_DEGREE = {
    0: 0,
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

SCALE_DEGREE = {
    0: 0,
    1: 2,
    2: 4,
    3: 5,
    4: 7,
    5: 9,
    6: 11
}

from fractions import Fraction as frac

W = frac(4)
H = frac(2)
Q = frac(1)
E = frac(1) / frac(2)
S = frac(1) / frac(4)
T = frac(1) / frac(8)

W3 = (frac(2) / frac(3)) * W
H3 = (frac(2) / frac(3)) * H
Q3 = (frac(2) / frac(3)) * Q
E3 = (frac(2) / frac(3)) * E
S3 = (frac(2) / frac(3)) * S
T3 = (frac(2) / frac(3)) * T

W5 = (frac(2) / frac(5)) * W
H5 = (frac(2) / frac(5)) * H
Q5 = (frac(2) / frac(5)) * Q
E5 = (frac(2) / frac(5)) * E
S5 = (frac(2) / frac(5)) * S
T5 = (frac(2) / frac(5)) * T

Wd = W * frac(3) / frac(2)
Hd = H * frac(3) / frac(2)
Qd = Q * frac(3) / frac(2)
Ed = E * frac(3) / frac(2)
Sd = S * frac(3) / frac(2)
Td = T * frac(3) / frac(2)

STR_TO_DURATION = {
    "n": 0,
    # We let possibility for empty notes because it can be useful (eg : when projecting a melody), these should be ignored by parser
    "w": frac(4),
    "h": frac(2),
    "q": frac(1),
    "e": frac(1) / frac(2),
    "s": frac(1) / frac(4),
    "t": frac(1) / frac(8),

    "w5": frac(8) / frac(5),
    "h5": frac(4) / frac(5),
    "q5": frac(2) / frac(5),
    "e5": frac(2) / frac(10),
    "s5": frac(2) / frac(20),
    "t5": frac(2) / frac(40),

    "w7": frac(8) / frac(7),
    "h7": frac(4) / frac(7),
    "q7": frac(2) / frac(7),
    "e7": frac(2) / frac(14),
    "s7": frac(2) / frac(28),
    "t7": frac(2) / frac(56),

    "w3": frac(8) / frac(3),
    "h3": frac(4) / frac(3),
    "q3": frac(2) / frac(3),
    "e3": frac(2) / frac(6),
    "s3": frac(2) / frac(12),
    "t3": frac(2) / frac(24),

    "wd": W * frac(3) / frac(2),
    "hd": H * frac(3) / frac(2),
    "qd": Q * frac(3) / frac(2),
    "ed": E * frac(3) / frac(2),
    "sd": S * frac(3) / frac(2),
    "td": T * frac(3) / frac(2),
}

DURATION_TO_STR = {
    val: key for key, val in STR_TO_DURATION.items()
}

INDEX_MODE = {
    "M": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 2,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 4,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 5,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 7,
        (4, "s"): 8,
        (4, "b"): 6,

        (5, ""): 9,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 11,
        (6, "s"): 11,
        (6, "b"): 10,

    },

    "m": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 2,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 3,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 5,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 7,
        (4, "s"): 7,
        (4, "b"): 6,

        (5, ""): 8,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 11,
        (6, "s"): 11,
        (6, "b"): 10,
    },

    "mm": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 2,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 3,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 5,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 7,
        (4, "s"): 7,
        (4, "b"): 6,

        (5, ""): 9,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 11,
        (6, "s"): 11,
        (6, "b"): 10,
    },

    "dorian": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 2,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 3,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 5,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 7,
        (4, "s"): 7,
        (4, "b"): 6,

        (5, ""): 9,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 10,
        (6, "s"): 11,
        (6, "b"): 10,
    },

    "phrygian": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 1,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 3,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 5,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 7,
        (4, "s"): 7,
        (4, "b"): 6,

        (5, ""): 9,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 10,
        (6, "s"): 11,
        (6, "b"): 10,
    },

    "lydian": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 2,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 4,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 6,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 7,
        (4, "s"): 8,
        (4, "b"): 6,

        (5, ""): 9,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 11,
        (6, "s"): 11,
        (6, "b"): 10,

    },

    "mixolydian": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 2,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 4,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 5,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 7,
        (4, "s"): 8,
        (4, "b"): 6,

        (5, ""): 9,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 10,
        (6, "s"): 11,
        (6, "b"): 10,

    },

    "aeolian": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 2,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 3,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 5,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 7,
        (4, "s"): 7,
        (4, "b"): 6,

        (5, ""): 8,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 10,
        (6, "s"): 11,
        (6, "b"): 10,
    },

    "locrian": {
        (0, ""): 0,
        (0, "s"): 0,
        (0, "b"): 0,

        (1, ""): 1,
        (1, "s"): 2,
        (1, "b"): 1,

        (2, ""): 3,
        (2, "s"): 4,
        (2, "b"): 3,

        (3, ""): 5,
        (3, "s"): 6,
        (3, "b"): 5,

        (4, ""): 6,
        (4, "s"): 7,
        (4, "b"): 6,

        (5, ""): 8,
        (5, "s"): 9,
        (5, "b"): 8,

        (6, ""): 10,
        (6, "s"): 11,
        (6, "b"): 10,
    },

}


ACCIDENTS_TO_NOTE = {
    (0, "min"): 0,
    (0, "maj"): 0,
    (0, "natural"): 0,
    (0, "dim"): 0,
    (0, "aug"): 1,

    (1, "min"): 1,
    (1, "maj"): 2,
    (1, "natural"): 2,
    (1, "dim"): 1,
    (1, "aug"): 2,

    (2, "min"): 3,
    (2, "maj"): 4,
    (2, "natural"): 4,
    (2, "dim"): 3,
    (2, "aug"): 4,

    (3, "min"): 5,
    (3, "maj"): 5,
    (3, "natural"): 5,
    (3, "dim"): 5,
    (3, "aug"): 6,

    (4, "min"): 7,
    (4, "maj"): 7,
    (4, "natural"): 7,
    (4, "dim"): 6,
    (4, "aug"): 7,

    (5, "min"): 8,
    (5, "maj"): 9,
    (5, "natural"): 9,
    (5, "dim"): 8,
    (5, "aug"): 9,

    (6, "min"): 10,
    (6, "maj"): 11,
    (6, "natural"): 11,
    (6, "dim"): 10,
    (6, "aug"): 11,
}



def construct_index_tonality():
    """ """
    result = {}
    for mode in INDEX_MODE.keys():
        D = INDEX_MODE[mode]
        res_mode = {}
        for key, val in D.items():
            if val not in res_mode:
                res_mode[val] = key
            elif key[1] == "":
                res_mode[val] = key
        result[mode] = res_mode

        # Choose best
    return result


INDEX_TONALITY = construct_index_tonality()

SCALES = {
    "M": [0, 2, 4, 5, 7, 9, 11],
    "m": [0, 2, 3, 5, 7, 8, 11],
    "mm": [0, 2, 3, 5, 7, 9, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 9, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10]
}

SCALE_UNISSON = 0
SCALE_SECOND = 1
SCALE_THIRD = 2
SCALE_FOURTH = 3
SCALE_FIFTH = 4
SCALE_SIXTH = 5
SCALE_SEVENTH = 6
SCALE_OCTAVE = 7

INST_PIANO = 'piano'
INST_PIZZICATO = 'pizzicato'
INST_BRIGHT_PIANO = 'bright_piano'
INST_ELECTRIC_PIANO = 'electric_piano'
INST_HONKY_TONK = 'honky_tonk'
INST_ELECTRIC_PIANO_1 = 'electric_piano_1'
INST_ELECTRIC_PIANO_2 = 'electric_piano_2'
INST_HARPSICHORD = 'harpsichord'
INST_CLAVI = 'clavi'
INST_CELESTA = 'celesta'
INST_GLOCKENSPIEL = 'glockenspiel'
INST_MUSIC_BOX = 'music_box'
INST_VIBRAPHONE = 'vibraphone'
INST_MARIMBA = 'marimba'
INST_XYLOPHONE = 'xylophone'
INST_TUBULAR_BELLS = 'tubular_bells'
INST_DULCIMER = 'dulcimer'
INST_DRAWBAR_ORGAN = 'drawbar_organ'
INST_PERCUSSIVE_ORGAN = 'percussive_organ'
INST_ROCK_ORGAN = 'rock_organ'
INST_CHURCH_ORGAN = 'church_organ'
INST_REED_ORGAN = 'reed_organ'
INST_ACCORDION = 'accordion'
INST_HARMONICA = 'harmonica'
INST_TANGO_ACCORDION = 'tango_accordion'
INST_ACOUSTIC_GUITAR = 'acoustic_guitar'
INST_STEEL_GUITAR = 'steel_guitar'
INST_JAZZ_GUITAR = 'jazz_guitar'
INST_CLEAN_GUITAR = 'clean_guitar'
INST_OVERDRIVEN_GUITAR = 'overdriven_guitar'
INST_DISTORTION_GUITAR = 'distortion_guitar'
INST_HARMONIC_GUITAR = 'harmonic_guitar'
INST_ACOUSTIC_BASS = 'acoustic_bass'
INST_ELECTRIC_BASS_FINGER = 'electric_bass_finger'
INST_ELECTRIC_BASS_PICK = 'electric_bass_pick'
INST_FRETLESS_BASS = 'fretless_bass'
INST_SLAP_BASS_1 = 'slap_bass_1'
INST_SLAP_BASS_2 = 'slap_bass_2'
INST_SYNTH_BASS_1 = 'synth_bass_1'
INST_SYNTH_BASS_2 = 'synth_bass_2'
INST_VIOLIN = 'violin'
INST_VIOLA = 'viola'
INST_CELLO = 'cello'
INST_CONTRABASS = 'contrabass'
INST_TREMOLO_STRING = 'tremolo_string'
INST_HARP = 'harp'
INST_TIMPANI = 'timpani'
INST_STRING_ENSEMBLE_1 = 'string_ensemble_1'
INST_STRING_ENSEMBLE_2 = 'string_ensemble_2'
INST_SYNTH_STRING_1 = 'synth_string_1'
INST_SYNTH_STRING_2 = 'synth_string_2'
INST_CHOIR_AAHS = 'choir_aahs'
INST_CHOIR_OOHS = 'choir_oohs'
INST_SYNTH_CHOIR = 'synth_choir'
INST_ORCHESTRA_HIT = 'orchestra_hit'
INST_TRUMPET = 'trumpet'
INST_TROMBONE = 'trombone'
INST_TUBA = 'tuba'
INST_MUTED_TRUMPET = 'muted_trumpet'
INST_FRENCH_HORN = 'french_horn'
INST_BRASS_SECTION = 'brass_section'
INST_SYNTH_BRASS_1 = 'synth_brass_1'
INST_SYNTH_BRASS_2 = 'synth_brass_2'
INST_SOPRANO_SAX = 'soprano_sax'
INST_ALTO_SAX = 'alto_sax'
INST_TENOR_SAX = 'tenor_sax'
INST_BARITONE_SAX = 'baritone_sax'
INST_OBOE = 'oboe'
INST_ENGLISH_HORN = 'english_horn'
INST_BASSOON = 'bassoon'
INST_CLARINET = 'clarinet'
INST_PICCOLO = 'piccolo'
INST_FLUTE = 'flute'
INST_RECORDER = 'recorder'
INST_PAN_FLUTE = 'pan_flute'
INST_BLOWN_BOTTLE = 'blown_bottle'
INST_SHAKUHACHI = 'shakuhachi'
INST_WHISTLE = 'whistle'
INST_OCARINA = 'ocarina'
INST_SQUARE_LEAD = 'square_lead'
INST_SAWTOOTH_LEAD = 'sawtooth_lead'
INST_CALLIOPE_LEAD = 'calliope_lead'
INST_CHIFF_LEAD = 'chiff_lead'
INST_CHARANG_LEAD = 'charang_lead'
INST_VOICE_LEAD = 'voice_lead'
INST_FIFTHS_LEAD = 'fifths_lead'
INST_BASS_LEAD = 'bass_lead'
INST_PAD_NEW_AGE = 'pad_new_age'
INST_PAD_WARM = 'pad_warm'
INST_PAD_POLYSYNTH = 'pad_polysynth'
INST_PAD_CHOIR = 'pad_choir'
INST_PAD_BOWED = 'pad_bowed'
INST_PAD_METALLIC = 'pad_metallic'
INST_PAD_HALO = 'pad_halo'
INST_PAD_SWEEP = 'pad_sweep'
INST_FX_RAIN = 'fx_rain'
INST_FX_SOUNDTRACK = 'fx_soundtrack'
INST_FX_CRYSTAL = 'fx_crystal'
INST_FX_ATMOSPHERE = 'fx_atmosphere'
INST_FX_BRIGHTNESS = 'fx_brightness'
INST_FX_GLOBLINS = 'fx_globlins'
INST_FX_ECHOES = 'fx_echoes'
INST_FX_SCI_FI = 'fx_sci_fi'
INST_SITAR = 'sitar'
INST_BANJO = 'banjo'
INST_SHAMISEN = 'shamisen'
INST_KOTO = 'koto'
INST_KALIMBA = 'kalimba'
INST_BAGPIPE = 'bagpipe'
INST_FIDDLE = 'fiddle'
INST_SHANAI = 'shanai'
INST_TINKLE_BELL = 'tinkle_bell'
INST_AGOGO = 'agogo'
INST_STEEL_DRUMS = 'steel_drums'
INST_WOODBLOCK = 'woodblock'
INST_TAIKO_DRUM = 'taiko_drum'
INST_MELODIC_TOM = 'melodic_tom'
INST_SYNTH_DRUM = 'synth_drum'
INST_REVERSE_CYMBAL = 'reverse_cymbal'
INST_GUITAR_FRET_NOISE = 'guitar_fret_noise'
INST_BREATH_NOISE = 'breath_noise'
INST_SEASHORE = 'seashore'
INST_BIRD_TWEET = 'bird_tweet'
INST_TELEPHONE_RING = 'telephone_ring'
INST_HELICOPTER = 'helicopter'
INST_APPLAUSE = 'applause'
INST_GUNSHOT = 'gunshot'

OCTAVES = {
    INST_PICCOLO: 1,
    INST_FLUTE: 1,
    INST_OBOE: 0,
    INST_ENGLISH_HORN: 0,
    INST_CLARINET: 0,
    INST_BASSOON: -1,
    INST_FRENCH_HORN: -1,
    INST_TRUMPET: -1,
    INST_TROMBONE: -2,
    INST_TUBA: -2,
    INST_PIANO: -1,
    INST_VIOLIN: 1,
    INST_VIOLA: 0,
    INST_CELLO: -2,
    INST_CONTRABASS: -2,
    INST_HARP: -1,
    INST_ACOUSTIC_GUITAR: -1,
    INST_TIMPANI: -2
}
OCTAVES = {
    key: 0 for key in OCTAVES.keys()
}

ALL_INST = list(OCTAVES.keys())

PITCH = 0
OFFSET = 1
DURATION = 2
VELOCITY = 3
TRACK = 4
SILENCE = 5
CONTINUATION = 6
TEMPO = 7
PEDAL = 8

DRUMS_DICT = {
    (0, -2):  'bd',
    (1, -2): 'rs',
    (2, -2): 'sn',
    (3, -2): 'cp',
    (4, -2): 'sn2',
    (5, -2): 'bt',
    (6, -2): 'hh',
    (7, -2): 'lt',
    (8, -2): 'ch',
    (9, -2): 'mt',
    (10, -2): 'oh',
    (11, -2): 'ht'
}

_NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Fs', 'G', 'Ab', 'A', 'Bb', 'B']
def absolute_note_repr(note):
    val, oct = note.val, note.octave
    note_str = _NOTES[val % len(_NOTES)]
    oct_str = str(note.base_octave + oct + val // oct)
    return f"{note_str}{oct_str}"