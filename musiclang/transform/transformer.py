import numpy as np

from .utils_random import *
from .mask import Mask


class Transformer:
    TYPE = 'TRANSFORMER'

    def __call__(self, element, on=Mask(), **kwargs):
        raise NotImplemented

    def action(self, element, **kwargs):
        raise NotImplemented

    def get_params(self):
        dic = self.__dict__
        dic = {key: value for key, value in dic.items() if not key.startswith('_')}
        return dic

    def set_params(self, **params):
        for param in params.keys():
            self.__setattr__(param, params[param])

    def get_default(self, element):
        return element.copy()

    def copy(self):
        obj = self.__class__(**self.get_params())
        return obj

    def is_valid(self):
        return self.get_params()

    def init_seed(self, **kwargs):
        seed = None
        if "seed" in kwargs.keys():
            seed = kwargs['seed']
        self.seed = seed if seed is not None else np.random.randint(0, 2 ** 31 - 1)
        return self.seed

    def __repr__(self):
        params = self.get_params()
        param_str = "("
        for name, value in params.items():
            if isinstance(value, str):
                value = '"' + value + '"'
            param_str += str(name) + "=" + str(value) + ","

        param_str = param_str[:-1]
        param_str += ")"
        return self.__class__.__name__ + param_str

    def get_part_name(self, part, chord):
        if isinstance(self.part, int):
            return chord.parts[self.part]
        else:
            return part

    def get_parts_name(self, parts, chord):
        return [self.get_part_name(part, chord) for part in parts]

    def convert_to_list(self, val, n, default, constr, increase=True):
        """
        Convert a parameter value to a list given a number
        If
        :param val:
        :param n:
        :param default:
        :param constr:
        :return:
        """
        if val is None:
            res = [default() for i in range(n)]
        elif isinstance(val, constr()):
            res = [val + 5000 * i * increase for i in range(n)]
        else:
            res = val

        return res

    @classmethod
    def random_choice(self, array, chars, seed="", root=""):
        """
        Select an element at random in an array
        """
        return random_choice(array, chars, seed=seed, root=root)

    @classmethod
    def random_permutation(self, chars, array, seed="", root=""):
        """
        Generate a permutation of size n following a bytes encoding
        if chars,seed,root,proba is the same it always generates the same output
        Algorithm : Fisher Yates shuffle  : https://en.wikipedia.org/wiki/Random_permutation#:~:text=A%20simple%20algorithm%20to%20generate,has%20index%200%2C%20and%20the
        :param array: array to shuffle
        :param seed:
        :param root:
        :return:
        """
        return random_permutation(chars, array, seed=seed, root=root)

    @classmethod
    def random_boolean(self, chars, seed="", root="", proba=0.2):
        """
        Generate a random boolean following a bytes encoding
        if chars,seed,root,proba is the same it always generates the same output
        :param seed:
        :param root:
        :param chars:
        :param proba:
        :return:
        """
        return random_boolean(chars, seed=seed, root=root, proba=proba)

    @classmethod
    def random_int(self, chars, low, high, seed="", root=""):
        """
        Generate an integer between low and high following a bytes encoding
        if chars,seed,root,proba is the same it always generates the same output
        :param chars:
        :param low:
        :param high:
        :param seed:
        :param root:
        :return:
        """
        return random_int(chars, low, high, seed=seed, root=root)

    @classmethod
    def random_float(self, chars, low, high, seed="", root=""):
        """
        Generate a float between low and high following a bytes encoding
        if chars,seed,root,proba is the same it always generates the same output
        :param chars:
        :param low:
        :param high:
        :param seed:
        :param root:
        :return:
        """
        return random_float(chars, low, high, seed=seed, root=root)

    def __add__(self, other):
        if isinstance(other, Transformer):
            return TransformerSerie([self, other])
        if isinstance(other, TransformerSerie):
            return TransformerSerie([self] + other.actions)
        if isinstance(other, TransformerParallel):
            return TransformerSerie([self, other])
        else:
            raise Exception(f'Cannot add Transformer {type(self)} and {type(other)}')

    @staticmethod
    def get_instrument_name_and_part(instrument_name):
        """
        Return intrument_name, instrument (before __) and part (after __) as int
        :param instrument_name:
        :return:
        """
        parts = instrument_name.split('__')
        if len(parts) == 1:
            inst, part = parts[0], 0
        else:
            inst, part = parts
            part = int(part)
        return instrument_name, inst, part

    @staticmethod
    def part_is_of_instrument(part, instrument):
        return part.split('__')[0] == instrument

    @staticmethod
    def get_instrument_parts(inst, chord: 'Chord'):
        return [part for part in chord.score.keys() if Transformer.part_is_of_instrument(part, inst)]

    @staticmethod
    def get_instrument_parts_separated(inst, chord: 'Chord'):
        return [part.split('__') for part in chord.score.keys() if Transformer.part_is_of_instrument(part, inst)]

    def apply_on_melody(self, element, on=Mask(), **kwargs):
        from musiclang import Melody
        new_melody = [self.action(m, **kwargs) if on(m, **kwargs) else self.get_default(m) for m in element.notes]
        new_melody = [m for m in new_melody if m is not None]
        return Melody(new_melody, tags=element.tags)

    def apply_on_chord(self, element, on=Mask(), **kwargs):
        from musiclang import Chord
        chord = Chord(element.element, extension=element.extension, tonality=element.tonality,
                      score={
                          key: self(element.score[key], on=on.child(element), chord=element, instrument=key, **kwargs)
                          if on(element.score[key]) else self.get_default(element.score[key]) for key in element.score},
                      octave=element.octave, tags=element.tags)
        # Filter None keys
        return chord(**{part: melody for part, melody in chord.score.items() if melody is not None})

    def apply_on_score(self, element, on=Mask(), **kwargs):
        from musiclang import Score
        chords = [self(m, on=on.child(element), **kwargs) if on(m, **kwargs) else self.get_default(m) for m in
                  element.chords]
        chords = [chord for chord in chords if chord is not None]
        return Score(chords, tags=element.tags)

    @staticmethod
    def get_part(inst, voice, chord: 'Chord'):
        return chord.score.get(inst + '__' + voice, None)

    def __mul__(self, other):
        if isinstance(other, Transformer):
            return TransformerParallel([self, other])
        if isinstance(other, TransformerParallel):
            return TransformerParallel([self] + other.actions)
        if isinstance(other, TransformerSerie):
            return TransformerSerie([self * action for action in other.actions])

        else:
            raise Exception(f'Cannot add Transformer {type(self)} and {type(other)}')


