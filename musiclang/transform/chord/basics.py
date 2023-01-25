from musiclang.transform import ChordTransformer


class Modulate(ChordTransformer):
    """
    Modulate to a different tonality
    """
    def __init__(self, modulation):
        self.modulation = modulation

    def action(self, chord, **kwargs):
        return chord % self.modulation


class ModulateKeepOriginMode(ChordTransformer):
    """
    Modulate to a different tonality, but each chord keeps the same tonality mode
    """
    def __init__(self, modulation):
        from musiclang import Tonality, Element
        if isinstance(modulation, int):
            self.modulation = Tonality(modulation)
        elif isinstance(modulation, Element):
            self.modulation = Tonality(modulation.val)
        else:
            self.modulation = modulation

    def action(self, chord, **kwargs):
        from musiclang import Tonality
        mode = chord.tonality.mode
        new_chord = (chord % self.modulation) % Tonality(0, mode=mode)
        return new_chord


class RepeatChord(ChordTransformer):
    """
    Repeat a chord n times
    """
    def __init__(self, n):
        self.n = n

    def action(self, chord, **kwargs):
        return chord * self.n
