

class ScoreMerger:

    def action(self, *scores, **kwargs):
        raise NotImplemented

    def __call__(self, *scores, **kwargs):
        return self.action(*scores, **kwargs)