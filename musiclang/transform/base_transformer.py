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
        beat = 0
        idx = 0
        last_note = None
        new_melody = []
        for m in element.notes:
            note = self.action(m, beat=beat, idx=idx,
                               last_note=last_note, **kwargs) if on(m, beat=beat, idx=idx,
                                                                    last_note=last_note,
                                                                    **kwargs) else self.get_default(m)
            beat += m.duration
            idx += 1
            last_note = m
            if note is not None:
                new_melody.append(note)

        new_melody = [m for m in new_melody if m is not None]
        return Melody(new_melody, tags=element.tags)

    def apply_on_chord(self, element, on=Mask(), **kwargs):
        from musiclang import Chord
        chord = Chord(element.element, extension=element.extension, tonality=element.tonality,
                      score={
                          key: self(element.score[key], on=on.child(element, **kwargs), chord=element, instrument=key, **kwargs)
                          if on(element.score[key], chord=element, instrument=key, **kwargs)
                          else self.get_default(element.score[key]) for key in element.score},
                      octave=element.octave, tags=element.tags)
        # Filter None keys
        return chord(**{part: melody for part, melody in chord.score.items() if melody is not None})

    def apply_on_score(self, element, on=Mask(), **kwargs):
        beat = 0
        idx = 0
        last_chord = None
        score = None
        for m in element.chords:
            chord = self(m, on=on.child(element, **kwargs), chord_beat=beat, chord_idx=idx, last_chord=last_chord, **kwargs)\
                if on(m, chord_beat=beat, chord_idx=idx, last_chord=last_chord, **kwargs) else self.get_default(m)
            beat += m.duration
            idx += 1
            last_chord = m
            if chord is not None:
                score += chord

        return score.add_tags(element.tags)

    @staticmethod
    def get_part(inst, voice, chord: 'Chord'):
        return chord.score.get(inst + '__' + voice, None)

