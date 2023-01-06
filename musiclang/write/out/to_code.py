"""
Copyright (c) 2023, Florian GARDIN
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import autopep8

def chord_serie_to_code(chord_serie, **kwargs):
    """Export a string with all the generated python code

    Parameters
    ----------
    chord_serie :
        
    **kwargs :
        

    Returns
    -------

    """
    result = []
    result += get_import_lines()
    result += line_return()
    result += get_initial_variable_declaration(**kwargs)
    result += line_return()

    chord_serie_result = []
    for chord_idx, chord in enumerate(chord_serie.chords):

        chord_result = []
        for part_name in chord.parts:
            part = chord.score[part_name]
            code, variable_name = get_part_variables(part, chord_idx, part_name)
            result += code
            chord_result.append((code, variable_name, part_name))

        chord_code, chord_variable_name = get_chord_variable(chord_idx, chord, chord_result)
        chord_serie_result.append(chord_variable_name)
        result += chord_code
        result += line_return()

    # Get chord serie
    result += line_return()

    result += get_score(chord_serie_result)
    result += line_return()
    result += get_end_result()


    result = "\n".join(result)

    result = autopep8.fix_code(result
                                )

    return result

def line_return():
    """ """
    return ['']

def get_score(chord_serie_result):
    """

    Parameters
    ----------
    chord_serie_result :
        

    Returns
    -------

    """
    score_value = " + ".join(chord_serie_result)
    score = [f"score = {score_value}"]
    return score


def get_chord_variable(chord_idx, chord, chord_result):
    """

    Parameters
    ----------
    chord_idx :
        
    chord :
        
    chord_result :
        

    Returns
    -------

    """
    chord_variable_name = f"chord_{chord_idx}"
    code_inside_chord = ""
    for code_part, part_variable_name, part_name in chord_result:
        code_inside_chord += f"{part_name}={part_variable_name},"

    code_inside_chord = code_inside_chord[:-1]

    code_chord_def = chord.to_code()
    code = f"{code_chord_def}({code_inside_chord})"
    result = [f"{chord_variable_name} = {code}"]
    return result, chord_variable_name



def get_part_variables(part, chord_idx, part_name):
    """

    Parameters
    ----------
    part :
        
    chord_idx :
        
    part_name :
        

    Returns
    -------

    """
    variable_name = part_name + '_' + str(chord_idx)

    code = part.to_code()

    result = [f"{variable_name} = {code}"]

    return result, variable_name


def get_end_result():
    """ """
    result = ["score.to_midi(FILENAME, tempo=TEMPO)"]
    return result

def get_initial_variable_declaration(tempo=120, filename="", **kwargs):
    """

    Parameters
    ----------
    tempo :
         (Default value = 120)
    filename :
         (Default value = "")
    **kwargs :
        

    Returns
    -------

    """
    result = [
        "### GLOBAL SCORE VARIABLES",
        "",
        "TEMPO = {tempo}".format(tempo=tempo),
        f'FILENAME = "{filename}" # REPLACE WITH YOUR DESTINATION',
        "",
        "###"
              ]
    return result

def get_import_lines():
    """ """
    result =[
            "from musiclang.write.library import *",
            "from fractions import Fraction as frac"
             ]

    return result


