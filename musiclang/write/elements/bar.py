from .element import Formatter

class BarElement(Formatter):

    def __init__(self, idx=None):
        self.idx = idx

    def to_text(self):
        return '\n' + str(self)

    def __repr__(self):
        real_idx = str(self.idx) if self.idx is not None else 'x'
        return f'm{real_idx}'