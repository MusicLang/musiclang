from .element import Formatter

class CounterpointElement(Formatter):

    def __init__(self, fixed_voices=None):
        self.fixed_voices = fixed_voices

    def to_text(self):
        return '\n' + str(self)

    def __repr__(self):
        return f'!counterpoint {" ".join(self.fixed_voices)}'