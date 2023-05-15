import numpy as np
from itertools import product
from musiclang import Chord, Tonality

TEMPLATES = [
                ('', [0, 4, 7], 1),
                ('(m3)', [0, 3, 7], 1),
                ('(m3)(b5)', [0, 3, 6], 1.0),
                ('(m3)(b5)[add6]', [0, 3, 6, 9], 1.0),
                ('(+)', [0, 4, 8], 0.8),
                ('(sus2)', [0, 2, 7], 0.9),
                ('(sus4)', [0, 5, 7], 0.9),
                ('(M7)', [0, 4, 7, 11], 0.7),
                ('(m3)(m7)', [0, 3, 7, 10], 0.7),
                ('(m3)(M7)', [0, 3, 7, 10], 0.7),
                ('(m7)', [0, 4, 7, 10], 1.0),
                ('(m3)(m7)(b5)', [0, 3, 6, 10], 0.95),
        ]

EXTENSIONS = [  '',
                '7',
                '(+)',
                '(sus2)',
                '(sus4)',
               ]
CHORD_TYPE_TO_PITCHES = {t[0]: t[1] for t in TEMPLATES}
CHORD_TYPES = np.asarray([t[0] for t in TEMPLATES])
PITCH_CLASS = np.arange(12)

CHROMA_VECTORS = [t[1] for t in TEMPLATES]
COEFFS = np.asarray([t[2] for t in TEMPLATES])
# Convert chroma_vectors into a 12xn_chords matrix with each row being the indexes of the chroma_vector
CHROMA_VECTORS_MATRIX = np.asarray([[(1.0*(i%12)) in chroma_vector for i in range(12)] for chroma_vector in CHROMA_VECTORS])
CHROMA_VECTORS_MATRIX = np.concatenate([np.roll(CHROMA_VECTORS_MATRIX, i, axis=1) for i in range(12)], axis=0)
COEFFS = np.concatenate([COEFFS for i in range(12)], axis=0)

MODES = ['M', 'm']
TONALITIES = list(range(12))
ROMAN_NUMERALS = list(range(7))

PITCHES_DICT = {(roman, tonality_root, tonality_mode, extension): Chord(roman, tonality=Tonality(tonality_root, mode=tonality_mode))[extension].chord_extension_pitch_classes
                for roman, tonality_root, tonality_mode, extension in product(ROMAN_NUMERALS, TONALITIES, MODES, EXTENSIONS)}

# Remove all augmented with minor thirds
PITCHES_DICT = {k: v for k, v in PITCHES_DICT.items() if not (k[3] == '(+)' and ((v[1] - v[0]) % 12) == 3)}
# Remove the 2, _, m, sus4
PITCHES_DICT = {k: v for k, v in PITCHES_DICT.items() if not (k[3] == '(sus4)' and k[0] == 2 and k[2] == 'm')}
# Remove the 5, _, m, sus2
PITCHES_DICT = {k: v for k, v in PITCHES_DICT.items() if not (k[3] == '(sus2)' and k[0] == 5 and k[2] == 'm')}


# Invert pitches dict to get a dict of pitch classes to potential chord types
PITCH_CLASSES_DICT = {}
for k, v in PITCHES_DICT.items():
    pitch_class = tuple(sorted(v))
    if pitch_class not in PITCH_CLASSES_DICT:
        PITCH_CLASSES_DICT[pitch_class] = []
    PITCH_CLASSES_DICT[pitch_class].append(k)