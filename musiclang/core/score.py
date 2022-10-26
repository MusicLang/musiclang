from .constants import *
from .out.to_code import chord_serie_to_code

class Element:
    """
    An element represents the basis of numeral roman notation, it usually represents a degree
    The first degree is indexed with a 0 value.
    If you call or modulate this object you get a Chord, if you call a mode (m,M,mm) on this you get a Tonality
    (eg : Element(0) = I)
    """
    def __init__(self, val):
        self.val = val

    def __add__(self, other):
        if isinstance(other, int):
            return Element(self.val + other)
        if isinstance(other, Element):
            return Element(self.val, other.val)
        else:
            raise Exception('Cannot add if not type int or Element')

    def __repr__(self):
        return Chord(element=self.val).__repr__()

    def __getitem__(self, extension):
        return Chord(element=self.val, extension=extension)

    def __call__(self, *melodies, **named_melodies):
        return Chord(element=self.val)(*melodies, **named_melodies)


    def __mod__(self, other):
            return Chord(element=self.val) % other

    def copy(self):
        return Element(self.val)

    def o(self, octave):
        return Chord(element=self.val, extension=5).o(octave)

    @property
    def element(self):
        return self.val

    @property
    def tonality(self):
        return Tonality(0)

    @property
    def octave(self):
        return 0

    @property
    def b(self):
        return Tonality(self.val).b

    @property
    def s(self):
        return Tonality(self.val).s

    @property
    def m(self):
        return Tonality(self.val).m

    @property
    def M(self):
        return Tonality(self.val).M

    @property
    def mm(self):
        return Tonality(self.val).mm


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


        pass

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
        degree, accident = INDEX_TONALITY[new_abs_degree]
        octave = (self.abs_degree + other.abs_degree) // 12
        new_mode = other.mode
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

