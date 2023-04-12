from .element import Formatter

class FreeTextElement(Formatter):

    def __init__(self, text):
        self.text = text

    def to_text(self):
        return '\n' + str(self)

    def __repr__(self):
        return str(self.text)
