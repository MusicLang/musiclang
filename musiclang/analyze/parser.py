"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

"""
This file groups a set of functions to parse files into MusicLang objects
"""

def parse_to_musiclang(input_file: str, **kwargs):
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
    if extension.lower() in ['mid', 'midi']:
        return parse_midi_to_musiclang(input_file, **kwargs)
    elif extension.lower() in ['mxl', 'xml', 'musicxml', 'krn']:
        return parse_mxl_to_musiclang(input_file, **kwargs)
    else:
        raise Exception('Unknown extension {}'.format(extension))


def tokenize_midi_file(input_file, output_file, chord_range=None, quantization=16):
    import itertools
    def get_chord_range(tokens, tokenizer, start, end):
        bar_none = tokenizer['Bar_None']

        # Find first tempo token
        types = [event.type for event in tokens.events]
        # Find first Tempo event
        try:
            tempo = tokens[types.index('Tempo')]
        except Exception as e:
            tempo = None
        # Split tokens per bar_none token (like a str.split) (list to list of list)
        tokens = [list(g) for k, g in itertools.groupby(tokens, lambda x: x == bar_none) if not k]
        # Get the sublist between start and end
        tokens = tokens[start:end]
        # Add bar_none to each sublist
        tokens = [[bar_none] + t for t in tokens]
        # Flatten the list adding bar_none between each sublist
        tokens = list(itertools.chain.from_iterable(tokens))
        if tempo is not None and start > 0:
            tokens.insert(3, tempo)

        return tokens

    from miditok import REMI
    from miditok.classes import TokenizerConfig
    from miditoolkit import MidiFile

    config = TokenizerConfig(
        beat_res={(0, 8): quantization, (8, 16): quantization},
        use_tempos=True,
        use_time_signatures=True,
        one_token_stream_for_programs=True,
        use_programs=True)


    tokenizer = REMI(
        tokenizer_config=config,
    )
    #tokenizer.one_token_stream = True

    #[tokenizer.add_to_vocab(f'Position_{idx}') for idx in range(64, 256)]

    tokens = tokenizer.midi_to_tokens(MidiFile(input_file))

    if chord_range is not None:
        tokens = get_chord_range(tokens, tokenizer, *chord_range)


    midi = tokenizer.tokens_to_midi(tokens)

    # Reload for test
    midi.dump(output_file)

