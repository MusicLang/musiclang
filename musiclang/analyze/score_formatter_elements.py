from fractions import Fraction as frac
import re
from musiclang.library import *

class BaseElement:

    def to_text(self):
        pass


class Bar(BaseElement):

    def __init__(self, idx=None):
        self.idx = idx

    def to_text(self):
        real_idx = str(self.idx) if self.idx is not None else 'x'
        return f'\nm{real_idx}'


class TonalityLine(BaseElement):

    def __init__(self, text):
        self.text = text
        self.tonality = None
        self.init()

    def init(self):
        self.tonality = self.text.split(':')[1].replace(' ', '')
    def to_text(self):
        return f'{self.key}:{self.mode}'

    def parse(self, score, parent):
        return CurrentTonality(self.tonality).parse(score, parent)
class CurrentTonality(BaseElement):

    def __init__(self, text):
        self.text = text
        self.key = 0
        self.mode = 'M'
        self.init()

    def to_text(self):
        return self.text + ' '

    def init(self):
        tab = 'CDEFGAB'
        notes = [0, 2, 4, 5, 7, 9, 11]
        note = self.text.replace(':', '').replace('#', '').replace('b', '').replace('-', '')
        tone = notes[tab.index(note.upper())]
        mode = 'major' if note.upper() == note else 'minor'

        tone += self.text.count('#')
        tone -= self.text.count('b')
        tone -= self.text.count('-')

        self.key = tone
        self.mode = mode

    def parse(self, score, parent):
        parent.key = self.key
        parent.mode = self.mode
        return score

    def __repr__(self):
        return f"CurrentTonality({self.key}, {self.mode})"



class BarLine:
    def __init__(self, text, parent):
        self.text = text
        self.idx = 0
        self.init(parent)

    def is_chord(self, element):
        return not self.is_beat(element)

    def is_beat(self, element):
        return element.startswith('b') and element[1].isdigit()

    def is_tonality(self, element):
        return ':' in element and not ('|' in element)

    def init(self, parent):
        # Get bar idx, ignoring var
        bar_number = self.text.split(' ')[0].split('var')[0]
        if 'x' in bar_number:
            self.idx = parent.init_bar_number + 1
        else:
            self.idx = int(bar_number[1:])

    def get_elements(self):
        array = self.text.split(' ')
        elements = []
        last_was_chord = False
        for element in array[1:]:
            if self.is_beat(element):
                elements.append(Beat(element))
                last_was_chord = False  # Only a beat can allow a new chord
            elif self.is_tonality(element):
                elements.append(CurrentTonality(element))
            elif self.is_chord(element) and not last_was_chord:
                if element != '':
                    elements.append(BarChord(element))
                    last_was_chord = True
        return elements

    def parse(self, score, parent):
        parent.set_bar_number(self.idx)
        return score

    def __repr__(self):
        return f"Bar({self.idx})"



class MultiBar:
    def __init__(self, text):
        self.text = text
        self.receiver_range = None
        self.emitter_range = None
        self.init()

    def is_chord(self, element):
        pass

    def is_beat(self, element):
        pass

    def init(self):
        new, old = self.text.replace(' ', '').split('=')
        res = new[1:].split('-')
        if len(res) == 1:
            a = res[0]
            b = a
        else:
            a, b = res

        a, b = int(a), int(b) + 1
        self.receiver_range = a, b

        res = old[1:].split('-')
        if len(res) == 1:
            c = res[0]
            d = c
        else:
            c, d = res
        c, d = int(c), int(d) + 1
        self.emitter_range = c, d
        if d - c != b - a:
            raise Exception(f'Range of bars must be equals for: {self.text}')

    def parse(self, score, parent):
        return score

    def __repr__(self):
        return f"MultiBar({self.text})"


class Event:

    def __new__(cls, text, parent):
        return cls.init(text, parent)

    @classmethod
    def is_generate(cls, text):
        return text.replace(' ', '').startswith('!generate')

    @classmethod
    def is_voicing(cls, text):
        return text.replace(' ', '').startswith('!voicing')

    @classmethod
    def is_voice_leading(cls, text):
        return text.replace(' ', '').startswith('!voice_leading')

    @classmethod
    def is_rhythm(cls, text):
        return text.replace(' ', '').startswith('!rhythm')

    @classmethod
    def is_instruments(cls, text):
        return text.replace(' ', '').startswith('!instruments')

    @classmethod
    def is_counterpoint(cls, text):
        return text.replace(' ', '').startswith('!counterpoint')

    @classmethod
    def init(cls, text, parent):
        if cls.is_generate(text):
            return Generate(text)
        elif cls.is_voicing(text):
            return Voicing(text)
        elif cls.is_instruments(text):
            return Instruments(text)
        elif cls.is_rhythm(text):
            return Rhythm(text, parent)
        elif cls.is_voice_leading(text):
            return VoiceLeading(text, parent)
        elif cls.is_counterpoint(text):
            return Counterpoint(text, parent)
        else:
            raise Exception(f'Not existing event {text}')




class Counterpoint:
    def __init__(self, text, parent):
        self.text = text
        self.init(parent)

    def init(self, parent):
        self.text = re.sub(' +', ' ', self.text)
        insts = ','.join([f"'{ins}'" for ins in self.text.replace('!counterpoint', '').lstrip(' ').split(' ')])
        insts = eval(insts + ',')
        tracks = {}
        # Assign tracks
        fixed_voices = []
        for ins in insts:
            if ins != '':
                if '__' in ins:
                    fixed_voices.append(ins)
                    tracks[ins] = int(ins.split('__')[1]) + 1
                else:
                    fixed_voices.append(f'{ins}__{tracks.get(ins, 0)}')
                    tracks[ins] = tracks.get(ins, 0) + 1

        self.fixed_voices = fixed_voices
        parent.set_counterpoint(self.fixed_voices)

    def parse(self, score, parent):

        return score

    def __repr__(self):
        return f"Counterpoint({self.text})"


