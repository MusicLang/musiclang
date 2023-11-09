import music21
import re
import numpy as np
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
    figure = figure.replace('/o', 'ø').replace('4/3', '43')
    figure = figure.replace('/4', '4').replace('/3', '').replace('/2', '').replace('/5', '5')
    if mode == 'major':
        figure = figure.replace('III+', 'III(+)')

    res = figure.split('/')
    if len(res) == 1:
        prim, sec, ter = res[0], None, None
    elif len(res) == 2:
        prim, sec, ter = res[0], res[1], None
    elif len(res) == 3:
        prim, sec, ter = res[0], res[1], res[2]
    else:
        raise Exception(f'Issue with figure {figure}')

    return _analyze_one_chord(prim, sec, ter, key, mode)

def _analyze_one_chord(prim, sec, ter, key, mode):
    mode = {'major': 'M', 'minor': 'm', 'M': 'M', 'm': 'm'}[mode]
    prim = _clean(prim)
    prim = _replace_special_cases(prim)
    degree, extension = _get_degree_and_extension(prim)
    sec_degree, _ = _get_degree_and_extension(sec)
    ter_degree, _ = _get_degree_and_extension(ter)
    extension = _clean_extension(extension)
    # Get the key, mode of the sec_degree
    final_degree, final_key, final_mode = _get_degree_and_tonality(sec_degree, ter_degree, degree, key, mode)
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


from musiclang.analyze.constants import DICT_TONALITY_REVERSE

TONALITY_DICT = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11
}


def get_relative_tone(first_degree, first_mode, current_degree, current_mode):
    delta_degree = (current_degree - first_degree) % 12
    figure = DICT_TONALITY_REVERSE[first_mode][delta_degree, current_mode]
    return figure


def convert_harmony(harmony, get_features=False):
    """
    Convert harmony to relative modulations (Using ternary "/" modulations instead of named modulation).
    That way the harmony does not modulate through the piece.

    Parameters
    ----------
    harmony: str
        Harmony to convert

    Returns
    -------
    new_harmony: str

    """
    lines = harmony.split('\n')
    new_harmony = []
    current_degree = 0
    current_mode = 'M'
    first_degree = 0
    nb_chords = 0
    nb_modulations = 0
    nb_time_signature_change = 0
    bar_duration = 4
    time_signature_den = 4
    time_signature_nom = 4
    has_time = False
    bar_numbers = []
    nb_bars = 0
    first_mode = 'M'
    tonality_line = None
    first = True
    for line in lines:
        if line == "":
            continue
        elif not line.startswith('m'):
            if line.lower().startswith("time"):
                if not has_time:
                    time_signature_nom = int(line.split(':')[1].strip().split('/')[0])
                    time_signature_den = int(line.split(':')[1].strip().split('/')[1])
                    bar_duration = time_signature_nom * 4 / time_signature_den
                nb_time_signature_change += 1
                has_time = True
            new_harmony.append(line)
        else:
            elements = line.split(' ')
            new_line = []
            for el in elements:
                if ":" in el:
                    degree = TONALITY_DICT[el[0].lower()]
                    mode = 'm' if el[0] == el[0].lower() else 'M'
                    flats = len([e for e in el[1:] if e in ['b', '-']])
                    sharps = len([e for e in el[1:] if e in ['#', 's']])
                    degree = degree + sharps - flats
                    if first:
                        first_degree = degree
                        first_mode = mode
                        #new_line.append(el)
                        tonality_line = el.replace(':', '')
                    else:
                        nb_modulations += 1
                    current_degree = degree
                    current_mode = mode
                    first = False
                elif el.startswith('m'):
                    bar_number = int(el[1:].replace('.', '', 1))
                    bar_numbers.append(bar_number)
                    nb_bars = max(bar_number, nb_bars)
                    new_line.append(el)
                elif el.startswith('b') and el[1:].replace('.', '', 1).isdigit():
                    new_el = el
                    new_line.append(new_el)
                else:
                    nb_chords += 1
                    if current_degree != first_degree or current_mode != first_mode:
                        # Relative tone
                        new_el = el + "/" + get_relative_tone(first_degree,
                                                              first_mode, current_degree, current_mode)
                    else:
                        new_el = el
                    new_line.append(new_el)

            new_harmony.append(' '.join(new_line))
    if tonality_line is not None:
        new_harmony.insert(0, "Tonality : " + tonality_line)

    if get_features:
        new_harmony = "\n".join(new_harmony)
        data = {
                "raw_annotation": harmony,
                "annotation": new_harmony,
                "nb_chords": float(nb_chords),
                "nb_bars": float(nb_bars),
                "nb_chords_per_bar": float(nb_chords / nb_bars),
                "nb_modulations": float(nb_modulations),
                "nb_modulations_per_bar": float(nb_modulations / nb_bars),
                "nb_time_signature_change": float(nb_time_signature_change),
                "time_signature_nom": int(time_signature_nom),
                "time_signature_den": int(time_signature_den),
                "bar_duration": float(bar_duration),
                "max_bar_jump": float(np.max(np.diff(bar_numbers))) if len(bar_numbers) > 1 else 0,
                "mode": first_mode,
                "degree": int(first_degree)
                }
        return new_harmony, data

    return "\n".join(new_harmony)

def _get_degree_and_tonality(sec_degree, ter_degree, degree, key, mode):
    if ter_degree is not None:
        # Change the key, mode
        key_add, new_mode = DICT_TONALITY[mode][ter_degree]
        key, mode = (key + key_add) % 12, new_mode

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


