import numpy as np

from .utils_random import *


class Transformer:

    def __call__(self, melody, **kwargs):
        raise NotImplemented

    def get_params(self):
        dic = self.__dict__
        dic = {key: value for key, value in dic.items() if not key.startswith('_')}
        return dic

    def set_params(self, **params):
        for param in params.keys():
            self.__setattr__(param, params[param])

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


    @staticmethod
    def get_part(inst, voice, chord: 'Chord'):
        return chord.score.get(inst + '__' + voice, None)

    def __mul__(self, other):
        if isinstance(other, Transformer):
            return TransformerParallel([self , other])
        if isinstance(other, TransformerParallel):
            return TransformerParallel([self] + other.actions)
        if isinstance(other, TransformerSerie):
            return TransformerSerie([self * action for action in other.actions])

        else:
            raise Exception(f'Cannot add Transformer {type(self)} and {type(other)}')

class NoteTransformer(Transformer):

    def action(self, note: 'Note', **kwargs):
        raise NotImplemented

    def __call__(self, melody, **kwargs):
        from musiclang import Score, Melody, Chord, Note
        if isinstance(melody, Note):
            return self.action(melody, **kwargs)
        if isinstance(melody, Melody):
            new_melody = [self.action(m) for m in melody.notes]
            melo = None
            for m in new_melody:
                melo += m
            return melo
        elif isinstance(melody, list):
            return [self(n) for n in melody]
        elif isinstance(melody, Chord):
            return Chord(melody.element, extension=melody.extension, tonality=melody.tonality,
                         score={key: self(melody.score[key]) for key in melody.score}, octave=melody.octave)
        elif isinstance(melody, Score):
            return Score(chords=[self(chord) for chord in melody.chords])


class MelodyTransformer(Transformer):

    def action(self, melody, **kwargs):
        raise NotImplemented

    def __call__(self, melody, **kwargs):
        from musiclang import Score, Melody, Chord, Note
        if isinstance(melody, Melody):
            return self.action(melody, **kwargs)
        elif isinstance(melody, Note):
            return self.action(Melody([melody]), **kwargs)
        elif isinstance(melody, list):
            return [self(n) for n in melody]
        elif isinstance(melody, Chord):
            return Chord(melody.element, extension=melody.extension, tonality=melody.tonality,
                         score={key: self(melody.score[key]) for key in melody.score}, octave=melody.octave)
        elif isinstance(melody, Score):
            return Score(chords=[self(chord) for chord in melody.chords])

class GlobalTransformer(Transformer):

    def action(self, *data, **kwargs):
        raise NotImplemented

    def __call__(self, *data, **kwargs):
        """
        Act on a serie of chords
        :param melody:
        :param kwargs:
        :return:
        """
        return self.action(*data, **kwargs)


class ScoreTransformer(Transformer):

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



class ChordTransformer(Transformer):

    def action(self, chord, **kwargs):
        raise NotImplemented

    def __call__(self, melody, **kwargs):
        from musiclang import Score, Melody, Chord
        if isinstance(melody, Chord):
            return self.action(melody, **kwargs)
        elif isinstance(melody, Score):
            return Score([self(m, **kwargs) for m in melody.chords])
        else:
            raise Exception(f'Cannot apply on part of instrument in the type {type(melody)}')

class DictTransformer(Transformer):

    def action(self, melody, **kwargs):
        raise NotImplemented

    def __call__(self, melody, **kwargs):
        from musiclang import Score, Melody, Chord
        if isinstance(melody, dict):
            return self.action(melody, **kwargs)
        if isinstance(melody, Chord):
            melody = melody.copy()
            melody.score = self.action(melody.score, **kwargs)
            return melody
        elif isinstance(melody, Score):
            return Score([self(m, **kwargs) for m in melody.chords])
        else:
            raise Exception(f'Cannot apply on part of instrument in the type {type(melody)}')



class Identity(GlobalTransformer):
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
            return TransformerSerie([self] +  other.actions)
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
