from .element import Formatter
from musiclang import Chord, Tonality
from musiclang.analyze.roman_parser import analyze_one_chord

class ChordElement(Formatter):

    def __init__(self, text):
        self.text = text

    def to_text(self):
        return ' ' + str(self)

    def __repr__(self):
        return f'{self.text}'

    @classmethod
    def get_key_mode(cls, tonality):
        tab = 'CDEFGAB'
        notes = [0, 2, 4, 5, 7, 9, 11]
        note = tonality.replace(':', '').replace('#', '').replace('b', '').replace('-', '')
        tone = notes[tab.index(note.upper())]
        mode = 'M' if note.upper() == note else 'm'

        tone += tonality.count('#')
        tone -= tonality.count('b')
        tone -= tonality.count('-')

        return tone, mode

    @classmethod
    def get_tonic_chord(cls, tonality):
        key, mode = cls.get_key_mode(tonality)
        if mode == 'm':
            return (ChordElement('i')).parse_with_tonality(tonality)
        elif mode == 'M':
            return (ChordElement('I')).parse_with_tonality(tonality)

    def parse_with_tonality(self, tonality):
        key, mode = self.get_key_mode(tonality)
        final_degree, extension, final_key, final_mode = analyze_one_chord(self.text, key, mode)
        chord = Chord(final_degree,
                      tonality=Tonality(final_key, final_mode))[extension]

        return chord

    def has_pitch(self, pitch, tonality):
        chord = self.parse_with_tonality(tonality)
        return chord.has_pitch(pitch)