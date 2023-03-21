from musiclang.library import *
from musiclang import Note
from fractions import Fraction as frac

class PluckedChords:


    def __init__(self, nb_instruments, pluck_spacing=frac(1, 4), bar_duration=4):
        self.nb_instruments = nb_instruments
        self.pluck_spacing = pluck_spacing
        self.bar_duration = bar_duration

    def __call__(self, *args, **kwargs):
        pass

        pattern_dict = {}
        for i in range(self.nb_instruments):
            template_note = Note('x', i, 0, 1)
            local_melody = []
            if i > 0:
                local_melody += [r.set_duration(self.pluck_spacing * i)]
            local_melody += [template_note.set_duration(self.pluck_spacing)]
            local_melody += [l.set_duration(self.bar_duration - (i + 1) * self.pluck_spacing)]

            local_melody = sum(local_melody, None)

            pattern_dict[f'v__{i}'] = local_melody

        return NC(**pattern_dict)