class Note:
    """
    Represents a note
    """
    def __init__(self, type, val, octave, duration, amp=120):
        self.type = type
        self.val = val
        self.octave = octave
        self.duration = duration
        self.amp = amp

    @property
    def notes(self):
        return Melody([self]).notes

    @property
    def scale_pitch(self):
        if self.type == "s":
            return self.val + 7 * self.octave
        else:
            raise Exception(f'Not well defined pitch for type {self.type}')

    @property
    def delta_value(self):
        if self.type[1] == "u":
            return self.val
        elif self.type[1] == "d":
            return -self.val
        else:
            raise Exception(f'Not well defined delta value for type {self.type}')

    def __len__(self):
        return 1

    def copy(self):
        return Note(self.type, self.val, self.octave, self.duration, amp=self.amp)

    def set_duration(self, value):
        result = self.copy()
        result.duration = value
        return result

    def augment(self, value):
        result = self.copy()
        result.duration *= value
        return result

    def change_type(self, new_type):
        c = self.copy()
        c.type = new_type
        return c

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        else:
            return (self.type == other.type) and (self.val == other.val) and (self.duration == other.duration) and \
                   (self.octave == other.octave)

    @property
    def ppp(self):
        note = self.copy()
        note.amp = 20
        return note

    @property
    def pp(self):
        note = self.copy()
        note.amp = 40
        return note

    @property
    def p(self):
        note = self.copy()
        note.amp = 60
        return note

    @property
    def mf(self):
        note = self.copy()
        note.amp = 80
        return note

    @property
    def f(self):
        note = self.copy()
        note.amp = 100
        return note

    @property
    def ff(self):
        note = self.copy()
        note.amp = 110
        return note

    @property
    def fff(self):
        note = self.copy()
        note.amp = 120
        return note

    def add_interval(self, note):
        if note.type[1] not in ['u', 'd']:
            raise Exception('note argument must be a relative type (*u, *d)')
        val = note.val if note.type[1] == 'u' else -note.val
        oct = note.octave
        return self.add_value(val, oct)

    def add_value(self, val, octave):
        if self.type[0] in ['s', 'h', 'c']:
            if self.type[0] == 's':
                mod = 7

            elif self.type[0] == 'h':
                mod = 12

            elif self.type[0] == 'c':
                mod = 3

            new_note = self.copy()
            new_note.val += val
            new_note.octave += octave
            new_note.octave += new_note.val // mod
            new_note.val = new_note.val % mod
        else:
            return self.copy()

        return new_note

    @property
    def had_absolute_note(self):
        return self.starts_with_absolute_note

    @property
    def is_relative(self):
        return ("u" in self.type or "d" in self.type)

    @property
    def starts_with_relative(self):
        return self.is_relative

    @property
    def starts_with_absolute_or_silence(self):
        return self.type == "r" or self.starts_with_absolute_note

    @property
    def is_silence(self):
        return self.type == "r"

    @property
    def is_pattern_note(self):
        return "a" in self.type

    @property
    def is_chromatic_note(self):
        return "h" in self.type

    @property
    def is_scale_note(self):
        return "s" in self.type

    @property
    def is_chord_note(self):
        return "c" in self.type

    @property
    def is_continuation(self):
        return self.type == "l"

    @property
    def is_note(self):
        return self.type not in ["r", "l"]

    @property
    def starts_with_note(self):
        return self.type not in ["r", "l"]

    @property
    def starts_with_absolute_note(self):
        return self.starts_with_note and not self.is_relative

    def __add__(self, other):
        """
        Create a melody from the note and other note or melody
        :param other:
        :return:
        """
        if isinstance(other, Note):
            return Melody([self, other])
        if isinstance(other, Melody):
            return Melody([self] + other.notes)
        else:
            raise Exception('Cannot add if not instance of Note or melody')

    def __and__(self, n):
        """
        Transpose by n
        :param n:
        :return:
        """
        if self.type in ['s', 'c', 'h']:
            return self.add_value(n, 0)
        else:
            return self.copy()

    def __matmul__(self, other):
        # Apply a function to each note
        return other(self.copy())

    def oabs(self, octave):
        note = self.copy()
        note.octave += octave
        return note

    def o(self, octave):
        return self.orel(octave)

    def orel(self, octave):
        """
        Relative octave (change if definite absolute do not otherwise)
        :param octave:
        :return:
        """
        if self.type in ['s', 'h', 'c']:
            return self.oabs(octave)
        return self.copy()

    def __getattr__(self, item):
        try:
            note = self.copy()
            note.duration *= STR_TO_DURATION[item]
            return note
        except:
            raise AttributeError()

    def __mul__(self, other):
        """
        If other is Integer, repeat the note other times
        If other is note, create a vertical melody
        If other is melody append note to vertical melody
        :param other:
        :return:
        """
        if isinstance(other, int):
            return Melody([self.copy() for i in range(other)])
        else:
            raise Exception('Cannot multiply Note and ' + str(type(other)))

    def duration_to_str(self):
        return DURATION_TO_STR[self.duration]

    def __radd__(self, other):
        if other is None:
            return Melody([self.copy()])
        else:
            raise Exception('Cannot add')

    def fix_continuation(self):
        durations_candidates = [d for d in list(DURATION_TO_STR.keys()) if d < self.duration]
        nearest_duration = min(durations_candidates, key=lambda x: abs(x - self.duration))
        remaining_duration = self.duration - nearest_duration
        # Add continuations if necessary
        n1 = self.copy()
        n1.duration = nearest_duration
        n2 = Continuation(remaining_duration)
        return n1 + n2

    def to_code(self):
        """
        Represent a note as valid python code using standard musiclang library
        :return:
        """

        if self.is_note:
            result = f"{self.type}{self.val}"
        else:
            result = f"{self.type}"

        if self.duration != Q:
            if self.duration in DURATION_TO_STR:
                duration = DURATION_TO_STR[self.duration]
                result += f".{duration}"
            else:
                result += f".augment({self.duration})"

        if self.octave != 0:
            result += f".o({self.octave})"

        return result

    def __repr__(self):
        try:
            return f"{self.type}{self.val}.o{self.octave}.{self.duration_to_str()}"
        except KeyError:
            notes = self.fix_continuation()
            return notes.__repr__()


class Silence(Note):
    def __init__(self, duration):
        super().__init__("r", 0, 0, duration)

    def copy(self):
        return Silence(self.duration)

    def __repr__(self):
        try:
            return f"r.{self.duration_to_str()}"
        except KeyError:
            notes = self.fix_continuation()
            return notes.__repr__()

class Continuation(Note):
    def __init__(self, duration):
        super().__init__("l", 0, 0, duration)

    def copy(self):
        return Continuation(self.duration)

    def __repr__(self):
        try:
            return f"l.{self.duration_to_str()}"
        except KeyError:
            notes = self.fix_continuation()
            return notes.__repr__()

