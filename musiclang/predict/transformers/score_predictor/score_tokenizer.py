from musiclang.write.library import T, S, E, Q, H, W
from lark.exceptions import UnexpectedToken, UnexpectedInput, UnexpectedCharacters, UnexpectedEOF
from fractions import Fraction as frac
from lark import Lark


grammar = """
// EBNF Rule for a simple music language based on chord
// Melodies are specified relatively to the chord scale context
%ignore " "
%ignore "\\n"
%ignore "\\t"
start           : (expression "+")* expression SEMICOLON
expression      : chord LPAR chord_dict RPAR
chord           : LPAR DEGREE (FIGURED_BASS)? ( PERCENT tonality) RPAR
chord_dict      : (INSTRUMENT EQUAL melody COMMA)* (INSTRUMENT EQUAL melody) 
melody          : (note PLUS)* note
note            : (SCALE_NOTE | CHROMATIC_NOTE | SILENCE | CONTINUATION ) (DOT full_duration)? (DOT OCTAVE )? (DOT DYNAMIC)?
full_duration   : (DURATION (DOTTED_DURATION)*) | (DURATION (N_UPLET)?)
tonality        : DEGREE (DOT ACCIDENT)? DOT TONALITY_MODE
LPAR            : "("
RPAR            : ")"
PERCENT         : "%"
PLUS            : "+"
SEMICOLON       : ";"
DOT             : "."
DEGREE          : "I" | "II" | "III" | "IV" | "V" | "VI" | "VII" // Chord degree (always upper case because relative to a tonality)
ACCIDENT        : "b" | "s" // flat and sharp
COMMA           : ","
EQUAL           : "="
TONALITY_MODE   : "M" | "m" | "mm" // Major, minor and melodic minor
FIGURED_BASS    : "[]"  | "['7']" | "['6']" | "['64']" | "['65']" | "['2']" | "['63']" | "['43']" // Roman numeral figured bass
OCTAVE          : "o(1)" | "o(-1)" | "o(-2)" | "o(2)" | "o(3)" | "o(-3)" | "o(4)" | "o(-4)"| "o(5)" | "o(-5)" // Delta octave (1, -1, ...)
DURATION        : "w" | "h" | "q" | "e" | "s" | "t" // (Base duration of a note, by order : ( "whole" | "half" | "quarter" | "sixteenth" | "thirty-second" )
DOTTED_DURATION : "d"  // Dotted duration
N_UPLET         : "3" | "5" | "7"
SCALE_NOTE      : "s0" | "s1" | "s2" | "s3" | "s4" | "s5" | "s6" // Scale notes : s0 = first note of the chord scale, s1 = second note , etc ...). Example : In (I % I.M), s0 = C, s1 = D, s6 = B
CHROMATIC_NOTE  : "h0" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "h7" | "h8" | "h9" | "h10" | "h11" // Chromatic note, example, in (I % I.M):  h0 = C, h1 = C#, h6 = F#
SILENCE         : "r" // To denote a rest in the music
CONTINUATION    : "l" // To denote that it should be the continuation of the previous note in a melody
DYNAMIC         : "ppp" | "pp" | "p" | "mf" | "f" | "ff" | "fff" ("molto pianissimo" | "pianissimo" | "piano" | "mezzo forte" | "forte" | "double forte" | "triple forte"
INSTRUMENT      : "V__0" | "piano__0" | "piano__1" | "piano__2" | "piano__3" | "piano__4" | "piano__5" | "piano__6" | "piano__7" | "piano__8" | "piano__9" | "piano__10" | "piano__11" | "piano__12" | "piano__13" | "piano__14" | "piano__15"
"""

PARSER = Lark(grammar)


