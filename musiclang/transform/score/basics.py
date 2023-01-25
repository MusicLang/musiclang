from musiclang.transform import ScoreTransformer


class RepeatScore(ScoreTransformer):
    def __init__(self, n):
        self.n = n

    def action(self, score, **kwargs):
        return score * self.n
