"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

"""
This file groups a set of functions to parse files into MusicLang objects
"""

def parse_to_musiclang(input_file: str):
    """Parse an input file into a musiclang Score
    - Get chords with the AugmentedNet (https://github.com/napulen/AugmentedNet)
    - Get voice separation and parsing

    Parameters
    ----------
    input_file : str
        Input filepath
        
    Returns
    -------
    score: musiclang.Score
        Parsed score

    config: dict
        Dict of score configuration

    """
    extension = input_file.split('.')[-1]
    if extension in ['mid', 'midi']:
        return parse_midi_to_musiclang(input_file)
    elif extension in ['mxl', 'xml', 'musicxml', 'krn']:
        return parse_mxl_to_musiclang(input_file)
    else:
        raise Exception('Unknown extension {}'.format(extension))

def parse_midi_to_musiclang(input_file: str):
    """Parse a midi input file into a musiclang Score
    - Get chords with the AugmentedNet (https://github.com/napulen/AugmentedNet)
    - Get voice separation and parsing

    Parameters
    ----------
    input_file : str
        Input midi filepath

    Returns
    -------
    score: musiclang.Score
        Parsed score

    config: dict
     Dict of score configuration

    """
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


def parse_mxl_to_musiclang(input_file: str):
    """Parse a music xml input file into a musiclang Score
    - Get chords with the AugmentedNet (https://github.com/napulen/AugmentedNet)
    - Separate into monophonic voice with the proper instrument

    Parameters
    ----------
    input_file: str :
            Filepath of the input

    Returns
    -------
    score : musiclang.Score

    config: dict
        Dict of score configuration

    """

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

def parse_directory_to_musiclang(directory: str):
    """Parse a directory containing a 'data.mid' and 'data_annotated.rntxt' file (midi file and chord annotation file)

    Parameters
    ----------
    directory : str
        Directory with a "data.mid" file and a "data_annotated.rntxt" annotation file

    Returns
    -------
    score: Score
        MusicLang score parsed

    config: dict
        Dict of score configuration

    """
    import os
    from .augmented_net import batch
    print('1/2 : Analyze the score (This may takes a while)')
    annotation_file = os.path.join(directory, 'data_annotated.rntxt')
    midi_file = os.path.join(directory, 'data.mid')
    mxl_file = os.path.join(directory, 'data.mxl')
    batch(midi_file)
    score, tempo = parse_midi_to_musiclang_with_annotation(midi_file, annotation_file)
    annotation = open(annotation_file, 'r').read()
    return score, {'annotation': annotation, 'tempo': tempo}




def parse_midi_to_musiclang_with_annotation(midi_file: str, annotation_file: str):
    """

    Parameters
    ----------
    midi_file: str :
        Filepath to the midi file to parse
        
    annotation_file: str :
        Filepath to the anotation file to parse
        

    Returns
    -------
    score: Score
        MusicLang score parsed

    tempo: int
        Tempo of the score

    """

    chords = get_chords_from_analysis(annotation_file)
    score, tempo = parse_musiclang_sequence(midi_file, chords)
    return score, tempo


# Helpers for parser


def parse_tonality(element):
    """Parse tonality as written in musicLang from Music21 object

    Parameters
    ----------
    element :
        return: key_tonic : Degree of the key (in 0-12)

    Returns
    -------
    type
        key_tonic : Degree of the key (in 0-12)

    """

    DICT_MODE = {'major': 'M', 'minor': 'm'}
    if element.secondaryRomanNumeralKey is not None:
        key_tonic = element.secondaryRomanNumeralKey.tonic.pitchClass
        key_mode = DICT_MODE[element.secondaryRomanNumeralKey.mode]
    else:
        key_tonic = element.key.tonic.pitchClass
        key_mode = DICT_MODE[element.key.mode]
    if 'N' in element.primaryFigure:
        key_tonic += 1
        key_mode = 'M'
    elif 'Ger' in element.primaryFigure:
        key_tonic += 1  # For musiclang it will be a V % II.b.M
        key_mode = 'M'
    elif 'It' in element.primaryFigure:
        key_tonic += 1  # For musiclang it will be a I % II.b.M
        key_mode = 'M'
    elif 'Fr' in element.primaryFigure:
        key_tonic += 3
        key_mode = 'mm'
    return key_tonic, key_mode