TOKENS  = [
    ('DEGREE', 'I'),
    ('DEGREE', 'II'),
    ('DEGREE', 'III'),
    ('DEGREE', 'IV'),
    ('DEGREE', 'V'),
    ('DEGREE', 'VI'),
    ('DEGREE', 'VII'),
    ('TONALITY_MODE', 'm'),
    ('TONALITY_MODE', 'M'),
    ('TONALITY_MODE', 'mm'),
    ('ACCIDENT', 'b'),
    ('ACCIDENT', 's'),
    ('PERCENT', '%'),
    ('PLUS', '+'),
    ('DOT', '.'),
    ('LPAR', '('),
    ('RPAR', ')'),
    ('SEMICOLON', ';'),
    ('FIGURED_BASS', "['7']"),
    ('FIGURED_BASS', "['64']"),
    ('FIGURED_BASS', "['6']"),
    ('FIGURED_BASS', "['65']"),
    ('FIGURED_BASS', "['2']"),
    ('FIGURED_BASS', "['63']"),
    ('FIGURED_BASS', "['43']"),
    ('OCTAVE', "o(1)"),
    ('OCTAVE', "o(-1)"),
    ('OCTAVE', "o(2)"),
    ('OCTAVE', "o(-2)"),
    ('OCTAVE', "o(3)"),
    ('OCTAVE', "o(-3)"),
    ('OCTAVE', "o(4)"),
    ('OCTAVE', "o(-4)"),
    ('OCTAVE', "o(5)"),
    ('OCTAVE', "o(-5)"),
    ('DURATION', "t"),
    ('DURATION', "s"),
    ('DURATION', "e"),
    ('DURATION', "q"),
    ('DURATION', "h"),
    ('DURATION', "w"),
    ('DOTTED_DURATION', 'd'),
    ('N_UPLET', "3"),
    ('N_UPLET', "5"),
    ('N_UPLET', "7"),
    ('SILENCE', "r"),
    ('CONTINUATION', "l"),
    ('SCALE_NOTE', "s0"),
    ('SCALE_NOTE', "s1"),
    ('SCALE_NOTE', "s2"),
    ('SCALE_NOTE', "s3"),
    ('SCALE_NOTE', "s4"),
    ('SCALE_NOTE', "s5"),
    ('SCALE_NOTE', "s6"),
    ('CHROMATIC_NOTE', "h0"),
    ('CHROMATIC_NOTE', "h1"),
    ('CHROMATIC_NOTE', "h2"),
    ('CHROMATIC_NOTE', "h3"),
    ('CHROMATIC_NOTE', "h4"),
    ('CHROMATIC_NOTE', "h5"),
    ('CHROMATIC_NOTE', "h6"),
    ('CHROMATIC_NOTE', "h7"),
    ('CHROMATIC_NOTE', "h8"),
    ('CHROMATIC_NOTE', "h9"),
    ('CHROMATIC_NOTE', "h10"),
    ('CHROMATIC_NOTE', "h11"),
    ('DYNAMIC', "ppp"),
    ('DYNAMIC', "pp"),
    ('DYNAMIC', "p"),
    ('DYNAMIC', "mf"),
    ('DYNAMIC', "f"),
    ('DYNAMIC', "ff"),
    ('DYNAMIC', "fff"),
    ('INSTRUMENT', 'V__0'),
    ('INSTRUMENT', 'piano__0'),
    ('INSTRUMENT', 'piano__1'),
    ('INSTRUMENT', 'piano__2'),
    ('INSTRUMENT', 'piano__3'),
    ('INSTRUMENT', 'piano__4'),
    ('INSTRUMENT', 'piano__5'),
    ('INSTRUMENT', 'piano__6'),
    ('INSTRUMENT', 'piano__7'),
    ('INSTRUMENT', 'piano__8'),
    ('INSTRUMENT', 'piano__9'),
    ('INSTRUMENT', 'piano__10'),
    ('INSTRUMENT', 'piano__11'),
    ('INSTRUMENT', 'piano__12'),
    ('INSTRUMENT', 'piano__13'),
    ('INSTRUMENT', 'piano__14'),
    ('INSTRUMENT', 'piano__15'),
    ('COMMA', ','),
    ('EQUAL', "=")
]

TOKENIZER = {val: idx for idx, val in enumerate(TOKENS)}
TOKENIZER_STR = {val[1]: idx for idx, val in enumerate(TOKENS)}
DETOKENIZER = {val: key for key, val in TOKENIZER.items()}

def _construct_tokens():
    """ """
    result = {}
    for type, val in TOKENS:
        idx = TOKENIZER[(type, val)]
        result[type] = result.get(type, []) + [idx]

    return result


from musiclang import Note
_note = Note('s', 0, 0, 1)

TOKENS_IDXS = _construct_tokens()

TERMINAL_TYPE = 'SEMICOLON'
TERMINAL_IDX = TOKENIZER[('SEMICOLON', ';')]
CANDIDATES_BASE = [T, S, E, Q, H, W]
CANDIDATES_DOTTED = [c * frac(3, 2) for c in CANDIDATES_BASE]
CANDIDATES_3_UPLET = [_note.w3.duration, _note.h3.duration, _note.q3.duration, _note.e3.duration, _note.s3.duration, _note.t3.duration]
CANDIDATES_5_UPLET = [_note.w5.duration, _note.h5.duration, _note.q5.duration, _note.e5.duration, _note.s5.duration, _note.t5.duration]
CANDIDATES_7_UPLET = [_note.w7.duration, _note.h7.duration, _note.q7.duration, _note.e7.duration, _note.s7.duration, _note.t7.duration]
CANDIDATES_N_UPLET = CANDIDATES_3_UPLET + CANDIDATES_5_UPLET + CANDIDATES_7_UPLET

NORMALS = set(CANDIDATES_BASE + CANDIDATES_DOTTED + CANDIDATES_N_UPLET)
CANDIDATES = CANDIDATES_BASE + CANDIDATES_DOTTED
CANDIDATES_3 = CANDIDATES_3_UPLET
CANDIDATES = list(sorted(CANDIDATES))

