from musiclang.library import *
from musiclang import Note
from fractions import Fraction as frac

from musiclang import Score

class Pattern:

    bar_duration = None
    nb_instruments = 8 # Maximum number of instruments
    drums = False

    def __call__(self, instruments=None, **kwargs):

        pattern_dict = self.action(instruments=instruments, **kwargs)
        if self.drums > 0:
            pattern_dict = self.get_drums(self.drums, pattern_dict)

        return pattern_dict


    def to_json(self):
        return {
            "bar_duration": self.bar_duration,
            "nb_instruments": self.nb_instruments,
            "pattern": str(NC(**self.action([f'v__{i}' for i in range(self.nb_instruments)])))
        }

    @classmethod
    def from_json(cls, json_dict: dict, instruments: list):
        pattern: Score = Score.from_str(json_dict['pattern'])
        nb_instruments = json_dict['nb_instruments']
        all_instruments = pattern.score.keys()
        instruments = [(f'v__{i}', instr) for i, instr in enumerate(instruments[:nb_instruments])]
        pattern_dict = {new_instrument: pattern.score[base_instrument] for base_instrument, new_instrument in instruments}
        for instr in all_instruments:
            if not instr.startswith('v__'):
                pattern_dict[instr] = pattern.score[instr]
        return pattern_dict

    def action(self, instruments=None, **kwargs):
        raise NotImplemented

    def get_drums(self, drums, pattern_dict):
        return pattern_dict



class PluckedChords(Pattern):

    def __init__(self, pluck_spacing=frac(1, 4), bar_duration=4):
        self.pluck_spacing = pluck_spacing
        self.bar_duration = bar_duration

    def action(self, instruments=None, **kwargs):
        pattern_dict = {}
        for i, instr in enumerate(instruments):
            template_note = Note('x', i, 0, 1)
            local_melody = []
            if i > 0:
                local_melody += [r.set_duration(self.pluck_spacing * i)]
            local_melody += [template_note.set_duration(self.pluck_spacing)]
            local_melody += [l.set_duration(self.bar_duration - (i + 1) * self.pluck_spacing)]

            local_melody = sum(local_melody, None)

            pattern_dict[instr] = local_melody

        return pattern_dict


class Waltz(Pattern):

    bar_duration = 3
    spacing = 1

    def action(self, instruments=None, **kwargs):
        pattern_dict = {}
        for i, instr in enumerate(instruments):
            template_note = Note('x', i, 0, 1)
            local_melody = []
            if i == 0:
                local_melody = template_note.set_duration(3 * self.spacing).accent + bd1.set_duration(3 * self.spacing)
            if i > 0:
                silence = r.set_duration(self.spacing)
                note = template_note.set_duration(self.spacing)
                local_melody = (silence.copy().accent + note.copy().accent + note.copy().retarded) * 2

            pattern_dict[instr] = local_melody

        return pattern_dict


class Nocturne(Pattern):

    nb_instruments = 4
    bar_duration = 4
    spacing = frac(1)

    def action(self, instruments=None, **kwargs):
        pattern_dict = {}
        for i, instr in enumerate(instruments):
            if i == 0:
                notes = [Note('x', i, 0, 1).set_duration(self.spacing) for i in range(self.nb_instruments)]
                local_melody = notes[0] + notes[1] + notes[3] + notes[2]
            else:
                local_melody = r.set_duration(self.bar_duration)
            pattern_dict[instr] = local_melody

        return pattern_dict


class AlbertiBass(Pattern):
    nb_instruments = 4
    bar_duration = 4
    spacing = frac(1)

    def action(self, instruments=None, **kwargs):
        pattern_dict = {}
        for i, instr in enumerate(instruments):
            if i == 0:
                notes = [Note('x', i, 0, 1).set_duration(self.spacing) for i in range(self.nb_instruments)]
                local_melody = notes[0] + notes[2] + notes[1] + notes[2]
            else:
                local_melody = r.set_duration(self.bar_duration)
            pattern_dict[instr] = local_melody

        return pattern_dict

class StandardPlucked(Pattern):

    def __init__(self, bar_duration=4):
        self.bar_duration = bar_duration

    def action(self, instruments=None, **kwargs):
        pattern_dict = {}
        for i, instr in enumerate(instruments):
            template_note = Note('x', i, 0, 1)
            local_melody = template_note.set_duration(self.bar_duration).to_melody()
            pattern_dict[instr] = local_melody

        return pattern_dict


class EpicMusicTernary(Pattern):

    bar_duration = 6
    spacing = frac(1 / 2)

    def __init__(self, drums=False):
        self.drums = drums

    def action(self, instruments=None, **kwargs):
        pattern_dict = {}
        for i, instr in enumerate(instruments):
            template_note = Note('x', i, 0, 1)
            local_melody = []
            if i == 0:
                local_melody = template_note.set_duration(self.bar_duration).accent
            if i > 0:
                first = template_note.set_duration(2 * self.spacing)
                local_melody = first.accent + (bu1 + bd1 + bu0 + bu1).e + bu0 + (bu1 + bd1 + bu0 + bu1).e

            pattern_dict[instr] = local_melody
        if self.drums:
            pattern_dict = self.get_drums(self.drums, pattern_dict)
        return pattern_dict

    def get_drums(self, drums, pattern_dict):
        """
        Return a drum pattern associated with this
        Returns
        -------

        """

        pattern_dict['drums__0'] = crash.set_duration(self.bar_duration).accent
        pattern_dict['drums__1'] = (bd.set_duration(self.bar_duration//2).accent) + (sn.set_duration(self.bar_duration//2).accent)
        pattern_dict['drums__3'] = (hh.set_duration(3 * self.spacing) + (hh.set_duration(3 * self.spacing))) * 2
        if drums == 2:
            pattern_dict['drums__4'] = bd.set_duration(self.spacing/2) * int(2 * self.bar_duration / self.spacing)
            pattern_dict['drums__5'] = (ride.set_duration(3 * self.spacing) + (ride.set_duration(3 * self.spacing))) * 2

        return pattern_dict

