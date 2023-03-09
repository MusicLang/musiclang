from .element import Formatter

class TonalityElement(Formatter):

    def __init__(self, tone):
        self.tone = tone

    def to_text(self):
        return ' ' + str(self)

    def __repr__(self):
        return f'{self.tone}:'