def get_degree(element):
    """Get the scale degree of an element (from Music21)

    Parameters
    ----------
    element :
        Music21 element

    Returns
    -------
    degree : int

    """
    degree = element.scaleDegree - 1
    if 'Ger' in element.primaryFigure:
        degree = 4
    if 'It' in element.primaryFigure:
        degree = 4
    elif 'N' in element.primaryFigure:
        degree = 0
    elif 'Fr' in element.primaryFigure:
        degree = 3

    return degree



def get_duration(roman):
    """Get the duration of a chord

    Parameters
    ----------
    roman :


    Returns
    -------
    type
        result, fractions.Fraction with denominator limited to 8

    """
    from fractions import Fraction as frac
    return frac(roman.duration.quarterLength).limit_denominator(8)


def parse_musiclang_sequence(midi_file, chords):
    """Parse a midi file into MusicLang and chords with chords duration

    Parameters
    ----------
    midi_file :

    chords :
        

    Returns
    -------

    """
    from .midi_parser import parse_midi
    from .item import convert_to_items
    from .to_musiclang import infer_voices_per_tracks, infer_score_with_chords_durations
    notes, instruments, tempo = parse_midi(midi_file)
    sequence = convert_to_items(notes)
    print('2/3 : Performing voice separation (This may takes a while)')
    sequence = infer_voices_per_tracks(sequence)
    print('3/3 : Create the score')
    score = infer_score_with_chords_durations(sequence, chords, instruments)
    print('Finished creating score')
    return score, tempo


def get_chords_from_mxl(input_file):
    """Given a mxl file, return a MusicLang score parsing only the chord progression

    Parameters
    ----------
    input_file : str
        MusicXML file to parse

    Returns
    -------
    score: musiclang.Score

    """
    import shutil
    import tempfile
    import os
    from .augmented_net import batch
    with tempfile.TemporaryDirectory() as di:
        mxl_file = os.path.join(di, 'data.mxl')
        annotated_file = os.path.join(di, 'data_annotated.rntxt')
        shutil.copy(input_file, mxl_file)
        batch(mxl_file)
        return get_chords_from_analysis(annotated_file)


def get_chords_from_analysis(analysis):
    """Given an analysis file (.rntxt), return a MusicLang score parsing only the chord progression

    Parameters
    ----------
    analysis : str,
        Filepath of analysis file (.rntxt) format
        

    Returns
    -------
    score: musiclang.Score

    """
    import music21
    analysis = music21.converter.parse(analysis, format="romanText")
    chords = music21_roman_analysis_to_chords(analysis)
    ml = chords_to_musiclang(chords)
    return ml



def chords_to_musiclang(chords):
    """

    Parameters
    ----------
    chords :
        

    Returns
    -------

    """
    from musiclang import Tonality, Chord, Note
    new_score = None
    for notes, duration, degree, figure, key in chords:
        key_tonic, key_mode = key
        tonality = Tonality(key_tonic, mode=key_mode)
        chord = Chord(degree, tonality=tonality, extension=figure)
        scale_notes = []
        for pitch_class, octave in notes:
            # Parse the note in musiclang
            scale_notes.append(chord.parse(pitch_class).o(octave + 1).augment(duration))

        chord_score = {f'piano__{idx}': sn for idx, sn in enumerate(scale_notes)}
        new_score += chord(**chord_score)

    return new_score


def music21_roman_analysis_to_chords(score):
    """

    Parameters
    ----------
    score :
        

    Returns
    -------

    """
    time_sig = None

    chords = []
    # Get time sigs
    romans = score.recurse().getElementsByClass('RomanNumeral')
    for roman in romans:
        key_tonic, key_mode = parse_tonality(roman)
        notes = [(n.pitch.pitchClass, n.pitch.octave - 5) for n in roman.notes]
        duration = get_duration(roman)
        degree = get_degree(roman)
        figure = roman.figuresWritten.replace('/', '')
        if figure == 'ar':
            figure = ''
        chords.append([notes, duration, degree, figure, (key_tonic, key_mode)])

    return chords
