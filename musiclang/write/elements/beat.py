from .element import Formatter

class BeatElement(Formatter):

    def __init__(self, time):
        self.time = time

    def to_text(self):
        return ' ' + str(self)

    def __repr__(self):
        return f'b{self.time}'