CANDIDATES_DENOM = {
    3: list(sorted(CANDIDATES_BASE + CANDIDATES_3_UPLET)),
    6: list(sorted(CANDIDATES_BASE + CANDIDATES_3_UPLET)),
    12: list(sorted(CANDIDATES_BASE + CANDIDATES_3_UPLET)),
    24: list(sorted(CANDIDATES_BASE + CANDIDATES_3_UPLET)),
    5: list(sorted(CANDIDATES_BASE + CANDIDATES_5_UPLET)),
    10: list(sorted(CANDIDATES_BASE + CANDIDATES_5_UPLET)),
    20: list(sorted(CANDIDATES_BASE + CANDIDATES_5_UPLET)),
    7: list(sorted(CANDIDATES_BASE + CANDIDATES_7_UPLET)),
    14: list(sorted(CANDIDATES_BASE + CANDIDATES_7_UPLET)),
    28: list(sorted(CANDIDATES_BASE + CANDIDATES_7_UPLET))
}

def correct_with_grammar(text):
    """

    Parameters
    ----------
    text :
        

    Returns
    -------
    type
        valid_character : boolean, True if the character is suitable for musiclang
        expected : list[str]: List of expected tokens

    """
    try:
        PARSER.parse(text)
    except UnexpectedEOF as e:
        return True, e.expected
    except UnexpectedCharacters as e:
        return False, list(e.allowed)
    return True, []


def get_candidates(text):
    """

    Parameters
    ----------
    text :
        

    Returns
    -------
    type
        valid_character : boolean, True if the character is suitable for musiclang
        expected : list[str]: List of expected tokens

    """
    import time
    start = time.time()
    try:
        PARSER.parse(text + 'X')
    except UnexpectedEOF as e:
        return e.expected
    except UnexpectedCharacters as e:
        return list(e.allowed)
    return []


ALL_INSTRUMENTS = {f'piano__{i}' for i in range(16)}

def get_candidates_idx(text, can_terminate=False):
    """

    Parameters
    ----------
    text :
        
    can_terminate :
         (Default value = False)

    Returns
    -------

    """
    import numpy as np
    candidates = get_candidates(text)
    tokens = list(PARSER.lex(text))
    instruments = {t.value for t in tokens if t.type == 'INSTRUMENT'}
    forbidden_instruments = ALL_INSTRUMENTS - (ALL_INSTRUMENTS - instruments)
    forbidden_instruments_idx = [TOKENIZER[('INSTRUMENT', ins)] for ins in forbidden_instruments]
    vec = np.zeros(len(TOKENIZER), dtype=float)
    idxs = np.asarray(sum([TOKENS_IDXS[c] for c in candidates], []))
    # Transform it to potential tokens
    vec[vec == 0] = - float('inf')
    vec[idxs] = 0.0
    vec[forbidden_instruments_idx] = - float('inf')
    if not can_terminate:
        vec[TERMINAL_IDX] = - float('inf')

    return vec


def get_is_terminal(text):
    """

    Parameters
    ----------
    text :
        

    Returns
    -------

    """
    return TERMINAL_TYPE in get_candidates(text)


def tokenize_string(text):
    """

    Parameters
    ----------
    text :
        

    Returns
    -------

    """
    tokens = [TOKENIZER[(d.type, d.value)] for d in list(PARSER.lex(text))]
    return tokens

def score_to_text(score):
    """

    Parameters
    ----------
    score :
        

    Returns
    -------

    """
    clean_score = decompose_duration_score(score.to_score())
    score_str = str(clean_score) + ';'
    return score_str

def tokenize(score):
    """

    Parameters
    ----------
    score :
        

    Returns
    -------

    """
    score_str = score_to_text(score)
    tokens = tokenize_string(score_str)
    return tokens

def untokenize(tokens):
    """

    Parameters
    ----------
    tokens :
        

    Returns
    -------

    """
    return ''.join([DETOKENIZER[d][1] for d in tokens])


def decompose_duration(note):
    """

    Parameters
    ----------
    note :
        

    Returns
    -------

    """
    from musiclang import Continuation
    result = None
    # Find biggest that fit
    duration = note.duration
    if duration in NORMALS:
        return note
    denom = frac(note.duration).denominator
    candidates = CANDIDATES_DENOM.get(denom, CANDIDATES)
    biggest_c = [c for c in candidates if c <= note.duration][-1]
    result += note.copy().augment(biggest_c / note.duration)
    remaining_duration = note.duration - result.duration
    while True:
        if result.duration == note.duration:
            return result
        try:
            biggest_c = [c for c in candidates if c <= remaining_duration][-1]
        except:
            return result
        result += Continuation(biggest_c)
        remaining_duration = note.duration - result.duration


def decompose_duration_score(score):
    """

    Parameters
    ----------
    score :
        

    Returns
    -------

    """
    new_score = None
    for chord in score:
        new_dict = {}
        for inst in chord.parts:
            new_melody = None
            for note in chord.score[inst].notes:
                new_melody += decompose_duration(note)
            new_dict[inst] = new_melody

        new_score += chord(**new_dict)

    return new_score



