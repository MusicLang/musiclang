from .element import Formatter

class VoicingElement(Formatter):

    def __init__(self, notes):
        self.notes = notes

    def to_text(self):
        return '\n' + str(self)

    def __repr__(self):
        return f'!voicing {" ".join([str(n) for n in self.notes])}'