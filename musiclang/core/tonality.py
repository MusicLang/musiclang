from .constants import *

class Tonality:
    """
    Represents a tonality, it can be applied via % operator to a chord to modulate it on another tonality
    It is represented by a degree, an accident, a mode, and an octave

    """
    def __init__(self, degree, accident="", mode="M", octave=0):
        self.degree = degree
        self.accident = accident
        self.mode = mode
        self.octave = octave

    @property
    def scale_pitches(self):
        abs_degree = self.abs_degree
        mode = self.mode
        octave = self.octave
        pitch_scale = [n + abs_degree + 12 * octave for n in SCALES[mode]]
        return pitch_scale

    def _eq(self, other):
        return self.degree == other.degree and self.accident == other.accident and self.mode == other.mode and self.octave == other.octave

    def __eq__(self, other):
        if not isinstance(other, Tonality):
            return False
        # To get equalities between enharmonies we need to reformulate chord adding neutral modulation
        return (Tonality(0) + self )._eq(Tonality(0) + other )

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def copy(self):
        return Tonality(self.degree, self.accident, self.mode, self.octave)

    def __radd__(self, other):
        if other is None:
            return self
        else:
            raise Exception('Not valid addition of tonality')

    def add(self, other):
        new_abs_degree = (self.abs_degree + other.abs_degree) % 12
        new_mode = other.mode
        degree, accident = INDEX_TONALITY[new_mode][new_abs_degree]
        octave = (self.abs_degree + other.abs_degree) // 12
        return Tonality(degree=degree, accident=accident, mode=new_mode, octave=octave)

    @property
    def abs_degree(self):
        return INDEX_MODE[self.mode][(self.degree, self.accident)]

    def __add__(self, other):
        """
        Add another tonality
        :param other:
        :return:
        """
        if other is None:
            return self
        else:
            return self.add(other)

    @property
    def b(self):
        tone = self.copy()
        tone.accident = "b"
        return tone

    @property
    def s(self):
        tone = self.copy()
        tone.accident = "s"
        return tone

    @property
    def m(self):
        tone = self.copy()
        tone.mode = "m"
        return tone

    @property
    def M(self):
        tone = self.copy()
        tone.mode = "M"
        return tone

    @property
    def mm(self):
        tone = self.copy()
        tone.mode = "mm"
        return tone


    @property
    def dorian(self):
        tone = self.copy()
        tone.mode = "dorian"
        return tone

    @property
    def phrygian(self):
        tone = self.copy()
        tone.mode = "phrygian"
        return tone

    @property
    def lydian(self):
        tone = self.copy()
        tone.mode = "lydian"
        return tone

    @property
    def mixolydian(self):
        tone = self.copy()
        tone.mode = "mixolydian"
        return tone

    @property
    def aeolian(self):
        tone = self.copy()
        tone.mode = "aeolian"
        return tone

    @property
    def locrian(self):
        tone = self.copy()
        tone.mode = "locrian"
        return tone


    def d(self):
        return self.o(-1)

    def o(self, octave):
        tonality = self.copy()
        tonality.octave += octave
        return tonality

    def degree_to_str(self):
        return ELEMENT_TO_STR[self.degree]

    def __repr__(self):
        return f'{self.degree_to_str()}{self.accident}.{self.mode}.o{self.octave}'

    def to_code(self):
        sep_accident = ""
        if self.accident != "":
            sep_accident = "." + self.accident
        octave_str = ""
        if self.octave != 0:
            octave_str = f".o({self.octave})"

        return f'{self.degree_to_str()}{sep_accident}.{self.mode}{octave_str}'