def parse_midi_to_musiclang(input_file: str, chord_range=None, tokenize_before=True, quantization=16, fast_chord_inference=True, **kwargs):
    """Parse a midi input file into a musiclang Score
    - Get chords with dynamic programming
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
    import time
    import os
    import shutil
    # First tokenize the midi file
    with tempfile.TemporaryDirectory() as di:
        midi_file = os.path.join(di, 'data.mid')
        if tokenize_before:
            tokenize_midi_file(input_file, midi_file, chord_range=chord_range, quantization=quantization)
        elif chord_range is None:
            shutil.copy(input_file, midi_file)
        else:
            raise Exception('Chord range must be None if tokenize_before is False')

        if not fast_chord_inference:
            mxl_file = os.path.join(di, 'data.mxl')
            obj = _m21Parse(midi_file)
            obj.write('mxl', fp=os.path.join(mxl_file))

        result = parse_directory_to_musiclang(di, fast_chord_inference=fast_chord_inference, **kwargs)
    return result


def parse_mxl_to_musiclang(input_file: str, **kwargs):
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
        obj = _m21Parse(input_file)
        obj.write('midi', fp=os.path.join(midi_file))
        shutil.copy(input_file, mxl_file)
        result = parse_directory_to_musiclang(di, **kwargs)
    return result

def parse_directory_to_musiclang(directory: str, fast_chord_inference=True, **kwargs):
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
    midi_file = os.path.join(directory, 'data.mid')
    mxl_file = os.path.join(directory, 'data.mxl')
    if not fast_chord_inference:
        from .augmented_net import infer_chords
        pprint('1/4 : Analyze the score (This may takes a while)')
        annotation_file = os.path.join(directory, 'data_annotated.rntxt')
        infer_chords(mxl_file)
        score, config = parse_midi_to_musiclang_with_annotation(midi_file, annotation_file)

    else:
        score, config = parse_midi_to_musiclang_without_annotation(midi_file)

    score = score.to_drum()
    return score, config



def parse_midi_to_musiclang_without_annotation(midi_file: str):
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

    config: dict
        Config of the score

    """
    config = {}
    score, tempo = parse_musiclang_sequence_and_chords(midi_file)

    config.update({'tempo': tempo, 'time_signature': score.config['time_signature']})
    return score, config

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

    config: dict
        Config of the score

    """


    chords = get_chords_from_analysis(annotation_file)
    config = chords.config
    score, tempo = parse_musiclang_sequence(midi_file, chords)
    config.update({'tempo': tempo})
    return score, config


# Helpers for parser


def parse_roman_numeral(element):
    print(element.primaryFigure + element.secondaryRomanNumeral.primaryFigure)

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

    figure = element.primaryFigure

    if 'N' in figure:
        key_tonic += 1
        key_mode = 'M'
    elif 'Ger' in figure:
        key_tonic += 1  # For musiclang it will be a V % II.b.M
        key_mode = 'M'
    elif 'It' in figure:
        key_tonic += 1  # For musiclang it will be a I % II.b.M
        key_mode = 'M'
    elif 'Fr' in figure:
        key_tonic += 3
        key_mode = 'mm'
    # elif 'bIII' in figure:
    #     key_tonic += 3
    #     key_mode = 'M'
    # elif 'biii' in figure:
    #     key_tonic += 3
    #     key_mode = 'm'
    # elif 'bIV' in figure:
    #     key_tonic += 4
    #     key_mode = 'M'
    # elif 'biv' in figure:
    #     key_tonic += 4
    #     key_mode = 'm'
    # elif 'bVII' in figure:
    #     key_tonic += 10
    #     key_mode = 'M'
    # elif 'bvii' in figure:
    #     key_tonic += 10
    #     key_mode = 'm'
    # elif 'bVI' in figure:
    #     key_tonic += 8
    #     key_mode = 'M'
    # elif 'bvi' in figure:
    #     key_tonic += 8
    #     key_mode = 'm'
    # elif 'bII' in figure:
    #     key_tonic += 1
    #     key_mode = 'M'
    # elif 'bii' in figure:
    #     key_tonic += 1
    #     key_mode = 'm'
    # elif 'bV' in figure:
    #     key_tonic += 6
    #     key_mode = 'M'
    # elif 'bv' in figure:
    #     key_tonic += 6
    #     key_mode = 'm'

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
    elif 'It' in element.primaryFigure:
        degree = 4
    elif 'N' in element.primaryFigure:
        degree = 0
    elif 'Fr' in element.primaryFigure:
        degree = 3
    # elif 'bIII' in element.primaryFigure:
    #     degree = 0
    # elif 'biii' in element.primaryFigure:
    #     degree = 0
    # elif 'bIV' in element.primaryFigure:
    #     degree = 0
    # elif 'biv' in element.primaryFigure:
    #     degree = 0
    # elif 'bVII' in element.primaryFigure:
    #     degree = 0
    # elif 'bvii' in element.primaryFigure:
    #     degree = 0
    # elif 'bVI' in element.primaryFigure:
    #     degree = 0
    # elif 'bvi' in element.primaryFigure:
    #     degree = 0
    # elif 'bII' in element.primaryFigure:
    #     degree = 0
    # elif 'bii' in element.primaryFigure:
    #     degree = 0
    # elif 'bV' in element.primaryFigure:
    #     degree = 0
    # elif 'bv' in element.primaryFigure:
    #     degree = 0

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



def pprint(text):
    import os
    verbose = os.getenv('VERBOSE', False)
    if verbose:
        print(text)

def parse_musiclang_sequence_and_chords(midi_file):
    """Parse a midi file into MusicLang and chords

    Parameters
    ----------
    midi_file : str
        Path to the midi file
    """
    from musiclang import Score
    from .midi_parser import parse_midi
    from .item import convert_to_items
    from .to_musiclang import infer_score_with_chords_durations
    from .chord_inference import fast_chord_inference

    pprint('1/4 : Performing voice separation (This may takes a while)')
    notes, instruments, tempo, time_signature, bars = parse_midi(midi_file)

    pprint('2/4 : Now infering chords with fast inference')
    chords = fast_chord_inference(notes, bars)
    sequence = convert_to_items(notes)
    pprint('3/4 : Create the score')
    import time
    start = time.time()
    score = infer_score_with_chords_durations(sequence, chords, instruments)
    pprint('Finished creating score in {} seconds'.format(time.time() - start))
    pprint('Finished creating score')
    pprint('4/4 Normalize the score...')
    score = score.normalize()
    score.config['time_signature'] = time_signature

    return score, tempo


def parse_musiclang_sequence(midi_file, chords):
    """Parse a midi file into MusicLang and chords with chords duration

    Parameters
    ----------
    midi_file :

    chords :


    Returns
    -------

    """
    from musiclang import Score
    from .midi_parser import parse_midi
    from .item import convert_to_items
    from .to_musiclang import infer_score_with_chords_durations


    pprint('2/4 : Performing voice separation (This may takes a while)')
    notes, instruments, tempo, time_signature, bars = parse_midi(midi_file)
    sequence = convert_to_items(notes)
    pprint('3/4 : Create the score')
    score = infer_score_with_chords_durations(sequence, chords, instruments)
    pprint('Finished creating score')
    pprint('4/4 Normalize the score...')
    score = score.normalize()

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
    from .augmented_net import infer_chords
    with tempfile.TemporaryDirectory() as di:
        mxl_file = os.path.join(di, 'data.mxl')
        annotated_file = os.path.join(di, 'data_annotated.rntxt')
        shutil.copy(input_file, mxl_file)
        infer_chords(mxl_file)
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
    from .score_formatter import ScoreFormatter
    with open(analysis, 'r') as f:
        chords = ScoreFormatter(f.read()).parse()
    return chords



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
        figure = roman.primaryFigure
        figure = figure.replace('bI', '').replace('bV', '')
        figure = figure.replace('#I', '').replace('#V', '')
        figure = figure.replace('I', '').replace('V', '')
        figure = figure.replace('bi', '').replace('bv', '')
        figure = figure.replace('#i', '').replace('#v', '')
        figure = figure.replace('i', '').replace('v', '')

        #primary_figure = roman.primaryFigure

        replacer = (
            ('M7', '[M7]'),
            ('maj7', '[M7]'),
            ('m7', '[m7]'),
            ('min7', '[m7]'),
            ('+', '(+)'),
            ('b5', '(b5)'),
            ('b7', '[m7]'),
            ('b9', '[m9]'),
            ('ar', ''),
            ('add2', '[add2]'),
            ('add4', '[add4]'),
            ('add6', '[add6]'),
            ('add9', '[add9]'),
            ('add11', '[add11]'),
            ('add13', '[add13]'),
            ('sus2', '(sus2)'),
            ('sus4', '(sus4)'),
            ('[no5]', '{-5}'),
            ('[no3]', '{-3}'),
            ('[no1]', '{-1}'),
            ('[no7]', '{-7}'),
        )

        figure = figure.replace('[', '').replace('(', '').replace(']', '').replace(')', '')
        for key, val in replacer:
            figure = figure.replace(key, val)

        chords.append([notes, duration, degree, figure, (key_tonic, key_mode)])

    return chords


def old_annotation_to_musiclang(file):
    import music21
    analysis = music21.converter.parse(file, format="romanText")
    chords = music21_roman_analysis_to_chords(analysis)
    score = chords_to_musiclang(chords)
    return score


def _m21Parse(f, fmt=None, remove_perc=True):
    """

    Parameters
    ----------
    f :

    fmt :
         (Default value = None)

    Returns
    -------

    """
    import music21
    s = music21.converter.parse(f, format=fmt, forceSource=True)
    if remove_perc:

        for el in s.recurse():
            if set(el.classes).intersection(['PercussionChord', 'Unpitched']):  # or 'Piano'
                # el.activeSite.replace(el, instrument.Violin())
                el.activeSite.remove(el)

        # perc = [
        #     p
        #     for p in s.parts
        #     if list(p.recurse().getElementsByClass(["PercussionClef", "PercussionChord"]))
        # ]
        # s.remove(perc, recurse=True)
    return s