class Melody:
    def __init__(self, notes):
        self.notes = notes

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __add__(self, other):
        if isinstance(other, Note):
            return Melody(self.notes + [other])
        if isinstance(other, Melody):
            return Melody(self.notes + other.notes)

    def to_code(self):
        return " + ".join([n.to_code() for n in self.notes])

    @property
    def is_continuation(self):
        return all([n.is_continuation for n in self.notes])

    @property
    def starts_with_absolute_note(self):
        if len(self.notes) > 0:
            return self.notes[0].starts_with_absolute_note
        else:
            return False

    @property
    def had_absolute_note(self):
        return any([n.starts_with_absolute_note for n in self.notes])

    @property
    def starts_with_absolute_or_silence(self):
        if len(self.notes) > 0:
            return self.notes[0].starts_with_absolute_or_silence
        else:
            return False

    @property
    def starts_with_note(self):
        if len(self.notes) > 0:
            return self.notes[0].starts_with_note
        else:
            return False

    def augment(self, value):
        return Melody([n.augment(value) for n in self.notes])

    @property
    def duration(self):
        return sum([n.duration for n in self.notes])

    def __radd__(self, other):
        if other is None:
            return self.copy()

    def __and__(self, other):
        return Melody([n & other for n in self.notes])

    def __matmul__(self, other):
        # Apply a function to each note
        return Melody([n @ other for n in self.notes])

    def __mul__(self, other):
        if isinstance(other, int):
            melody_copy = self.copy()
            return Melody(melody_copy.notes * other)
        if isinstance(other, Note):
            return self * Melody([other.copy()])
        else:
            raise Exception('Cannot multiply Melody and ' + str(type(other)))

    def __len__(self):
        return len(self.notes)

    def o(self, octave):
        return Melody([n.o(octave) for n in self.notes])

    def __hasattr__(self, item):
        try:
            self.__getattr__(item)
        except:
            return False
        return True

    def __getattr__(self, item):
        try:
            return Melody([getattr(n, item) for n in self.notes])
        except:
            raise AttributeError()

    def copy(self):
        return Melody([s.copy() for s in self.notes])

    def __repr__(self):
        return ' '.join([str(note) for note in self.notes])

