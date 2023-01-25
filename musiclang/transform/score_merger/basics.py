from musiclang.transform.merger import ScoreMerger


class ConcatScores(ScoreMerger):

    def action(self, *scores, **kwargs):
        return sum(scores, None)


class TakeFirst(ScoreMerger):

    def action(self, *scores, **kwargs):
        return scores[0]


class TakeLast(ScoreMerger):

    def action(self, *scores, **kwargs):
        return scores[-1]


class TakeIdx(ScoreMerger):

    def __init__(self, idx, **kwargs):
        self.idx = idx

    def action(self, *scores, **kwargs):
        return scores[self.idx]


class TakeSlice(ScoreMerger):

    def __init__(self, slice, **kwargs):
        self.slice = slice

    def action(self, *scores, **kwargs):
        return scores[self.slice]


class ConcatWithPattern(ScoreMerger):

    def __init__(self, pattern, **kwargs):
        self.pattern = pattern

    def action(self, *scores, **kwargs):
        return sum([scores[p] for p in self.pattern], None)


class RandomSelector(ScoreMerger):
    def __init__(self, rg=None):
        import numpy as np
        self.rg = rg if rg is None else np.random.RandomState()

    def __call__(self, *scores, **kwargs):
        return self.rg.choice(scores)