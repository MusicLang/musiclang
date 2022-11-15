import numpy as np
from musiclang.core.chord import Chord
from musiclang.core.tonality import Tonality



def _chord_inference(pitch_set, tonality):
    scale_chord_candidates = [Chord(i, extension=extension, tonality=tonality) for
                              extension in [5, 7] for i in range(7)
                              ]
    if pitch_set == set():  # If no chord we take I of the scale
        candidates = [scale_chord_candidates[0]]
    # Find if corresponding to a scale degree
    else:
        candidates = [chord for chord in scale_chord_candidates if chord.pitch_set == pitch_set]

    if len(candidates) > 0:
        return candidates[0].copy()
    else:
        return None

def infer_chords_degrees(chords, scales):
    """
    Infer a chord (with degrees) sequence for absolute chord and scales sequence
    :param chords: list of pitch sets representing a chord (in  mod 12 algebra)
    :param scales: List of scale for each chord (root_scale in mod 12 algebra, mode in ['m', 'M', 'mm'])
    :return: List of musiclang chords
    """
    chord_degrees = []
    for chord, scale in zip(chords, scales):
        root_scale, mode_scale = scale
        tonality = Tonality(root_scale, mode=mode_scale)
        chord_candidate = _chord_inference(chord, tonality)
        if chord_candidate is not None:
            chord_degrees.append(chord_candidate)
        else:
            roots = [(root_scale + 7 * i) % 12 for i in range(0, 12)]
            modes = ['M', 'm', 'mm']
            candidates = [(root, mode) for root in roots for mode in modes]
            for troot, tmode in candidates:
                new_tone = Tonality(troot, mode=tmode)
                if new_tone.scale_set.issuperset(chord):
                    result = _chord_inference(chord, new_tone)
                    if result is not None:
                        chord_degrees.append(result)
                        break

            else:
                raise Exception(' Could not match a scale and a chord for {}'.format(chord))

    return chord_degrees