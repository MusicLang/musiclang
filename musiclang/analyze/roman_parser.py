import music21
import re

from .constants import DICT_RELATIVE_CHANGE, DICT_TONALITY, EXTENSION_REPLACER, DEGREE_REGEX



def annotation_to_musiclang(text):
    """
    Parse an annotation file or string to musiclang chords with proper durations

    Parameters
    ----------
    text: str
        Filepath or annotation to parse

    Returns
    -------
    score: Score
        MusicLang score

    """
    from .parser import chords_to_musiclang
    print(text)
    chords = analyze_roman_notation(text)
    score = chords_to_musiclang(chords)
    return score


def analyze_roman_notation(text):
    """
    Given a text or a string representing a roman annotation, extract informations

    Parameters
    ----------
    text: str
        Filepath or annotation string to parse

    Returns
    -------


    """

    text = _first_clean(text)
    analysis = music21.converter.parse(text, format="romanText")
    romans = analysis.recurse().getElementsByClass('RomanNumeral')
    chords = []

    for roman in romans:
        prim, sec, key, mode, duration = _get_roman_full(roman)
        notes = [(n.pitch.pitchClass, n.pitch.octave - 5) for n in roman.notes]
        final_degree, extension, final_key, final_mode = _analyze_one_chord(prim, sec, key, mode)
        # Use it
        chords.append([notes, duration, final_degree, extension, (final_key, final_mode)])

    return chords


def _first_clean(text):
    text = text.replace('%', 'ø')
    return text

def analyze_one_chord(figure, key, mode):
    figure = figure.replace('/4', '4').replace('/3', '').replace('/2', '').replace('/5', '5')
    res = figure.split('/')
    if len(res) == 1:
        prim, sec = res[0], None
    elif len(res) == 2:
        prim, sec = res[0], res[1]
    else:
        raise Exception(f'Issue with figure {figure}')

    return _analyze_one_chord(prim, sec, key, mode)

def _analyze_one_chord(prim, sec, key, mode):
    mode = {'major': 'M', 'minor': 'm', 'M': 'M', 'm': 'm'}[mode]
    prim = _clean(prim)
    prim = _replace_special_cases(prim)
    degree, extension = _get_degree_and_extension(prim)
    sec_degree, _ = _get_degree_and_extension(sec)
    extension = _clean_extension(extension)
    # Get the key, mode of the sec_degree
    final_degree, final_key, final_mode = _get_degree_and_tonality(sec_degree, degree, key, mode)
    return final_degree, extension, final_key, final_mode

def _replace_special_cases(prim):

    #Ge* = ivo*[b3]
    #It* = #ivo*[b3]
    #N = bII6
    #Fr = II*[bV]
    #N6 = bII6

    # if 'N6' in prim:
    #     prim = prim.replace('N6', 'bII6')
    # elif 'N' in prim:
    #     prim = prim.replace('N', 'bII6')
    if 'Ger' in prim:
        pass
    elif 'It' in prim:
        prim = 'It' + prim.replace('It', '')
    elif 'Fr' in prim:
        prim = 'Fr' + prim.replace('Fr', '')

    return prim

def _get_duration(roman):
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


def _get_roman_full(roman):
    secondary = None
    if roman.secondaryRomanNumeral is not None:
        secondary = roman.secondaryRomanNumeral.primaryFigure
    duration = _get_duration(roman)
    return roman.primaryFigure, secondary, roman.key.tonic.pitchClass, roman.key.mode, duration

def _get_degree_and_extension(data):
    if data is None:
        return None, None
    else:
        degree = DEGREE_REGEX.match(data)[0]
        extension = data.replace(degree, '')
        if degree == 'N' and extension == '':
            extension = '6'
        elif degree == "Ger" and extension == '':
            extension = '7'
        elif degree == "Ger" and extension == '6':
            extension = '65'
        elif degree == "It" and extension == '':
            extension = "7[no5]"
        elif degree == "It" and extension == '53':
            extension = "7[no5]"
        elif degree == "It" and extension == '6':
            extension = "65[no5]"
        elif degree == "It" and extension == '64':
            extension = "2[no5]"
        elif degree == "Fr" and extension == '':
            extension = "7[b5]"
        elif degree == "Fr" and extension == '6':
            extension = "65[b5]"
        elif degree == "Fr":
            extension = extension + "[b5]"
        elif degree == "It":
            extension = extension + "[no5]"
        return degree, extension


def _get_degree_and_tonality(sec_degree, degree, key, mode):

    if sec_degree is None:
        new_key, new_mode = key, mode
    else:
        key_add, new_mode = DICT_TONALITY[mode][sec_degree]
        new_key, new_mode = (key + key_add) % 12, new_mode
    degree, new_mode, key_add = DICT_RELATIVE_CHANGE[new_mode][degree]
    new_key = (new_key + key_add) % 12
    return degree, new_key, new_mode


def _clean(data):
    data = data.replace('42', '2').replace('4/3', '43').replace('/3', '').replace('/', '').replace('/4', '4')
    data = data.replace('%', 'ø')
    return data


def _clean_extension(figure):
    figure = figure.replace('[', '').replace('(', '').replace(']', '').replace(')', '')
    figure = figure.replace('66', '6').replace('67', '7').replace('62', '2').replace('643', '43')
    for key, val in EXTENSION_REPLACER:
        figure = figure.replace(key, val)
    return figure