class VoiceLeading:
    def __init__(self, text, parent):
        self.text = text
        self.init(parent)

    def init(self, parent):
        from musiclang.transform import VoiceLeading
        self.text = re.sub(' +', ' ', self.text)
        insts = ','.join([f"'{ins}'" for ins in self.text.replace('!voice_leading', '').lstrip(' ').split(' ')])
        insts = eval(insts + ',')
        tracks = {}
        # Assign tracks
        fixed_voices = []
        for ins in insts:
            if ins != '':
                if '__' in ins:
                    fixed_voices.append(ins)
                    tracks[ins] = int(ins.split('__')[1]) + 1
                else:
                    fixed_voices.append(f'{ins}__{tracks.get(ins, 0)}')
                    tracks[ins] = tracks.get(ins, 0) + 1
        self.voice_leading = VoiceLeading(fixed_voices=fixed_voices)
        parent.set_voice_leading(self.voice_leading)

    def parse(self, score, parent):

        return score

    def __repr__(self):
        return f"VoiceLeading({self.text})"


class Rhythm:
    """
    Apply a rhythm to a specific part
    """
    def __init__(self, text, parent):
        self.text = text
        self.init(parent)

    def init(self, parent):
        self.text = re.sub(' +', ' ', self.text)
        self.text = self.text.lstrip(' ')
        args = self.text.split(' ')
        self.instrument = f"{args[1]}"
        self.rhythm = f"{args[2]}"
        self.nb_bars = len(self.rhythm.split('|'))
        self.rhythm = [r if r in ['x', '.'] else '' for r in self.rhythm.replace('|', '')]
        self.rhythm = [1 if r == 'x' else 0 for r in self.rhythm]
        if '__' not in self.instrument:
            self.instrument = f"{self.instrument}__0"
        parent.set_rhythm(self.instrument, self.nb_bars, self.rhythm)

    def parse(self, score, parent):
        return score

    def __repr__(self):
        return f"Rhythm({self.text})"


class Instruments:
    def __init__(self, text):
        self.text = text
        self.init()

    def init(self):
        self.text = re.sub(' +', ' ', self.text)
        insts = ','.join([f"'{ins}'" for ins in self.text.replace('!instruments', '').lstrip(' ').split(' ')])
        insts = eval(insts)
        if isinstance(insts, str):
            insts = (insts,)
        tracks = {}
        # Assign tracks
        self.instruments = []
        for ins in insts:
            self.instruments.append(f'{ins}__{tracks.get(ins, 0)}')
            tracks[ins] = tracks.get(ins, 0) + 1

    def parse(self, score, parent):
        parent.instruments = self.instruments
        return score

    def __repr__(self):
        return f"Instruments({self.text})"

class Voicing:
    def __init__(self, text):
        self.text = text
        self.init()

    def init(self):
        import re
        self.text = re.sub(' +', ' ', self.text)
        self.score = ','.join([f"{ins}" for ins in self.text.replace('!voicing', '').lstrip(' ').split(' ')])
        self.score = eval(self.score)

    def parse(self, score, parent):
        parent.current_score = self.score
        return score

    def __repr__(self):
        return f"Voicing({self.text})"

class Generate:
    def __init__(self, text):
        self.text = text

    def parse(self, score, parent):
        return score

    def __repr__(self):
        return f"Generate({self.text})"


class TimeSignature:

    def __init__(self, text):
        self.text = text
        self.num = 4
        self.den = 4


    def parse(self, score, parent):
        num, den = self.text.split(':')[1].replace(' ', '').split('/')
        parent.set_time_signature((int(num), int(den)))
        return score

    def __repr__(self):
        return f'TimeSignature({self.num}, {self.den})'


class Beat:
    def __init__(self, text):
        self.text = text
        self.value = None
        self.init()

    def init(self):
        from fractions import Fraction as frac
        self.value = self.text.replace('b', '')

    def get_real_value(self, parent):
        CONVENTION_DICT = {(6, 8): 2, (2, 2): 2}
        nb_beats = CONVENTION_DICT.get(parent.time_signature, parent.duration)
        ratio = frac(nb_beats / parent.duration).limit_denominator(8)
        real_value = frac(float(self.value)).limit_denominator(8) - 1
        real_value /= ratio
        return real_value

    def parse(self, score, parent):
        parent.set_current_beat(self.get_real_value(parent))
        return score

    def __repr__(self):
        return f'Beat({self.value})'


class BarChord:

    def __init__(self, text):
        self.text = text

    def parse(self, score, parent):
        try:
            from musiclang import Chord, Tonality
            from musiclang.analyze.roman_parser import analyze_one_chord
            key, mode = parent.key, parent.mode
            final_degree, extension, final_key, final_mode = analyze_one_chord(self.text, key, mode)
            chord = Chord(final_degree,
                          tonality=Tonality(final_key, final_mode))[extension]
            new_dur = parent.duration - parent.current_beat
            applied_score = {key: item for key, item in zip(parent.instruments, parent.current_score)}
            chord = chord(**applied_score).set_duration(new_dur)
            score = parent.add_chord(chord, score)
        except Exception as e:
            new_exc = Exception(f"Exception for '{self.text}' occured at beat {parent.current_beat} of bar {parent.bar_number} : {e} ")
            print(new_exc)
            #raise new_exc from e
        return score

    def __repr__(self):
        return f"Chord({self.text})"


