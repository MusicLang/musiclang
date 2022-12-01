
def parse_to_musiclang(input_file):
    """
    Parse an input file into a musiclang Score
    - Get chords with the AugmentedNet (https://github.com/napulen/AugmentedNet)
    - Get voice separation and parsing
    :param input_file:
    :return: musiclang.Score
    """
    extension = input_file.split('.')[-1]
    if extension in ['mid', 'midi']:
        return parse_midi_to_musiclang(input_file)
    elif extension in ['mxl', 'xml', 'musicxml', 'krn']:
        return parse_mxl_to_musiclang(input_file)
    else:
        raise Exception('Unknown extension {}'.format(extension))

def parse_midi_to_musiclang(input_file):
    import tempfile
    import os
    import music21
    import shutil
    with tempfile.TemporaryDirectory() as di:
        midi_file = os.path.join(di, 'data.mid')
        mxl_file = os.path.join(di, 'data.mxl')
        obj = music21.converter.parse(input_file, format='midi')
        obj.write('musicxml', fp=os.path.join(di, mxl_file))
        shutil.copy(input_file, midi_file)
        result = parse_directory_to_musiclang(di)
    return result


def parse_mxl_to_musiclang(input_file):
    import tempfile
    import os
    import music21
    import shutil
    with tempfile.TemporaryDirectory() as di:
        midi_file = os.path.join(di, 'data.mid')
        mxl_file = os.path.join(di, 'data.mxl')
        obj = music21.converter.parse(input_file)
        obj.write('midi', fp=os.path.join(di, midi_file))
        shutil.copy(input_file, mxl_file)
        result = parse_directory_to_musiclang(di)
    return result

def parse_directory_to_musiclang(di):
    import os
    from musiclang.augmented_net import batch
    annotation_file = os.path.join(di, 'data_annotated.rntxt')
    midi_file = os.path.join(di, 'data.mid')
    mxl_file = os.path.join(di, 'data.mxl')
    batch(midi_file)
    score, tempo = parse_midi_to_musiclang_with_annotation(midi_file, annotation_file)
    annotation = open(annotation_file, 'r').read()
    return score, {'annotation': annotation, 'tempo': tempo}

def parse_midi_to_musiclang_with_annotation(midi_file, annotation_file):
    from musiclang.parser import MidiToMusicLang
    chords = analysis_file_to_musiclang_score(annotation_file)
    midi = MidiToMusicLang(midi_file)
    score = parse_musiclang_sequence(midi, chords)
    return score, midi.score.tempo


"""
Helpers for parser
"""

def parse_tonality(element):
    DICT_MODE = {'major': 'M', 'minor': 'm'}
    if element.secondaryRomanNumeralKey is not None:
        key_tonic = element.secondaryRomanNumeralKey.tonic.pitchClass
        key_mode = DICT_MODE[element.secondaryRomanNumeralKey.mode]
    else:
        key_tonic = element.key.tonic.pitchClass
        key_mode = DICT_MODE[element.key.mode]
    return key_tonic, key_mode


def get_duration(roman):
    from fractions import Fraction as frac
    return frac(roman.duration.quarterLength).limit_denominator(8)


def parse_musiclang_sequence(midi, chords):
    from .chords import convert_to_items
    from .to_musiclang import infer_voices_per_instruments, infer_score_with_chords_durations
    notes = midi.notes
    score = midi.score
    sequence = convert_to_items(notes)
    sequence = infer_voices_per_instruments(sequence, score.instruments)
    score = infer_score_with_chords_durations(sequence, chords, score.instruments)
    return score



def analysis_to_musiclang_score(analysis):
    import music21
    analysis = music21.converter.parse(analysis, format="romanText")
    chords = music21_roman_analysis_to_chords(analysis)
    ml = chords_to_musiclang(chords)
    return ml

def analysis_file_to_musiclang_score(file):
    import music21
    analysis = music21.converter.parse(file, format="romanText")
    chords = music21_roman_analysis_to_chords(analysis)
    ml = chords_to_musiclang(chords)
    return ml


def chords_to_musiclang(chords):
    from musiclang import Tonality, Chord, Note
    new_score = None
    for notes, duration, degree, figure, key in chords:
        key_tonic, key_mode = key
        tonality = Tonality(key_tonic, mode=key_mode)
        chord = Chord(degree, tonality=tonality)
        scale_notes = []
        for pitch_class, octave in notes:
            # Parse the note in musiclang
            scale_notes.append(chord.parse(pitch_class).o(octave + 1).augment(duration))

        chord_score = {f'piano__{idx}': sn for idx, sn in enumerate(scale_notes)}
        new_score += chord(**chord_score)

    return new_score


def music21_roman_analysis_to_chords(score):
    time_sig = None

    chords = []
    # Get time sigs
    romans = score.recurse().getElementsByClass('RomanNumeral')
    for roman in romans:
        key_tonic, key_mode = parse_tonality(roman)
        notes = [(n.pitch.pitchClass, n.pitch.octave - 5) for n in roman.notes]
        duration = get_duration(roman)
        degree = roman.scaleDegree - 1
        figure = roman.figuresWritten
        chords.append([notes, duration, degree, figure, (key_tonic, key_mode)])

    return chords