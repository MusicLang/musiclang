
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
        from .chord import Chord
        return Chord(element=self.val).__repr__()

    def __getitem__(self, extension):
        from .chord import Chord
        return Chord(element=self.val, extension=extension)

    def __call__(self, *melodies, **named_melodies):
        from .chord import Chord
        return Chord(element=self.val)(*melodies, **named_melodies)


    def __mod__(self, other):
            from .chord import Chord
            return Chord(element=self.val) % other


    def copy(self):
        return Element(self.val)

    def o(self, octave):
        from .chord import Chord
        return Chord(element=self.val, extension=5).o(octave)

    @property
    def scale_pitches(self):
        return self.o(0).scale_pitches

    @property
    def element(self):
        return self.val

    @property
    def tonality(self):
        from .tonality import Tonality
        return Tonality(0)

    @property
    def octave(self):
        return 0

    @property
    def b(self):
        from .tonality import Tonality
        return Tonality(self.val).b

    @property
    def s(self):
        from .tonality import Tonality
        return Tonality(self.val).s

    @property
    def m(self):
        from .tonality import Tonality
        return Tonality(self.val).m

    @property
    def M(self):
        from .tonality import Tonality
        return Tonality(self.val).M

    @property
    def mm(self):
        from .tonality import Tonality
        return Tonality(self.val).mm


    @property
    def dorian(self):
        from .tonality import Tonality
        return Tonality(self.val).dorian

    @property
    def phrygian(self):
        from .tonality import Tonality
        return Tonality(self.val).phrygian

    @property
    def lydian(self):
        from .tonality import Tonality
        return Tonality(self.val).lydian

    @property
    def mixolydian(self):
        from .tonality import Tonality
        return Tonality(self.val).mixolydian

    @property
    def aeolian(self):
        from .tonality import Tonality
        return Tonality(self.val).aeolian

    @property
    def locrian(self):
        from .tonality import Tonality
        return Tonality(self.val).locrian

