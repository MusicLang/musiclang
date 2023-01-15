import pickle
import logging


class Pipeline:
    """
    Pipeline object represents a sequence of steps that will lead to a concatenation of score
    You can pass parameters to pipelines because you use named steps :

    >>> pipeline =Pipeline(steps=[('partA', ActionWithArgs), ('partB', Action2WithArgs)])
    >>> score = pipeline(partA=someArgs, partB=someArgs2)
    You can nest pipelines in the steps and we use arguments unpacking to nest the arguments :
    >>> pipeline =Pipeline(steps=[('p1', Pipeline([('partA': ActionWithArgs), ('partB': ActionWithArgs)])), ('partC', Action2WithArgs)])
    >>> pipeline(p1__partA=someArgs, p1__partB=someOtherArgs, partC=args)
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
            if isinstance(to_modify, Pipeline):
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
        for step, val in self.steps:
            new_pipeline.steps.append((step, val.copy()))
        return new_pipeline

    def unpack_args(self, step, f, kwargs):
        if isinstance(f, Pipeline):
            args = {k.split('__')[1]: kwargs[k] for k in kwargs.keys() if k.startswith(step + '__')}
            return args
        else:
            return kwargs

    def __call__(self, score=None, **kwargs):
        for step, f in self.steps:
            arguments = self.unpack_args(step, f, kwargs)
            try:
                score += f(score, **arguments)
            except Exception as e:
                logging.error(f"Exception in Pipeline: {step}")
                logging.exception(e)
                raise e
        return score

    @staticmethod
    def load(filepath):
        with open(filepath, 'rb') as f:
            return Pipeline(pickle.load(f))


class VerticalPipeline(Pipeline):

    def __repr__(self):
        return "VerticalPipeline({})".format(self.steps.__repr__())

    def __call__(self, score=None, **kwargs):
        for step, f in self.steps:
            arguments = self.unpack_args(step, f, kwargs)
            try:
                score = f(score, **arguments)

            except Exception as e:
                logging.error(f"Exception in VerticalPipeline step : {step}")
                logging.exception(e)
                raise e

        return score