class NoteTransformer(Transformer):
    TYPE = 'NOTE'

    def action(self, note: 'Note', chord=None, instrument=None, **kwargs):
        raise NotImplemented

    def __call__(self, element, on=Mask(), **kwargs):
        from musiclang import Score, Melody, Chord, Note
        if isinstance(element, Note):
            return self.action(element, **kwargs) if on(element) else element.copy()
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
        return self.action(data, **kwargs)


class Identity(ScoreTransformer):
    def __call__(self, melody, **kwargs):
        return melody.copy()


class TransformerSerie:

    def __init__(self, actions):
        self.actions = actions

    def __copy__(self):
        return TransformerSerie([action.copy() for action in self.actions])

    def __add__(self, other):
        if isinstance(other, Transformer):
            return TransformerSerie(self.actions + [other])
        if isinstance(other, TransformerSerie):
            return TransformerSerie(self.actions + other)
        if isinstance(other, TransformerParallel):
            return TransformerSerie(self.actions + [other])
        else:
            raise Exception(f'Cannot add Transformer {type(self)} and {type(other)}')

    def __mul__(self, other):
        if isinstance(other, Transformer):
            return TransformerSerie([action * other for action in self.actions])

        elif isinstance(other, TransformerParallel):
            return TransformerSerie([action * other for action in self.actions])

        else:
            raise Exception(f'Cannot multiply Transformer {type(self)} and {type(other)}')

    def __radd__(self, other):
        if other is None:
            return self
        else:
            raise Exception(f'Cannot add Transformer {type(self)} and {type(other)}')

    def __call__(self, melody, **kwargs):
        score = None
        for action in self.actions:
            if isinstance(action, TransformerParallel):
                temp_score = melody.copy()
                for action_parallel in action.actions:
                    temp_score = action_parallel(temp_score, **kwargs)
                score += temp_score
            else:
                score += action(melody, **kwargs)

        return score


class TransformerParallel:
    def __init__(self, actions):
        self.actions = actions

    def __copy__(self):
        return TransformerParallel([action.copy() for action in self.actions])

    def __add__(self, other):
        if isinstance(other, Transformer):
            return TransformerSerie([self, other])
        if isinstance(other, TransformerSerie):
            return TransformerSerie([self] + other.actions)
        if isinstance(other, TransformerParallel):
            return TransformerSerie([self, other])
        else:
            raise Exception(f'Cannot add Transformer {type(self)} and {type(other)}')

    def __mul__(self, other):
        if isinstance(other, Transformer):
            return TransformerParallel(self.actions + [other])
        if isinstance(other, TransformerParallel):
            return TransformerParallel(self.actions + other)
        else:
            raise Exception(f'Cannot multiply Transformer {type(self)} and {type(other)}')

    def __call__(self, melody, **kwargs):
        score = melody.copy()
        for action_parallel in self.actions:
            score = action_parallel(score, **kwargs)
        return score

    def __rmul__(self, other):
        if other is None:
            return self


class ManyChordTransformer(ChordTransformer):
    def __init__(self, action, args, **kwargs):
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def __call__(self, melody, **kwargs):
        new_melody = melody.copy()
        for args in self.args:
            new_melody = self.action(*args, **kwargs)(new_melody)
        return new_melody
