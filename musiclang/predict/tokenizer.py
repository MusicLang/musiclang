from musiclang import Score


import lark
from lark import Lark

grammar = """
%ignore " "
start           : (expression "+")+ expression ";"
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
DETOKENIZER = {val: key for key, val in TOKENIZER.items()}



def tokenize_string(text):
    tokens = [TOKENIZER[(d.type, d.value)] for d in list(PARSER.lex(text))]
    return tokens

def tokenize(score):
    score_str = "+".join([str(s).replace('(\n)', '') for s in score.to_chords()]) + ";"
    tokens = [TOKENIZER[(d.type, d.value)] for d in list(PARSER.lex(score_str))]
    return tokens

def untokenize(tokens):
    return ''.join([DETOKENIZER[d][1] for d in tokens])