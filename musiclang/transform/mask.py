class Mask:

    def __call__(self, element, **kwargs):
        return True

    @classmethod
    def eval(cls, query):
        # Add to the namespace
        has = Mask.Has
        has_at_least = Mask.HasAtLeast
        Score = Mask.Score()
        Melody = Mask.Melody()
        Note = Mask.Note()
        Chord = Mask.Chord()
        true = Mask.True_
        false = Mask.False_
        query = eval(query)
        return query

    def child(self, element):
        return self

    @classmethod
    def HasAtLeast(cls, tags):
        return HasAtLeastMask(tags)

    @classmethod
    def Has(cls, tags):
        return HasMask(tags)

    @classmethod
    def And(cls, tags):
        return AndMask(tags)

    @classmethod
    def Bool(cls, bool):
        return BoolMask(bool)

    @classmethod
    def True_(cls):
        return BoolMask(True)

    @classmethod
    def False_(cls):
        return BoolMask(False)

    @classmethod
    def Or(cls, tags):
        return OrMask(tags)

    @classmethod
    def Score(cls):
        return ScoreMask()

    @classmethod
    def Melody(cls):
        return MelodyMask()

    @classmethod
    def Note(cls):
        return NoteMask()

    @classmethod
    def Chord(cls):
        return ChordMask()

    @classmethod
    def Func(cls, f):
        return FuncMask(f)

    def __and__(self, other):
        return AndMask([self, other])

    def __or__(self, other):
        return OrMask([self, other])

    def __invert__(self):
        return NotMask(self)

    def __repr__(self):
        return 'true'


class FuncMask(Mask):

    def __init__(self, f):
        self.f = f

    def __call__(self, element, **kwargs):
        return self.f(element, **kwargs)

    def __repr__(self):
        return 'funcMask'


class HasAtLeastMask(Mask):
    def __init__(self, tags):
        if isinstance(tags, str):
            tags = {tags}
        self.tags = set(tags)

    def __call__(self, element, **kwargs):
        return len(element.tags.intersection(self.tags)) > 0

    def __repr__(self):
        return f"has_at_least({self.tags})"


class NotMask(Mask):
    def __init__(self, other):
        self.other = other

    def __call__(self, element, **kwargs):
        return not self.other(element)

    def __repr__(self):
        return f"~ {self.other}"


class HasMask(Mask):
    def __init__(self, tags):
        if isinstance(tags, str):
            tags = {tags}
        self.tags = set(tags)

    def __call__(self, element, **kwargs):
        return element.tags.issuperset(self.tags)

    def __repr__(self):
        return f"has({self.tags})"


class AndMask(Mask):
    def __init__(self, terms):
        self.terms = terms

    def child(self, element):
        return self.__class__([t.child(element) for t in self.terms])

    def __call__(self, element, **kwargs):
        return all([t(element) for t in self.terms])

    def __repr__(self):
        return " & ".join([f"({term})" for term in self.terms])


class OrMask(Mask):
    def __init__(self, terms):
        self.terms = terms

    def child(self, element):
        return self.__class__([t.child(element) for t in self.terms])

    def __call__(self, element, **kwargs):
        return any([t(element) for t in self.terms])

    def __repr__(self):
        return " | ".join([f"({term})" for term in self.terms])


class BoolMask(Mask):

    def __init__(self, bool):
        self.bool = bool

    def __repr__(self):
        return f"{str(self.bool).lower()}"

    def __call__(self, element, **kwargs):
        return self.bool


class FalseMask(Mask):

    def __call__(self, element, **kwargs):
        return False

    def __repr__(self):
        return "false"


class TrueMask(Mask):

    def __call__(self, element, **kwargs):
        return True

    def __repr__(self):
        return "true"


class GtMask(Mask):

    def __init__(self, terms):
        self.terms = terms

    def child(self, element, **kwargs):
        return self if self.terms[0](element) else BoolMask(self(element))

    def __call__(self, element, **kwargs):
        return self.terms[0](element, **kwargs) or self.terms[1](element, **kwargs)

    def __repr__(self):
        return " > ".join([f"({term})" for term in self.terms])


class TypeMask(Mask):

    def __gt__(self, other):
        return GtMask([self, other])


class ScoreMask(TypeMask):

    def __call__(self, element, **kwargs):
        from musiclang import Score
        return not isinstance(element, Score)

    def __repr__(self):
        return "Score"


class MelodyMask(TypeMask):

    def __call__(self, element, **kwargs):
        from musiclang import Melody
        return not isinstance(element, Melody)

    def __repr__(self):
        return "Melody"


class ChordMask(TypeMask):
    def __call__(self, element, **kwargs):
        from musiclang import Chord
        return not isinstance(element, Chord)

    def __repr__(self):
        return "Chord"


class NoteMask(TypeMask):
    def __call__(self, element, **kwargs):
        from musiclang import Note
        return not isinstance(element, Note)

    def __repr__(self):
        return "Note"


