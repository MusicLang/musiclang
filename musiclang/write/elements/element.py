class Formatter:

    def to_text(self):
        pass

    @classmethod
    def parse_text(cls, elements):
        return ''.join([e.to_text() for e in elements])
