import numpy as np

from .base_transformer import Transformer
from .mask import Mask


class NoteTransformer(Transformer):
    TYPE = 'NOTE'

    def action(self, note: 'Note', chord=None, instrument=None, **kwargs):
        raise NotImplemented

    def __call__(self, element, on=Mask(), **kwargs):
        from musiclang import Score, Melody, Chord, Note
        if isinstance(element, Note):
            return self.action(element, **kwargs) if on(element, **kwargs) else element.copy()
        if isinstance(element, Melody):
            return self.apply_on_melody(element, on=on, **kwargs)
        elif isinstance(element, list):
            return [self(n) for n in element]
        elif isinstance(element, Chord):
            return self.apply_on_chord(element, on=on, **kwargs)
        elif isinstance(element, Score):
            return self.apply_on_score(element, on=on, **kwargs)
        else:
            raise Exception(f'Cannot apply to type {element.__class__}')


class NoteFilterTransform(NoteTransformer):

    def get_default(self, element):
        return None


class MaskFilter(NoteFilterTransform):

    def __init__(self, on):
        self.on = on

    def action(self, note, chord=None, instrument=None, **kwargs):
        return note

    def __call__(self, element, on=Mask(), **kwargs):
        return super().__call__(element, on=self.on & on, **kwargs)

class NoteMaskFilter(MaskFilter):
    pass


class NoteFilter(NoteFilterTransform):

    def action(self, note, chord=None, instrument=None, **kwargs):
        return note

    def filter(self, element, **kwargs):
        raise NotImplemented

    def __call__(self, element, on=Mask(), **kwargs):
        query_filter = Mask.Note() > Mask.Func(lambda x, **k: self.filter(element, **k))
        return super().__call__(element, on=query_filter & on, **kwargs)


class MelodyTransformer(Transformer):
    TYPE = 'MELODY'

    def action(self, melody, chord=None, instrument=None, **kwargs):
        raise NotImplemented

    def __call__(self, element, on=Mask(), **kwargs):
        from musiclang import Score, Melody, Chord, Note
        if isinstance(element, Melody):
            return self.action(element, **kwargs)
        elif isinstance(element, Note):
            return self.action(Melody([element]), **kwargs)
        elif isinstance(element, list):
            return [self(n, **kwargs) for n in element]
        elif isinstance(element, Chord):
            return self.apply_on_chord(element, on=on, **kwargs)
        elif isinstance(element, Score):
            return self.apply_on_score(element, on=on, **kwargs)
        else:
            raise Exception(f'Cannot apply to type {element.__class__}')


class MelodyFilterTransform(MelodyTransformer):

    def get_default(self, element):
        return None


class MelodyFilter(MelodyFilterTransform):

    def action(self, melody, chord=None, instrument=None, **kwargs):
        return melody

    def filter(self, element, **kwargs):
        raise NotImplemented

    def __call__(self, element, on=Mask(), **kwargs):
        query_filter = Mask.Melody() > Mask.Func(lambda x, **k: self.filter(element, **k))
        return super().__call__(element, on=query_filter & on, **kwargs)


class MelodyMaskFilter(MelodyFilterTransform):

    def __init__(self, on):
        self.on = on

    def action(self, note, chord=None, instrument=None, **kwargs):
        return note

    def __call__(self, element, on=Mask(), **kwargs):
        return super().__call__(element, on=self.on & on, **kwargs)


class ChordTransformer(Transformer):
    TYPE = 'CHORD'

    def action(self, chord, **kwargs):
        raise NotImplemented

    def __call__(self, element, on=Mask(), **kwargs):
        from musiclang import Score, Melody, Chord
        if isinstance(element, Chord):
            return self.action(element, **kwargs)
        elif isinstance(element, Score):
            res = self.apply_on_score(element, on=on, **kwargs)
            return res
        else:
            raise Exception(f'Cannot apply on part of instrument in the type {type(element)}')


class ChordFilterTransform(ChordTransformer):

    def get_default(self, element):
        return None


class ChordFilter(ChordFilterTransform):

    def action(self, chord, **kwargs):
        return chord

    def filter(self, element, **kwargs):
        raise NotImplemented

    def __call__(self, element, on=Mask(), **kwargs):
        query_filter = Mask.Chord() > Mask.Func(lambda x, **k: self.filter(x, **k))
        return super(ChordFilter, self).__call__(element, on=query_filter & on, **kwargs)


class ChordMaskFilter(ChordFilterTransform):

    def __init__(self, on):
        self.on = on

    def action(self, note, **kwargs):
        return note

    def __call__(self, element, on=Mask(), **kwargs):
        return super().__call__(element, on=self.on & on, **kwargs)


class DictTransformer(Transformer):
    TYPE = 'DICT'

    def action(self, melody, chord=None, **kwargs):
        raise NotImplemented

    def __call__(self, element, on=Mask(), **kwargs):
        from musiclang import Score, Melody, Chord
        if isinstance(element, dict):
            return self.action(element, **kwargs)
        if isinstance(element, Chord):
            element = element.copy()
            element.score = self.action(element.score, chord=element, **kwargs)
            return element
        elif isinstance(element, Score):
            chords = [self(m, on=on.child(element), **kwargs) if on(m) else self.get_default(m) for m in element.chords]
            chords = [chord for chord in chords if chord is not None]
            return Score(chords)
        else:
            raise Exception(f'Cannot apply on part of instrument in the type {type(element)}')


class ScoreTransformer(Transformer):
    TYPE = 'SCORE'

    def action(self, score, **kwargs):
        raise NotImplemented

    def __call__(self, data, **kwargs):
        """
        Act on a serie of chords
        :param melody:
        :param kwargs:
        :return:
        """
        from musiclang import Chord
        if isinstance(data, Chord):
            data = data.to_score()
        return self.action(data, **kwargs)


class FeatureExtractor(ScoreTransformer):
    """
    Take a score in input and can returns anything
    """
    TYPE = 'FEATURE'



class Identity(ScoreTransformer):
    def __call__(self, melody, **kwargs):
        return melody.copy()