class Chord:

    EXCLUDED_ITEMS = ['__array_struct__']
    def __init__(self, element, extension=5, tonality=None, score=None, octave=0):
        self.element = element
        self.extension = extension
        self.tonality = tonality
        self.octave = octave
        self.score = {} if score is None else score

    @property
    def parts(self):
        return list(self.score.keys())


    def get_part(self, item):
        if isinstance(item, int):
            return self.score[self.parts[item]]
        else:
            return self.score[item]


    def __eq__(self, other):
        if not isinstance(other, Chord):
            return False
        return self.element == other.element and self.extension == other.extension and self.tonality == other.tonality and self.octave == other.octave

    def __hash__(self):
        return hash( self.__repr__())

    @property
    def possible_notes(self):
        if self.extension == 5:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1)]
        elif self.extension == 7:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1)]
        elif self.extension == 9:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1), Note("s", 1, 1, 1)]
        elif self.extension == 11:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1), Note("s", 1, 1, 1), Note("s", 3, 1, 1)]
        elif self.extension == 13:
            return [Note("s", 0, 0, 1), Note("s", 2, 0, 1), Note("s", 4, 0, 1), Note("s", 6, 0, 1),
                    Note("s", 1, 1, 1), Note("s", 3, 1, 1), Note("s", 5, 1, 1)]

    @property
    def scale_notes(self):
        return [Note("s", i, 0, 1) for i in range(7)]

    @property
    def scale_dissonances(self):
        consonances = {(note.val % 7) for note in self.possible_notes}
        return [note for note in self.scale_notes if note.val not in consonances]

    def __getitem__(self, item):

        res = self.copy()
        res.extension = item
        if item not in [5, 7, 9, 11, 13]:
            raise Exception('Not valid chord extension : {}'.format(item))
        return res
    #
    # def __getattr__(self, item):
    #     chord = self.copy()
    #     chord.score = {k: getattr(s, item) for k, s in self.score.items()}
    #     return chord

    @property
    def duration(self):
        return max([self.score[key].duration for key in self.score.keys()])

    def set_part(self, item, part):
        part_name = self.parts[item] if isinstance(item, int) else item
        self.score[part_name] = part

    def has_score(self):
        return self.score is not None

    def to_chord(self):
        result = self.copy()
        result.score = None
        return result


    @property
    def chords(self):
        return Score([self]).chords

    def __mod__(self, other):
        #C.M [II.m] II:III#.M  ==> G#.m (2e accords de la troisième gamme de la deuxième gamme de do majeur)
        if isinstance(other, Tonality):
            chord = self.copy()
            # Tonality is always referenced from base tonality which is the most outside tonality
            other = other.copy()
            other.octave += self.octave
            chord.tonality = other + chord.tonality
            chord.octave = 0
            return chord
        else:
            raise Exception('Following % should be a Tonality')


    def modulate(self, other):
        if isinstance(other, Tonality):
            chord = self.copy()
            # Tonality is always referenced from base tonality which is the most outside tonality
            other = other.copy()
            other.octave += self.octave
            chord.tonality = chord.tonality + other
            chord.octave = 0
            return chord
        else:
            raise Exception('Following % should be a Tonality')

    def __add__(self, other):
        if isinstance(other, Chord):
            return Score([self.copy(), other.copy()])
        if isinstance(other, Score):
            return Score([self.copy()] + other.copy().chords)


    def __radd__(self, other):
        if other is None:
            return self.copy()

    def element_to_str(self):
        return ELEMENT_TO_STR[self.element]

    def extension_to_str(self):
        if self.extension == 5:
            return ''
        else:
            return '.' + str(self.extension)

    def melody_to_str(self):
        return ','.join([f"<{k}> " + str(melody) for k, melody in self.score.items()])

    def tonality_to_str(self, sep="/"):
        if self.tonality is None:
            return ""
        else:
            return f"{sep}" + str(self.tonality)

    def tonality_to_code(self):
        if self.tonality is None:
            return ""

        return " % " + self.tonality.to_code()

    def d(self):
        return self.o(-1)

    def u(self):
        return self.o(1)

    def o(self, octave):
        c = self.copy()
        c.octave += octave
        return c

    def copy(self):
        return Chord(element=self.element,
                     extension=self.extension,
                     tonality=self.tonality.copy() if self.tonality is not None else None,
                     score={k: s.copy() for k, s in self.score.items()} if self.score is not None else None,
                     octave=self.octave
                     )

    def preparse_named_melodies(self, named_melodies):
        named_melodies_result = {}
        for key in named_melodies.keys():
            key_obj = key.split('__')
            if len(key_obj) == 1:
                key_obj = key_obj[0]
                number = 0
            else:
                key_obj, number = key_obj[0], key_obj[1]
                number = int(number)

            if(isinstance(named_melodies[key], list)):
                for idx, melody in enumerate(named_melodies[key]):
                    named_melodies_result[key_obj + '__' + str(number + idx)] = melody
            else:
                named_melodies_result[key_obj + '__' + str(number)] = named_melodies[key]

        return named_melodies_result

    def __getattr__(self, item):
        try:
            return self(**{part: getattr(self.score[part], item) for part in self.parts})
        except:
            raise AttributeError()

    def __call__(self, *melodies, **named_melodies):
        chord = self.copy()
        named_melodies_preparsed = self.preparse_named_melodies(named_melodies)
        chord.score = {**{i: melody for i, melody in enumerate(melodies)}, **named_melodies_preparsed}
        return chord

    def __repr__(self):
        if self.score:
            return f"{self.element_to_str()}{self.extension_to_str()}{self.tonality_to_str()}({self.melody_to_str()})"
        else:
            return f"{self.element_to_str()}{self.extension_to_str()}{self.tonality_to_str()}"

    def to_code(self):
        """
        Export the code as python interpretable str.
        It ignores the score
        :return:
        """
        chord_str = f"({self.element_to_str()}{self.tonality_to_code()})"
        if self.octave != 0:
            chord_str = f"{chord_str}.o({self.octave})"

        return chord_str


class Score:
    def __init__(self, chords=None):
        self.chords = chords
        if self.chords is None:
            self.chords = []

    def to_chords(self):
        res = [chord.to_chord() for chord in self.chords]
        return res

    def copy(self):
        return Score([c.copy() for c in self.chords])

    def __add__(self, other):
        if isinstance(other, Chord):
            return Score(self.copy().chords + [other])
        if isinstance(other, Score):
            return Score(self.copy().chords + other.copy().chords)
        else:
            raise Exception('Cannot add to Score if not Chord or Score')

    def __getattr__(self, item):
        chords = self.copy()
        chords.chords = [getattr(s, item) for s in self.chords]
        return chords

    def __mod__(self, other):
        if isinstance(other, Tonality):
            return Score([c % other for c in self.chords])
        else:
            raise Exception('Following % should be a Tonality')

    def __radd__(self, other):
        if other is None:
            return self.copy()

    def __repr__(self):
        return ' \n'.join([str(chord) for chord in self.chords])


    def to_code(self, **kwargs):
        """
        Export the chord serie as a string representing valid python code that recreates the score
        :return:
        """

        code = chord_serie_to_code(self, **kwargs)
        return code

    def to_code_file(self, filepath, **kwargs):
        """
        Export the chord serie as a file representing valid python code that recreates the score
        :param filepath:
        :return:
        """
        code = self.to_code(**kwargs)
        with open(filepath, 'w') as f:
            f.write(code)

