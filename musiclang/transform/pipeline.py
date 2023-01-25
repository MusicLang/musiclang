import pickle
import logging


class ConcatPipeline:
    """
    Pipeline object represents a sequence of steps that will lead to a concatenation of successive transforms.

    For each step of the pipeline : ``score = score + transform(score)``

    Examples
    ---------
    Example applying a transpose only on chords that have an "ok" tag :

    >>> from musiclang.library import *
    >>> from musiclang.transform import ConcatPipeline
    >>> transposer = Transpose(2)
    >>> mask = Mask.Chord() > Mask.Has('ok')

    >>> pipeline = ConcatPipeline([('transpose', transposer, mask)])
    >>> score = (I % I.M)(piano=[s0, s2, s4]).add_tag('ok') + (V % I.M)(piano=[s0, s2, s4])
    >>> new_score = pipeline(score)
    >>> new_score
    (I % I.M)(piano=[s0, s2, s4]) + (V % I.M)(piano=[s0, s2, s4]) + (I % I.M)(piano=[s2, s4, s6]) + (V % I.M)(piano=[s0, s2, s4])

    Same example without the query :

    >>> from musiclang.library import *
    >>> from musiclang.transform import ConcatPipeline
    >>> transposer = Transpose(2)
    >>> pipeline = ConcatPipeline([('transpose', transposer)])
    >>> score = (I % I.M)(piano=[s0, s2, s4]).add_tag('ok') + (V % I.M)(piano=[s0, s2, s4])
    >>> new_score = pipeline(score)
    >>> new_score
    (I % I.M)(piano=[s0, s2, s4]) + (V % I.M)(piano=[s0, s2, s4]) + (I % I.M)(piano=[s2, s4, s6]) + (V % I.M)(piano=[s2, s4, s6])

    """
    def __init__(self, steps):
        self.steps = steps

    @property
    def dict_steps(self):
        return dict(self.steps)

    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.steps, f)

    def __repr__(self):
        return "Pipeline({})".format(self.steps.__repr__())

    def get_params(self, **params):
        pass

    def modify(self, param, value):
        candidates = [i for i in range(len(self.steps)) if self.steps[i][0] == param]
        if len(candidates) > 0:
            self.steps[candidates[0]] = (param, value)
        else:
            raise KeyError(f'Not existing param : {param}')

    def set_params(self, _copy=True, **params):
        """
        Set a nested dict of params
        :param params:
        :return:
        """
        if _copy:
            new_pipeline = self.copy()
        else:
            new_pipeline = self
        for param, value in params.items():
            to_modify = new_pipeline.dict_steps[param]
            if isinstance(to_modify, ConcatPipeline):
                new_pipeline.dict_steps[param] = to_modify.set_params(_copy=False, **value)

            else:
                if isinstance(value, dict):
                    new_params = new_pipeline.dict_steps[param].get_params()
                    new_params.update(value)
                    new_pipeline.modify(param, to_modify.__class__(**new_params))
                else:
                    new_pipeline.modify(param, value)

        return new_pipeline

    def copy(self):
        new_pipeline = self.__class__(steps=[])
        for data in self.steps:
            on = Mask()
            if len(data) == 2:
                from .mask import Mask
                step, val = data
            elif len(data) == 3:
                step, val, on = data
            new_pipeline.steps.append((step, val.copy(), on))
        return new_pipeline

    def unpack_args(self, step, f, kwargs):
        if isinstance(f, ConcatPipeline):
            print(kwargs)
            args = {k.split('__')[1]: kwargs[k] for k in kwargs.keys() if k.startswith(step + '__')}
            return args
        else:
            return kwargs

    def __call__(self, score=None, **kwargs):
        from .mask import Mask
        from musiclang import Score
        for data in self.steps:
            on = Mask()
            step, f = '', None
            if len(data) == 2:
                from .mask import Mask
                step, f = data
            elif len(data) == 3:
                step, f, on = data
            arguments = self.unpack_args(step, f, kwargs)
            try:
                to_add = f(score, on=on, **arguments)
                if isinstance(score, Score):
                    score += to_add.add_tag_children(f'step_{step}')
                else:
                    score += to_add
            except Exception as e:
                logging.error(f"Exception in Pipeline: {step}")
                logging.exception(e)
                raise e
        return score

    @staticmethod
    def load(filepath):
        with open(filepath, 'rb') as f:
            return ConcatPipeline(pickle.load(f))


class TransformPipeline(ConcatPipeline):
    """
    Pipeline object represents a sequence of steps that will lead to successive transforms.

    For each step of the pipeline : ``score = transform(score)``


    Examples
    ---------
    Example applying a transpose only on chords that have an "ok" tag :

    >>> from musiclang.library import *
    >>> from musiclang.transform import TransformPipeline
    >>> transposer = Transpose(1)
    >>> mask = Mask.Chord() > Mask.Has('ok')

    >>> pipeline = TransformPipeline([('transpose', transposer, mask), ('transpose2', transposer)])
    >>> score = (I % I.M)(piano=[s0, s2, s4]).add_tag('ok') + (V % I.M)(piano=[s0, s2, s4])
    >>> new_score = pipeline(score)
    >>> new_score
    (I % I.M)(piano=[s2, s4, s6]) + (V % I.M)(piano=[s1, s3, s4])

    The first chord with the tag is transposed twice (first transform match the mask)
    The second one is transposed once

    """

    def __repr__(self):
        return "TransformPipeline({})".format(self.steps.__repr__())

    def __call__(self, score=None, **kwargs):
        from musiclang import Score
        for data in self.steps:
            from .mask import Mask
            on = Mask()
            step, f = None, None
            if len(data) == 2:
                step, f = data
            elif len(data) == 3:
                step, f, on = data

            arguments = self.unpack_args(step, f, kwargs)
            try:
                score = f(score, on=on, **arguments)
                if isinstance(score, Score):
                    score = score.add_tag_children(f'step_{step}')

            except Exception as e:
                logging.error(f"Exception in TransformPipeline step : {step}")
                logging.exception(e)
                raise e

        return score