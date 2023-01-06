from lark import Lark
from lark.exceptions import UnexpectedToken, UnexpectedInput, UnexpectedCharacters, UnexpectedEOF



grammar = """
%ignore " "
start           : (expression "+")* expression ";"
expression      : chord
chord           : "(" DEGREE (EXTENSION)? ( "%" tonality)? ")"
DEGREE          : "I" | "II" | "III" | "IV" | "V" | "VI" | "VII"
tonality        : DEGREE ("." ACCIDENT)? "." MODE
ACCIDENT        : "b" | "s"
MODE            : "m" | "M" | "mm"
EXTENSION       : "[]"  | "['7']" | "['6']" | "['64']" | "['65']" | "['2']" | "['63']" | "['43']"
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
    ('MODE', 'm'),
    ('MODE', 'M'),
    ('MODE', 'mm'),
    ('ACCIDENT', 'b'),
    ('ACCIDENT', 's'),
    ('PERCENT', '%'),
    ('PLUS', '+'),
    ('DOT', '.'),
    ('LPAR', '('),
    ('RPAR', ')'),
    ('SEMICOLON', ';'),
    ('EXTENSION', "['7']"),
    ('EXTENSION', "['64']"),
    ('EXTENSION', "['6']"),
    ('EXTENSION', "['65']"),
    ('EXTENSION', "['2']"),
    ('EXTENSION', "['63']"),
    ('EXTENSION', "['43']"),
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

TOKENS_IDXS = _construct_tokens()
TERMINAL_TYPE = 'SEMICOLON'
TERMINAL_IDX = TOKENIZER[('SEMICOLON', ';')]

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
    try:
        PARSER.parse(text + 'X')
    except UnexpectedEOF as e:
        return e.expected
    except UnexpectedCharacters as e:
        return list(e.allowed)
    return []

def get_candidates_idx(text):
    """

    Parameters
    ----------
    text :
        

    Returns
    -------

    """
    import numpy as np
    candidates = get_candidates(text)

    vec = np.zeros(len(TOKENIZER), dtype=float)
    idxs = np.asarray(sum([TOKENS_IDXS[c] for c in candidates], []))
    # Transform it to potential tokens
    vec[vec == 0] = - float('inf')
    vec[idxs] = 0.0

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
    score_str = "+".join([str(s).replace('(\n)', '') for s in score.to_score().to_chords()]) + ";"
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