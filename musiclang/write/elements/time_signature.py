from .element import Formatter

class TimeSignatureElement(Formatter):

    def __init__(self, num, den):
        self.signature = (num, den)

    def to_text(self):
        return '\n' + str(self)

    def __repr__(self):
        return f'Time Signature:{self.signature[0]}/{self.signature[1]}'
