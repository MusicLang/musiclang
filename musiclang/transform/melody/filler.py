from musiclang import Melody, Score
from musiclang.transform import ScoreTransformer
from musiclang import Continuation

class MelodyFiller(ScoreTransformer):
    """
    
    """

    def __init__(self, instrument):
        self.instrument = instrument

    def action(self, score: Score, **kwargs):
        pass

        return score