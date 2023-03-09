from .element import Formatter

class RhythmElement(Formatter):

    def __init__(self, instrument, rhythm):
        self.instrument = instrument
        self.rhythm = rhythm

    def to_text(self):
        return '\n' + str(self)

    def __repr__(self):
        return f'!rhythm {self.instrument} {self.rhythm}'
