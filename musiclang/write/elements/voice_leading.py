from .element import Formatter

class VoiceLeadingElement(Formatter):

    def __init__(self, fixed_voices=None):
        self.fixed_voices = fixed_voices

    def to_text(self):
        return '\n' + str(self)

    def __repr__(self):
        return f'!voice_leading {" ".join(self.fixed_voices)}'